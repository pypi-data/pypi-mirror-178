'''
# `google_clouddeploy_delivery_pipeline`

Refer to the Terraform Registory for docs: [`google_clouddeploy_delivery_pipeline`](https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf
import constructs


class ClouddeployDeliveryPipeline(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipeline",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline google_clouddeploy_delivery_pipeline}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        serial_pipeline: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipeline", typing.Dict[str, typing.Any]]] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployDeliveryPipelineTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline google_clouddeploy_delivery_pipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#location ClouddeployDeliveryPipeline#location}
        :param name: Name of the ``DeliveryPipeline``. Format is [a-z][a-z0-9-]{0,62}. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#name ClouddeployDeliveryPipeline#name}
        :param annotations: User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#annotations ClouddeployDeliveryPipeline#annotations}
        :param description: Description of the ``DeliveryPipeline``. Max length is 255 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#description ClouddeployDeliveryPipeline#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#id ClouddeployDeliveryPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#labels ClouddeployDeliveryPipeline#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#project ClouddeployDeliveryPipeline#project}
        :param serial_pipeline: serial_pipeline block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#serial_pipeline ClouddeployDeliveryPipeline#serial_pipeline}
        :param suspended: When suspended, no new releases or rollouts can be created, but in-progress ones will complete. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#suspended ClouddeployDeliveryPipeline#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#timeouts ClouddeployDeliveryPipeline#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id_: builtins.str,
                *,
                location: builtins.str,
                name: builtins.str,
                annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                project: typing.Optional[builtins.str] = None,
                serial_pipeline: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipeline, typing.Dict[str, typing.Any]]] = None,
                suspended: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                timeouts: typing.Optional[typing.Union[ClouddeployDeliveryPipelineTimeouts, typing.Dict[str, typing.Any]]] = None,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ClouddeployDeliveryPipelineConfig(
            location=location,
            name=name,
            annotations=annotations,
            description=description,
            id=id,
            labels=labels,
            project=project,
            serial_pipeline=serial_pipeline,
            suspended=suspended,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putSerialPipeline")
    def put_serial_pipeline(
        self,
        *,
        stages: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStages", typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param stages: stages block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#stages ClouddeployDeliveryPipeline#stages}
        '''
        value = ClouddeployDeliveryPipelineSerialPipeline(stages=stages)

        return typing.cast(None, jsii.invoke(self, "putSerialPipeline", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#create ClouddeployDeliveryPipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#delete ClouddeployDeliveryPipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#update ClouddeployDeliveryPipeline#update}.
        '''
        value = ClouddeployDeliveryPipelineTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSerialPipeline")
    def reset_serial_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSerialPipeline", []))

    @jsii.member(jsii_name="resetSuspended")
    def reset_suspended(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspended", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> "ClouddeployDeliveryPipelineConditionList":
        return typing.cast("ClouddeployDeliveryPipelineConditionList", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="serialPipeline")
    def serial_pipeline(
        self,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineOutputReference", jsii.get(self, "serialPipeline"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ClouddeployDeliveryPipelineTimeoutsOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serialPipelineInput")
    def serial_pipeline_input(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipeline"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipeline"], jsii.get(self, "serialPipelineInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendedInput")
    def suspended_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "suspendedInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["ClouddeployDeliveryPipelineTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ClouddeployDeliveryPipelineTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="suspended")
    def suspended(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "suspended"))

    @suspended.setter
    def suspended(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class ClouddeployDeliveryPipelineCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineConditionList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeliveryPipelineConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeliveryPipelineConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ClouddeployDeliveryPipelineConditionOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pipelineReadyCondition")
    def pipeline_ready_condition(
        self,
    ) -> "ClouddeployDeliveryPipelineConditionPipelineReadyConditionList":
        return typing.cast("ClouddeployDeliveryPipelineConditionPipelineReadyConditionList", jsii.get(self, "pipelineReadyCondition"))

    @builtins.property
    @jsii.member(jsii_name="targetsPresentCondition")
    def targets_present_condition(
        self,
    ) -> "ClouddeployDeliveryPipelineConditionTargetsPresentConditionList":
        return typing.cast("ClouddeployDeliveryPipelineConditionTargetsPresentConditionList", jsii.get(self, "targetsPresentCondition"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ClouddeployDeliveryPipelineCondition]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineCondition],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ClouddeployDeliveryPipelineCondition],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionPipelineReadyCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class ClouddeployDeliveryPipelineConditionPipelineReadyCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineConditionPipelineReadyCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineConditionPipelineReadyConditionList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionPipelineReadyConditionList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineConditionPipelineReadyCondition]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineConditionPipelineReadyCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineConditionPipelineReadyCondition],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ClouddeployDeliveryPipelineConditionPipelineReadyCondition],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionTargetsPresentCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class ClouddeployDeliveryPipelineConditionTargetsPresentCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineConditionTargetsPresentCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineConditionTargetsPresentConditionList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionTargetsPresentConditionList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="missingTargets")
    def missing_targets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "missingTargets"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineConditionTargetsPresentCondition]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineConditionTargetsPresentCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineConditionTargetsPresentCondition],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ClouddeployDeliveryPipelineConditionTargetsPresentCondition],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "annotations": "annotations",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "serial_pipeline": "serialPipeline",
        "suspended": "suspended",
        "timeouts": "timeouts",
    },
)
class ClouddeployDeliveryPipelineConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        serial_pipeline: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipeline", typing.Dict[str, typing.Any]]] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployDeliveryPipelineTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#location ClouddeployDeliveryPipeline#location}
        :param name: Name of the ``DeliveryPipeline``. Format is [a-z][a-z0-9-]{0,62}. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#name ClouddeployDeliveryPipeline#name}
        :param annotations: User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#annotations ClouddeployDeliveryPipeline#annotations}
        :param description: Description of the ``DeliveryPipeline``. Max length is 255 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#description ClouddeployDeliveryPipeline#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#id ClouddeployDeliveryPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#labels ClouddeployDeliveryPipeline#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#project ClouddeployDeliveryPipeline#project}
        :param serial_pipeline: serial_pipeline block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#serial_pipeline ClouddeployDeliveryPipeline#serial_pipeline}
        :param suspended: When suspended, no new releases or rollouts can be created, but in-progress ones will complete. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#suspended ClouddeployDeliveryPipeline#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#timeouts ClouddeployDeliveryPipeline#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(serial_pipeline, dict):
            serial_pipeline = ClouddeployDeliveryPipelineSerialPipeline(**serial_pipeline)
        if isinstance(timeouts, dict):
            timeouts = ClouddeployDeliveryPipelineTimeouts(**timeouts)
        if __debug__:
            def stub(
                *,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
                location: builtins.str,
                name: builtins.str,
                annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                project: typing.Optional[builtins.str] = None,
                serial_pipeline: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipeline, typing.Dict[str, typing.Any]]] = None,
                suspended: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                timeouts: typing.Optional[typing.Union[ClouddeployDeliveryPipelineTimeouts, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument serial_pipeline", value=serial_pipeline, expected_type=type_hints["serial_pipeline"])
            check_type(argname="argument suspended", value=suspended, expected_type=type_hints["suspended"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "location": location,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if annotations is not None:
            self._values["annotations"] = annotations
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if serial_pipeline is not None:
            self._values["serial_pipeline"] = serial_pipeline
        if suspended is not None:
            self._values["suspended"] = suspended
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[cdktf.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[cdktf.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#location ClouddeployDeliveryPipeline#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the ``DeliveryPipeline``. Format is [a-z][a-z0-9-]{0,62}.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#name ClouddeployDeliveryPipeline#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User annotations.

        These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#annotations ClouddeployDeliveryPipeline#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the ``DeliveryPipeline``. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#description ClouddeployDeliveryPipeline#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#id ClouddeployDeliveryPipeline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are attributes that can be set and used by both the user and by Google Cloud Deploy.

        Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#labels ClouddeployDeliveryPipeline#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#project ClouddeployDeliveryPipeline#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serial_pipeline(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipeline"]:
        '''serial_pipeline block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#serial_pipeline ClouddeployDeliveryPipeline#serial_pipeline}
        '''
        result = self._values.get("serial_pipeline")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipeline"], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''When suspended, no new releases or rollouts can be created, but in-progress ones will complete.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#suspended ClouddeployDeliveryPipeline#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ClouddeployDeliveryPipelineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#timeouts ClouddeployDeliveryPipeline#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipeline",
    jsii_struct_bases=[],
    name_mapping={"stages": "stages"},
)
class ClouddeployDeliveryPipelineSerialPipeline:
    def __init__(
        self,
        *,
        stages: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStages", typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param stages: stages block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#stages ClouddeployDeliveryPipeline#stages}
        '''
        if __debug__:
            def stub(
                *,
                stages: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStages, typing.Dict[str, typing.Any]]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
        self._values: typing.Dict[str, typing.Any] = {}
        if stages is not None:
            self._values["stages"] = stages

    @builtins.property
    def stages(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStages"]]]:
        '''stages block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#stages ClouddeployDeliveryPipeline#stages}
        '''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStages"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipeline(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStages")
    def put_stages(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStages", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStages, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStages", [value]))

    @jsii.member(jsii_name="resetStages")
    def reset_stages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStages", []))

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> "ClouddeployDeliveryPipelineSerialPipelineStagesList":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesList", jsii.get(self, "stages"))

    @builtins.property
    @jsii.member(jsii_name="stagesInput")
    def stages_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStages"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStages"]]], jsii.get(self, "stagesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipeline]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipeline], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipeline],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ClouddeployDeliveryPipelineSerialPipeline],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStages",
    jsii_struct_bases=[],
    name_mapping={"profiles": "profiles", "target_id": "targetId"},
)
class ClouddeployDeliveryPipelineSerialPipelineStages:
    def __init__(
        self,
        *,
        profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param profiles: Skaffold profiles to use when rendering the manifest for this stage's ``Target``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#profiles ClouddeployDeliveryPipeline#profiles}
        :param target_id: The target_id to which this stage points. This field refers exclusively to the last segment of a target name. For example, this field would just be ``my-target`` (rather than ``projects/project/locations/location/targets/my-target``). The location of the ``Target`` is inferred to be the same as the location of the ``DeliveryPipeline`` that contains this ``Stage``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#target_id ClouddeployDeliveryPipeline#target_id}
        '''
        if __debug__:
            def stub(
                *,
                profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
                target_id: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument profiles", value=profiles, expected_type=type_hints["profiles"])
            check_type(argname="argument target_id", value=target_id, expected_type=type_hints["target_id"])
        self._values: typing.Dict[str, typing.Any] = {}
        if profiles is not None:
            self._values["profiles"] = profiles
        if target_id is not None:
            self._values["target_id"] = target_id

    @builtins.property
    def profiles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Skaffold profiles to use when rendering the manifest for this stage's ``Target``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#profiles ClouddeployDeliveryPipeline#profiles}
        '''
        result = self._values.get("profiles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_id(self) -> typing.Optional[builtins.str]:
        '''The target_id to which this stage points.

        This field refers exclusively to the last segment of a target name. For example, this field would just be ``my-target`` (rather than ``projects/project/locations/location/targets/my-target``). The location of the ``Target`` is inferred to be the same as the location of the ``DeliveryPipeline`` that contains this ``Stage``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#target_id ClouddeployDeliveryPipeline#target_id}
        '''
        result = self._values.get("target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStages]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStages]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStages]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ClouddeployDeliveryPipelineSerialPipelineStagesOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetProfiles")
    def reset_profiles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfiles", []))

    @jsii.member(jsii_name="resetTargetId")
    def reset_target_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetId", []))

    @builtins.property
    @jsii.member(jsii_name="profilesInput")
    def profiles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "profilesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetIdInput")
    def target_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="profiles")
    def profiles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "profiles"))

    @profiles.setter
    def profiles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profiles", value)

    @builtins.property
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetId"))

    @target_id.setter
    def target_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStages, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStages, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStages, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStages, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ClouddeployDeliveryPipelineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#create ClouddeployDeliveryPipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#delete ClouddeployDeliveryPipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#update ClouddeployDeliveryPipeline#update}.
        '''
        if __debug__:
            def stub(
                *,
                create: typing.Optional[builtins.str] = None,
                delete: typing.Optional[builtins.str] = None,
                update: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#create ClouddeployDeliveryPipeline#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#delete ClouddeployDeliveryPipeline#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/clouddeploy_delivery_pipeline#update ClouddeployDeliveryPipeline#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ClouddeployDeliveryPipelineTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ClouddeployDeliveryPipelineTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ClouddeployDeliveryPipelineTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[ClouddeployDeliveryPipelineTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ClouddeployDeliveryPipeline",
    "ClouddeployDeliveryPipelineCondition",
    "ClouddeployDeliveryPipelineConditionList",
    "ClouddeployDeliveryPipelineConditionOutputReference",
    "ClouddeployDeliveryPipelineConditionPipelineReadyCondition",
    "ClouddeployDeliveryPipelineConditionPipelineReadyConditionList",
    "ClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference",
    "ClouddeployDeliveryPipelineConditionTargetsPresentCondition",
    "ClouddeployDeliveryPipelineConditionTargetsPresentConditionList",
    "ClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference",
    "ClouddeployDeliveryPipelineConfig",
    "ClouddeployDeliveryPipelineSerialPipeline",
    "ClouddeployDeliveryPipelineSerialPipelineOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStages",
    "ClouddeployDeliveryPipelineSerialPipelineStagesList",
    "ClouddeployDeliveryPipelineSerialPipelineStagesOutputReference",
    "ClouddeployDeliveryPipelineTimeouts",
    "ClouddeployDeliveryPipelineTimeoutsOutputReference",
]

publication.publish()
