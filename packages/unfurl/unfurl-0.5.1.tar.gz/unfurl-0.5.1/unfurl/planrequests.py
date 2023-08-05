# Copyright (c) 2021 Adam Souzis
# SPDX-License-Identifier: MIT
import collections
import re
from typing import Iterator, List, Optional, Sequence, Tuple
import six
import shlex
import sys
import os
import os.path

from .util import (
    lookup_class,
    load_module,
    find_schema_errors,
    UnfurlError,
    UnfurlTaskError,
    to_enum,
)
from .result import serialize_value
from .support import Defaults, NodeState, Priority
from .runtime import EntityInstance
import logging

logger = logging.getLogger("unfurl")


# we want ConfigurationSpec to be independent of our object model and easily serializable
class ConfigurationSpec:
    @classmethod
    def getDefaults(cls):
        return dict(
            className=None,
            majorVersion=0,
            minorVersion="",
            workflow=Defaults.workflow,
            timeout=None,
            operation_host=None,
            environment=None,
            inputs=None,
            inputSchema=None,
            preConditions=None,
            postConditions=None,
            primary=None,
            dependencies=None,
            outputs=None,
            interface=None,
            entry_state=None,
            base_dir=None,
        )

    def __init__(
        self,
        name,
        operation,
        className=None,
        majorVersion=0,
        minorVersion="",
        workflow=Defaults.workflow,
        timeout=None,
        operation_host=None,
        environment=None,
        inputs=None,
        inputSchema=None,
        preConditions=None,
        postConditions=None,
        primary=None,
        dependencies=None,
        outputs=None,
        interface=None,
        entry_state=None,
        base_dir=None,
    ):
        assert name and className, "missing required arguments"
        self.name = name
        self.operation = operation
        self.className = className
        self.majorVersion = majorVersion
        self.minorVersion = minorVersion
        self.workflow = workflow
        self.timeout = timeout
        self.operation_host = operation_host
        self.environment = environment
        self.inputs = inputs or {}
        self.inputSchema = inputSchema
        self.outputs = outputs or {}
        self.preConditions = preConditions
        self.postConditions = postConditions
        self.artifact = primary
        self.dependencies = dependencies
        self.interface = interface
        self.entry_state = to_enum(NodeState, entry_state, NodeState.creating)
        self.base_dir = base_dir

    def find_invalidate_inputs(self, inputs):
        if not self.inputSchema:
            return []
        return find_schema_errors(serialize_value(inputs), self.inputSchema)

    # XXX same for postConditions
    def find_invalid_preconditions(self, target):
        if not self.preConditions:
            return []
        # XXX this should be like a Dependency object
        expanded = serialize_value(target.attributes)
        return find_schema_errors(expanded, self.preConditions)

    def create(self):
        className = self.className
        klass = lookup_class(className)
        if not klass:
            raise UnfurlError(f"Could not load configurator {self.className}")
        else:
            return klass(self)

    def should_run(self):
        return Defaults.shouldRun

    def copy(self, **mods):
        args = self.__dict__.copy()
        args.update(mods)
        return ConfigurationSpec(**args)

    def __eq__(self, other):
        if not isinstance(other, ConfigurationSpec):
            return False
        return (
            self.name == other.name
            and self.operation == other.operation
            and self.className == other.className
            and self.majorVersion == other.majorVersion
            and self.minorVersion == other.minorVersion
            and self.workflow == other.workflow
            and self.timeout == other.timeout
            and self.environment == other.environment
            and self.inputs == other.inputs
            and self.inputSchema == other.inputSchema
            and self.outputs == other.outputs
            and self.preConditions == other.preConditions
            and self.postConditions == other.postConditions
            and self.interface == other.interface
        )


class PlanRequest:
    error = None
    future_dependencies: list = []
    task = None
    render_errors = None

    def __init__(self, target: "EntityInstance"):
        self.target = target

    @property
    def root(self):
        return self.target.root if self.target else None

    def update_future_dependencies(self, completed):
        return self.future_dependencies

    def get_operation_artifacts(self):
        return []

    def include_in_plan(self):
        if self.task and self.task.priority == Priority.critical:
            return True  # XXX hackish, just used for primary_provider
        if self.target.priority is not None:
            return self.target.priority >= Priority.required
        if self.target.created:
            #  if already created then always include the resource
            return True
        return self.target.template.required

    def has_unfulfilled_refs(self) -> bool:
        for dep in self.get_unfulfilled_refs():
            return True
        return False

    def get_unfulfilled_refs(self):
        if not self.render_errors:
            return
        for error in self.render_errors:
            dep = getattr(error, "dependency", None)
            if dep:
                yield dep

    def update_unfulfilled_errors(self):
        self.render_errors = list(self._get_unfulfilled_errors())
        return self.has_unfulfilled_refs()

    def _get_unfulfilled_errors(self):
        if not self.render_errors:
            return
        for error in self.render_errors:
            dep = getattr(error, "dependency", None)
            if not dep or not dep.validate():
                yield error

    @property
    def not_ready(self):
        return self.future_dependencies or self.has_unfulfilled_refs()

    @property
    def name(self):
        return type(self).__name__

    def __str__(self) -> str:
        return f'Planned task {self.name} for "{self.target.name}"'


class TaskRequest(PlanRequest):
    """
    Yield this to run a child task. (see :py:meth:`unfurl.configurator.TaskView.create_sub_task`)
    """

    def __init__(
        self,
        configSpec,
        target,
        reason,
        persist=False,
        required=None,
        startState=None,
    ):
        super().__init__(target)
        self.configSpec = configSpec
        self.reason = reason
        self.persist = persist
        self.required = required
        self.error = configSpec.name == "#error"
        self.startState = startState
        self.task = None

    def _get_artifact_plan(self, artifact):
        # the artifact has an interface so it needs to be installed on the operation_host
        if artifact and artifact.get_interfaces():
            # the same global artifact can have different local names when declared on a node template
            # but are uniquely identified by (file, repository) so use that to generate a unique node template name
            name = "__artifact__" + artifact.get_name_from_artifact_spec(
                artifact.as_import_spec()
            )
            operation_host = (
                find_operation_host(self.target, self.configSpec.operation_host)
                or self.target.root
            )
            existing = operation_host.root.find_instance(name)
            if existing:
                if existing.operational:
                    return None
                else:
                    return JobRequest([existing])
            else:
                if not operation_host.template.spec.get_template(name):
                    # template isn't defined, define inline
                    artifact_tpl = artifact.toscaEntityTemplate.entity_tpl
                    template = dict(
                        name=name,
                        directives=["protected"],
                        type="unfurl.nodes.ArtifactInstaller",
                        artifacts={"install": artifact_tpl},
                    )
                    artifact_type = artifact_tpl["type"]
                    if (
                        artifact_type
                        not in operation_host.template.spec.template.topology_template.custom_defs
                    ):
                        # operation_host must be in an external ensemble that doesn't have the type def
                        artifact_type_def = self.target.template.spec.template.topology_template.custom_defs[
                            artifact_type
                        ]
                        template["custom_types"] = {artifact_type: artifact_type_def}
                else:
                    template = name

                return JobRequest(
                    [operation_host],
                    update=dict(
                        name=name,
                        parent=operation_host.name,
                        template=template,
                        attributes=artifact.properties,
                    ),
                )
        return None

    def get_operation_artifacts(self):
        artifacts = []
        if self.configSpec.dependencies:
            for artifact in self.configSpec.dependencies:
                jobRequest = self._get_artifact_plan(artifact)
                if jobRequest:
                    artifacts.append(jobRequest)
        jobRequest = self._get_artifact_plan(self.configSpec.artifact)
        if jobRequest:
            artifacts.append(jobRequest)
        return artifacts

    @property
    def name(self):
        if self.configSpec.operation:
            name = self.configSpec.operation
        else:
            name = self.configSpec.name
        if self.reason and self.reason not in name:
            return name + " (reason: " + self.reason + ")"
        return name

    def update_future_dependencies(self, completed):
        self.future_dependencies = [
            fr for fr in self.future_dependencies if fr not in completed
        ]
        return self.future_dependencies

    def _summary_dict(self, include_rendered=True):
        summary = dict(
            operation=self.configSpec.operation or self.configSpec.name,
            reason=self.reason,
        )
        rendered = {}
        if self.task and self.task._workFolders:
            for name, wf in self.task._workFolders.items():
                rendered[name] = wf.cwd
        if include_rendered:
            summary["rendered"] = rendered
        return summary

    def __repr__(self):
        state = " " + (self.target.state and self.target.state.name or "")
        return (
            f"TaskRequest({self.target}({self.target.status.name}{state}):{self.name})"
        )


class SetStateRequest(PlanRequest):
    def __init__(self, target, state):
        super().__init__(target)
        self.set_state = state

    @property
    def name(self):
        return self.set_state

    def _summary_dict(self):
        return dict(set_state=self.set_state)


class TaskRequestGroup(PlanRequest):
    def __init__(self, target, workflow):
        super().__init__(target)
        self.workflow = workflow
        self.children = []

    @property
    def future_dependencies(self):
        future_dependencies = []
        for req in self.children:
            future_dependencies.extend(req.future_dependencies)
        return future_dependencies

    def update_future_dependencies(self, completed):
        future_dependencies = []
        for req in self.children:
            future_dependencies.extend(req.update_future_dependencies(completed))
        return future_dependencies

    def get_operation_artifacts(self):
        artifacts = []
        for req in self.children:
            artifacts.extend(req.get_operation_artifacts())
        return artifacts

    def get_unfulfilled_refs(self):
        for req in self.children:
            yield from req.get_unfulfilled_refs()

    def update_unfulfilled_errors(self):
        for req in self.children:
            req.update_unfulfilled_errors()
        return self.has_unfulfilled_refs()

    def __str__(self) -> str:
        if self.children:
            return str(self.children)
        else:
            return f'Planned task {self.workflow} for "{self.target.name}"'

    def __repr__(self):
        return f"TaskRequestGroup({self.target}:{self.workflow}:{self.children})"


class JobRequest:
    """
    Yield this to run a child job.
    """

    def __init__(self, resources, errors=None, update=None):
        self.instances = resources
        self.errors = errors or []
        self.update = update

    def get_instance_specs(self):
        if self.update:
            return [self.update]
        else:
            return [r.name for r in self.instances]

    @property
    def name(self):
        if self.update:
            return self.update["name"]
        elif self.instances:
            return self.instances[0].name
        else:
            return ""

    @property
    def target(self):
        # XXX replace instances with target
        if self.instances:
            return self.instances[0]
        else:
            return None

    @property
    def root(self):
        if self.instances:
            # all instances need the same root
            assert (
                len(self.instances) == 1
                or len(set(id(i.root) for i in self.instances)) == 1
            )
            return self.instances[0].root
        else:
            return None

    def __repr__(self):
        return f"JobRequest({self.name})"


def find_operation_host(target, operation_host):
    # SELF, HOST, ORCHESTRATOR, SOURCE, TARGET
    if not operation_host or operation_host in ["localhost", "ORCHESTRATOR"]:
        return target.root.find_instance_or_external("localhost")
    if operation_host == "SELF":
        return target
    if operation_host == "HOST":
        # XXX should search all ancestors to find parent that can handle the given operation
        # e.g. ansible configurator should find ancestor compute node
        return target.parent
    if operation_host == "SOURCE":
        return target.source
    if operation_host == "TARGET":
        return target.target
    return target.root.find_instance_or_external(operation_host)


def get_render_requests(
    requests: Sequence[PlanRequest],
) -> Iterator[Tuple[Optional[TaskRequestGroup], TaskRequest]]:
    # returns requests that can be rendered grouped by its top-most task group
    for req in requests:
        if isinstance(req, TaskRequestGroup):
            for parent, child in get_render_requests(req.children):
                yield req, child  # yields root as parent
        elif isinstance(req, TaskRequest):
            yield None, req
        elif not isinstance(req, SetStateRequest):
            # note: SetStateRequests don't render, only run
            assert not req, f"unexpected type of request: {req}"


def _get_deps(parent, req, liveDependencies, requests):
    previous = None
    for (root, r) in requests:
        if req.target.key == r.target.key:
            continue  # skip self
        if req.required is not None and not req.required:
            continue  # skip requests that aren't going to run
        if r.target.key in liveDependencies:
            if root:
                if previous is root or parent is root:
                    # only yield root once and
                    # don't consider requests in the same root
                    continue
                previous = root
            yield root or r


def set_fulfilled(requests, completed):
    # requests, completed are top level requests,
    # as is future_dependencies
    ready, notReady = [], []
    for req in requests:
        _not_ready = False
        # always need to evaluate both:
        if req.update_future_dependencies(completed):
            _not_ready = True
        if req.update_unfulfilled_errors():
            _not_ready = True
        if _not_ready:
            notReady.append(req)
        else:  # list is now empty so request is ready
            ready.append(req)
    return ready, notReady


def _prepare_request(job, req: TaskRequest, errors):
    # req is a taskrequests, future_requests are (grouprequest, taskrequest) pairs
    if req.task:
        task = req.task
        task._attributeManager.attributes = {}
        task.target.root.attributeManager = task._attributeManager
    else:
        task = req.task = job.create_task(req.configSpec, req.target, reason=req.reason)
    error = None
    try:
        proceed, msg = job.should_run_task(task)
        if not proceed:
            req.required = False
            if task._errors:
                error = task._errors[0]
            logger.debug(
                "skipping task %s for instance %s with state %s and status %s: %s",
                req.configSpec.operation,
                req.target.name,
                req.target.state,
                req.target.status,
                msg,
            )
            # we want to track and save skipped tasks
            job.add_work(task)
    except Exception:
        proceed = False
        # note: failed rendering may be re-tried later if it has dependencies
        error = UnfurlTaskError(task, "should_run_task failed", logging.DEBUG)
    if error:
        task._inputs = None
        task._attributeManager.attributes = {}  # rollback changes
        errors.append(error)
    else:
        task.commit_changes()
    return proceed


def _render_request(job, parent, req, requests):
    # req is a taskrequests, future_requests are (grouprequest, taskrequest) pairs
    assert req.task
    task = req.task
    task._attributeManager.attributes = {}
    task.target.root.attributeManager = task._attributeManager

    error = None
    error_info = None
    try:
        task.logger.debug("rendering %s %s", task.target.name, task.name)
        task._rendering = True
        task.inputs
        assert not task._inputs.context.strict
        task.rendered = task.configurator.render(task)
    except Exception:
        # note: failed rendering may be re-tried later if it has dependencies
        error_info = sys.exc_info()
        error = UnfurlTaskError(task, "Configurator render failed", False)
    if task._errors:
        # we turned off strictness so templating errors got saved here instead
        req.render_errors = task._errors
        error = task._errors[0]
        task._errors = []
    task._rendering = False
    task._attributeManager.mark_referenced_templates(task.target.template)

    if parent and parent.workflow == "undeploy":
        # when removing an instance don't worry about depending values changing in the future
        deps = []
    else:
        # key => (instance, list<attribute>)
        liveDependencies = task._attributeManager.find_live_dependencies()
        task.logger.trace(f"liveDependencies for {task.target}: {liveDependencies}")
        # a future request may change the value of these attributes
        deps = list(_get_deps(parent, req, liveDependencies, requests))

    dependent_refs = [dep.expr for dep in req.get_unfulfilled_refs()]
    if deps or dependent_refs:
        req.future_dependencies = deps
        task.logger.debug(
            "%s:%s can not render yet, depends on %s",
            task.target.name,
            req.configSpec.operation,
            deps or dependent_refs,
            exc_info=error_info,
        )
        # rollback changes:
        task._errors = []
        task._inputs = None
        task._attributeManager.attributes = {}
        task.discard_work_folders()
        return deps or dependent_refs, None
    elif error:
        task.fail_work_folders()
        task._inputs = None
        task.logger.warning("Configurator render failed", exc_info=error_info)
        task._attributeManager.attributes = {}  # rollback changes
        return None, error
    else:
        task.logger.trace(f"committing changes from rendering task {task.target}")
        task.commit_changes()
        return None, None


def _add_to_req_list(reqs, parent, request):
    if parent:  # only add if we haven't already
        if not reqs or reqs[-1] is not parent:
            reqs.append(parent)
    else:
        reqs.append(request)


def _reevaluate_not_required(not_required, render_requests):
    # keep rendering if a not_required template was referenced and is now required
    new_not_required = []
    for (parent, request) in not_required:
        if request.include_in_plan():
            request.target.validate()
            render_requests.append((parent, request))
        else:
            new_not_required.append((parent, request))
    return new_not_required


def do_render_requests(
    job, requests: Sequence[PlanRequest]
) -> Tuple[List[PlanRequest], List[PlanRequest], List[UnfurlError]]:
    ready: List[PlanRequest] = []
    notReady: List[PlanRequest] = []
    errors: List[UnfurlError] = []
    flattened_requests = list(
        (p, r)
        for (p, r) in get_render_requests(requests)
        if _prepare_request(job, r, errors)
    )
    not_required = []
    render_requests = collections.deque(flattened_requests)
    while render_requests:
        parent, request = render_requests.popleft()
        # we dont require default templates that aren't referenced
        # (but skip this check if the job already specified specific instances)
        required = (
            job.workflow != "deploy" or job.is_filtered() or request.include_in_plan()
        )
        if not required:
            not_required.append((parent, request))
        else:
            request.target.validate()
            deps, error = _render_request(job, parent, request, flattened_requests)
            if error:
                errors.append(error)
            elif deps:
                # remove parent from ready if added it there
                if parent and ready and ready[-1] is parent:
                    ready.pop()
                _add_to_req_list(notReady, parent, request)
            elif not parent or not notReady or notReady[-1] is not parent:
                # don't add if the parent was placed on the notReady list
                _add_to_req_list(ready, parent, request)
            not_required = _reevaluate_not_required(not_required, render_requests)

    for (parent, request) in not_required:
        _add_to_req_list(notReady, parent, request)
    return ready, notReady, errors


def _filter_config(opts, config, target):
    if opts.readonly and config.workflow != "discover":
        return None, "read only"
    if opts.requiredOnly and not config.required:
        return None, "required"
    if opts.instance and target.name != opts.instance:
        return None, f"instance {opts.instance}"
    if opts.instances and target.name not in opts.instances:
        return None, f"instances {opts.instances}"
    return config, None


def filter_task_request(jobOptions, req):
    configSpec = req.configSpec
    configSpecName = configSpec.name
    configSpec, filterReason = _filter_config(jobOptions, configSpec, req.target)
    if not configSpec:
        logger.debug(
            "skipping configspec '%s' for '%s': doesn't match filter: '%s'",
            configSpecName,
            req.target.name,
            filterReason,
        )
        return None  # treat as filtered step

    return req


def _find_implementation(interface, operation, template):
    default = None
    for iDef in template.get_interfaces():
        if iDef.interfacename == interface or iDef.type == interface:
            if iDef.name == operation:
                return iDef
            if iDef.name == "default":
                default = iDef
    return default


def find_resources_from_template_name(root, name):
    # XXX make faster
    for resource in root.get_self_and_descendents():
        if resource.template.name == name:
            yield resource


def find_parent_template(source):
    for rel, req, reqDef in source.relationships:
        # special case "host" so it can be declared without full set of relationship / capability types
        if rel.is_derived_from("tosca.relationships.HostedOn") or "host" in req:
            return rel.target
    return None


def find_parent_resource(root, source):
    parentTemplate = find_parent_template(source.toscaEntityTemplate)
    if not parentTemplate:
        return root
    for parent in find_resources_from_template_name(root, parentTemplate.name):
        # XXX need to evaluate matches
        return parent
    raise UnfurlError(
        f"could not find parent instance {parentTemplate.name} for child {source.name}"
    )


def create_instance_from_spec(_manifest, target, rname, resourceSpec):
    pname = resourceSpec.get("parent")
    # get the actual parent if pname is a reserved name:
    if pname in [".self", "SELF"]:
        resourceSpec["parent"] = target.name
    elif pname == "HOST":
        resourceSpec["parent"] = target.parent.name if target.parent else "root"

    if isinstance(resourceSpec.get("template"), dict):
        # inline node template, add it to the spec
        tname = resourceSpec["template"].pop("name", rname)
        nodeSpec = _manifest.tosca.add_node_template(tname, resourceSpec["template"])
        resourceSpec["template"] = nodeSpec.name

    if resourceSpec.get("readyState") and "created" not in resourceSpec:
        # setting "created" to the target's key indicates that
        # the target is responsible for deletion
        # if "created" is not defined, set it if readyState is set
        resourceSpec["created"] = target.key

    if "parent" not in resourceSpec and "template" in resourceSpec:
        tname = resourceSpec['template']
        nodeSpec = _manifest.tosca.get_template(tname)
        if not nodeSpec:
            raise UnfurlError(
                f'Can not find template "{tname}" when trying to create instance "{rname}".'
            )
        parent = find_parent_resource(target.root, nodeSpec)
    else:
        parent = target.root
    # note: if resourceSpec[parent] is set it overrides the parent keyword
    return _manifest.create_node_instance(rname, resourceSpec, parent=parent)


def _maybe_mock(iDef, template):
    if not os.getenv("UNFURL_MOCK_DEPLOY"):
        return iDef
    mock = _find_implementation("Mock", iDef.name, template)
    if mock:
        return mock
    # mock operation not found, so patch iDef
    if not isinstance(iDef.implementation, dict):
        # it's a string naming an artifact
        iDef.implementation = dict(primary=iDef.implementation)
    iDef.implementation["className"] = "unfurl.configurator.MockConfigurator"
    return iDef


def create_task_request(
    jobOptions,
    operation,
    resource,
    reason=None,
    inputs=None,
    startState=None,
    operation_host=None,
    skip_filter=False,
):
    """implementation can either be a named artifact (including a python configurator class),
    or a file path"""
    interface, sep, action = operation.rpartition(".")
    iDef = _find_implementation(interface, action, resource.template)
    if iDef and iDef.name != "default":
        iDef = _maybe_mock(iDef, resource.template)
        # merge inputs
        if inputs:
            inputs = dict(iDef.inputs, **inputs)
        else:
            inputs = iDef.inputs or {}
        if iDef.invoke:
            # get the implementation from the operation specified with the "invoke" key
            iinterface, sep, iaction = iDef.invoke.rpartition(".")
            iDef = _find_implementation(iinterface, iaction, resource.template)
            inputs = dict(iDef.inputs, **inputs)

        kw = _get_config_spec_args_from_implementation(
            iDef, inputs, resource, operation_host
        )
    else:
        kw = None

    if kw:
        kw["interface"] = interface
        if reason:
            name = f"for {reason}: {interface}.{action}"
            if reason == jobOptions.workflow:
                # set the task's workflow instead of using the default ("deploy")
                kw["workflow"] = reason
        else:
            name = f"{interface}.{action}"
        configSpec = ConfigurationSpec(name, action, **kw)
        logger.debug(
            "creating configuration %s with %s for %s: %s",
            configSpec.name,
            tuple(f"{n}: {str(v)[:50]}" for n, v in configSpec.inputs.items())
            if configSpec.inputs
            else (),
            resource.name,
            reason or action,
        )
    else:
        errorMsg = f'unable to find an implementation for operation "{action}" on node "{resource.template.name}"'
        logger.trace(errorMsg)
        return None

    req = TaskRequest(
        configSpec,
        resource,
        reason or action,
        startState=startState,
    )
    if skip_filter:
        return req
    else:
        return filter_task_request(jobOptions, req)


def set_default_command(kw, implementation):
    inputs = kw["inputs"]
    if not implementation:
        implementation = inputs.get("cmd")
    # is it a shell script or a command line?
    shell = inputs.get("shell")
    if shell is None:
        # no special shell characters
        shell = not re.match(r"[\w.-]+\Z", implementation)

    operation_host = kw.get("operation_host")
    implementation = implementation.lstrip()
    if not operation_host or operation_host == "localhost":
        className = "unfurl.configurators.shell.ShellConfigurator"
        if shell:
            shellArgs = dict(command=implementation)
        else:
            shellArgs = dict(command=[implementation])
    else:
        className = "unfurl.configurators.ansible.AnsibleConfigurator"
        module = "shell" if shell else "command"
        playbookTask = dict(cmd=implementation)
        cwd = inputs.get("cwd")
        if cwd:
            playbookTask["chdir"] = cwd
        if shell and isinstance(shell, six.string_types):
            playbookTask["executable"] = shell
        shellArgs = dict(playbook=[{module: playbookTask}])

    kw["className"] = className
    if inputs:
        shellArgs.update(inputs)
    kw["inputs"] = shellArgs
    return kw


def _set_config_spec_args(kw, target, base_dir):
    # if no artifact or className, an error
    artifact = kw["primary"]
    className = kw.get("className")
    if not className and not artifact:  # malformed implementation
        logger.warning(
            "no artifact or className set on operation for %s: %s", target.name, kw
        )
        return None
    guessing = False
    if not className:
        className = artifact.properties.get("className")
        if not className:
            className = artifact.file
            guessing = className

    # load the configurator class
    try:
        if "#" in className and len(shlex.split(className)) == 1:
            path, sep, fragment = className.partition("#")
            fullpath = os.path.join(base_dir, path)
            mod = load_module(fullpath)
            klass = getattr(mod, fragment)  # raise if missing
        else:
            klass = lookup_class(className)
    except:
        klass = None
        logger.debug("exception while instantiating %s", className, exc_info=True)

    # invoke configurator classmethod to give configurator a chance to customize configspec (e.g. add dependencies)
    if klass:
        kw["className"] = f"{klass.__module__}.{klass.__name__}"
        return klass.set_config_spec_args(kw, target)
    elif guessing:
        # otherwise assume it's a shell command line
        logger.debug("interpreting 'implementation' as a shell command: %s", guessing)
        return set_default_command(kw, guessing)
    else:
        # error couldn't resolve className
        logger.warning("could not find configurator class: %s", className)
        return None


def _get_config_spec_args_from_implementation(iDef, inputs, target, operation_host):
    implementation = iDef.implementation
    kw = dict(
        inputs=inputs,
        outputs=iDef.outputs,
        operation_host=operation_host,
        entry_state=iDef.entry_state,
    )
    configSpecArgs = ConfigurationSpec.getDefaults()
    artifactTpl = None
    dependencies = None
    predefined = False
    if isinstance(implementation, dict):
        # operation_instance = find_operation_host(
        #     target, implementation.get("operation_host") or operation_host
        # )
        for name, value in implementation.items():
            if name == "primary":
                artifactTpl = value
                predefined = True
            elif name == "dependencies":
                dependencies = value
            elif name in configSpecArgs:
                # sets operation_host, environment, timeout, className
                kw[name] = value
    else:
        # "either because it refers to a named artifact specified in the artifacts section of a type or template,
        # or because it represents the name of a script in the CSAR file that contains the definition."
        artifactTpl = implementation
        # operation_instance = find_operation_host(target, operation_host)

    # if not operation_instance:
    #     operation_instance = operation_instance or target.root
    base_dir = getattr(iDef.value, "base_dir", iDef._source)
    kw["base_dir"] = base_dir
    if artifactTpl:
        artifact = target.template.find_or_create_artifact(
            artifactTpl, base_dir, predefined
        )
    else:
        artifact = None
    kw["primary"] = artifact

    if dependencies:
        kw["dependencies"] = [
            target.template.find_or_create_artifact(artifactTpl, base_dir, True)
            for artifactTpl in dependencies
        ]
    else:
        kw["dependencies"] = []

    return _set_config_spec_args(kw, target, base_dir)
