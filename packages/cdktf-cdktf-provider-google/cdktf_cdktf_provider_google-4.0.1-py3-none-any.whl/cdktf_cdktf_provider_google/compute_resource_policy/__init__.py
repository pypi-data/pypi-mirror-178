'''
# `google_compute_resource_policy`

Refer to the Terraform Registory for docs: [`google_compute_resource_policy`](https://www.terraform.io/docs/providers/google/r/compute_resource_policy).
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


class ComputeResourcePolicy(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicy",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy google_compute_resource_policy}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        group_placement_policy: typing.Optional[typing.Union["ComputeResourcePolicyGroupPlacementPolicy", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_schedule_policy: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicy", typing.Dict[str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        snapshot_schedule_policy: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicy", typing.Dict[str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeResourcePolicyTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy google_compute_resource_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the resource, provided by the client when initially creating the resource. The resource name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_'? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#name ComputeResourcePolicy#name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#description ComputeResourcePolicy#description}
        :param group_placement_policy: group_placement_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#group_placement_policy ComputeResourcePolicy#group_placement_policy}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#id ComputeResourcePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_schedule_policy: instance_schedule_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#instance_schedule_policy ComputeResourcePolicy#instance_schedule_policy}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#project ComputeResourcePolicy#project}.
        :param region: Region where resource policy resides. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#region ComputeResourcePolicy#region}
        :param snapshot_schedule_policy: snapshot_schedule_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#snapshot_schedule_policy ComputeResourcePolicy#snapshot_schedule_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#timeouts ComputeResourcePolicy#timeouts}
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
                name: builtins.str,
                description: typing.Optional[builtins.str] = None,
                group_placement_policy: typing.Optional[typing.Union[ComputeResourcePolicyGroupPlacementPolicy, typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                instance_schedule_policy: typing.Optional[typing.Union[ComputeResourcePolicyInstanceSchedulePolicy, typing.Dict[str, typing.Any]]] = None,
                project: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                snapshot_schedule_policy: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicy, typing.Dict[str, typing.Any]]] = None,
                timeouts: typing.Optional[typing.Union[ComputeResourcePolicyTimeouts, typing.Dict[str, typing.Any]]] = None,
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
        config = ComputeResourcePolicyConfig(
            name=name,
            description=description,
            group_placement_policy=group_placement_policy,
            id=id,
            instance_schedule_policy=instance_schedule_policy,
            project=project,
            region=region,
            snapshot_schedule_policy=snapshot_schedule_policy,
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

    @jsii.member(jsii_name="putGroupPlacementPolicy")
    def put_group_placement_policy(
        self,
        *,
        availability_domain_count: typing.Optional[jsii.Number] = None,
        collocation: typing.Optional[builtins.str] = None,
        vm_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability_domain_count: The number of availability domains instances will be spread across. If two instances are in different availability domain, they will not be put in the same low latency network Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#availability_domain_count ComputeResourcePolicy#availability_domain_count}
        :param collocation: Collocation specifies whether to place VMs inside the same availability domain on the same low-latency network. Specify 'COLLOCATED' to enable collocation. Can only be specified with 'vm_count'. If compute instances are created with a COLLOCATED policy, then exactly 'vm_count' instances must be created at the same time with the resource policy attached. Possible values: ["COLLOCATED"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#collocation ComputeResourcePolicy#collocation}
        :param vm_count: Number of VMs in this placement group. Google does not recommend that you use this field unless you use a compact policy and you want your policy to work only if it contains this exact number of VMs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#vm_count ComputeResourcePolicy#vm_count}
        '''
        value = ComputeResourcePolicyGroupPlacementPolicy(
            availability_domain_count=availability_domain_count,
            collocation=collocation,
            vm_count=vm_count,
        )

        return typing.cast(None, jsii.invoke(self, "putGroupPlacementPolicy", [value]))

    @jsii.member(jsii_name="putInstanceSchedulePolicy")
    def put_instance_schedule_policy(
        self,
        *,
        time_zone: builtins.str,
        expiration_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        vm_start_schedule: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule", typing.Dict[str, typing.Any]]] = None,
        vm_stop_schedule: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_zone: Specifies the time zone to be used in interpreting the schedule. The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#time_zone ComputeResourcePolicy#time_zone}
        :param expiration_time: The expiration time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#expiration_time ComputeResourcePolicy#expiration_time}
        :param start_time: The start time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        :param vm_start_schedule: vm_start_schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#vm_start_schedule ComputeResourcePolicy#vm_start_schedule}
        :param vm_stop_schedule: vm_stop_schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#vm_stop_schedule ComputeResourcePolicy#vm_stop_schedule}
        '''
        value = ComputeResourcePolicyInstanceSchedulePolicy(
            time_zone=time_zone,
            expiration_time=expiration_time,
            start_time=start_time,
            vm_start_schedule=vm_start_schedule,
            vm_stop_schedule=vm_stop_schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceSchedulePolicy", [value]))

    @jsii.member(jsii_name="putSnapshotSchedulePolicy")
    def put_snapshot_schedule_policy(
        self,
        *,
        schedule: typing.Union["ComputeResourcePolicySnapshotSchedulePolicySchedule", typing.Dict[str, typing.Any]],
        retention_policy: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy", typing.Dict[str, typing.Any]]] = None,
        snapshot_properties: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#retention_policy ComputeResourcePolicy#retention_policy}
        :param snapshot_properties: snapshot_properties block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#snapshot_properties ComputeResourcePolicy#snapshot_properties}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicy(
            schedule=schedule,
            retention_policy=retention_policy,
            snapshot_properties=snapshot_properties,
        )

        return typing.cast(None, jsii.invoke(self, "putSnapshotSchedulePolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#create ComputeResourcePolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#delete ComputeResourcePolicy#delete}.
        '''
        value = ComputeResourcePolicyTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGroupPlacementPolicy")
    def reset_group_placement_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupPlacementPolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceSchedulePolicy")
    def reset_instance_schedule_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceSchedulePolicy", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSnapshotSchedulePolicy")
    def reset_snapshot_schedule_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotSchedulePolicy", []))

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
    @jsii.member(jsii_name="groupPlacementPolicy")
    def group_placement_policy(
        self,
    ) -> "ComputeResourcePolicyGroupPlacementPolicyOutputReference":
        return typing.cast("ComputeResourcePolicyGroupPlacementPolicyOutputReference", jsii.get(self, "groupPlacementPolicy"))

    @builtins.property
    @jsii.member(jsii_name="instanceSchedulePolicy")
    def instance_schedule_policy(
        self,
    ) -> "ComputeResourcePolicyInstanceSchedulePolicyOutputReference":
        return typing.cast("ComputeResourcePolicyInstanceSchedulePolicyOutputReference", jsii.get(self, "instanceSchedulePolicy"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="snapshotSchedulePolicy")
    def snapshot_schedule_policy(
        self,
    ) -> "ComputeResourcePolicySnapshotSchedulePolicyOutputReference":
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicyOutputReference", jsii.get(self, "snapshotSchedulePolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeResourcePolicyTimeoutsOutputReference":
        return typing.cast("ComputeResourcePolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="groupPlacementPolicyInput")
    def group_placement_policy_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicyGroupPlacementPolicy"]:
        return typing.cast(typing.Optional["ComputeResourcePolicyGroupPlacementPolicy"], jsii.get(self, "groupPlacementPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceSchedulePolicyInput")
    def instance_schedule_policy_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicy"]:
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicy"], jsii.get(self, "instanceSchedulePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotSchedulePolicyInput")
    def snapshot_schedule_policy_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicy"]:
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicy"], jsii.get(self, "snapshotSchedulePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["ComputeResourcePolicyTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ComputeResourcePolicyTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

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
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "description": "description",
        "group_placement_policy": "groupPlacementPolicy",
        "id": "id",
        "instance_schedule_policy": "instanceSchedulePolicy",
        "project": "project",
        "region": "region",
        "snapshot_schedule_policy": "snapshotSchedulePolicy",
        "timeouts": "timeouts",
    },
)
class ComputeResourcePolicyConfig(cdktf.TerraformMetaArguments):
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
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        group_placement_policy: typing.Optional[typing.Union["ComputeResourcePolicyGroupPlacementPolicy", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_schedule_policy: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicy", typing.Dict[str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        snapshot_schedule_policy: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicy", typing.Dict[str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeResourcePolicyTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the resource, provided by the client when initially creating the resource. The resource name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_'? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#name ComputeResourcePolicy#name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#description ComputeResourcePolicy#description}
        :param group_placement_policy: group_placement_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#group_placement_policy ComputeResourcePolicy#group_placement_policy}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#id ComputeResourcePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_schedule_policy: instance_schedule_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#instance_schedule_policy ComputeResourcePolicy#instance_schedule_policy}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#project ComputeResourcePolicy#project}.
        :param region: Region where resource policy resides. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#region ComputeResourcePolicy#region}
        :param snapshot_schedule_policy: snapshot_schedule_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#snapshot_schedule_policy ComputeResourcePolicy#snapshot_schedule_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#timeouts ComputeResourcePolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(group_placement_policy, dict):
            group_placement_policy = ComputeResourcePolicyGroupPlacementPolicy(**group_placement_policy)
        if isinstance(instance_schedule_policy, dict):
            instance_schedule_policy = ComputeResourcePolicyInstanceSchedulePolicy(**instance_schedule_policy)
        if isinstance(snapshot_schedule_policy, dict):
            snapshot_schedule_policy = ComputeResourcePolicySnapshotSchedulePolicy(**snapshot_schedule_policy)
        if isinstance(timeouts, dict):
            timeouts = ComputeResourcePolicyTimeouts(**timeouts)
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
                name: builtins.str,
                description: typing.Optional[builtins.str] = None,
                group_placement_policy: typing.Optional[typing.Union[ComputeResourcePolicyGroupPlacementPolicy, typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                instance_schedule_policy: typing.Optional[typing.Union[ComputeResourcePolicyInstanceSchedulePolicy, typing.Dict[str, typing.Any]]] = None,
                project: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                snapshot_schedule_policy: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicy, typing.Dict[str, typing.Any]]] = None,
                timeouts: typing.Optional[typing.Union[ComputeResourcePolicyTimeouts, typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument group_placement_policy", value=group_placement_policy, expected_type=type_hints["group_placement_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_schedule_policy", value=instance_schedule_policy, expected_type=type_hints["instance_schedule_policy"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument snapshot_schedule_policy", value=snapshot_schedule_policy, expected_type=type_hints["snapshot_schedule_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
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
        if description is not None:
            self._values["description"] = description
        if group_placement_policy is not None:
            self._values["group_placement_policy"] = group_placement_policy
        if id is not None:
            self._values["id"] = id
        if instance_schedule_policy is not None:
            self._values["instance_schedule_policy"] = instance_schedule_policy
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if snapshot_schedule_policy is not None:
            self._values["snapshot_schedule_policy"] = snapshot_schedule_policy
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
    def name(self) -> builtins.str:
        '''The name of the resource, provided by the client when initially creating the resource.

        The resource name must be 1-63 characters long, and comply
        with RFC1035. Specifically, the name must be 1-63 characters long and
        match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_'? which means the
        first character must be a lowercase letter, and all following characters
        must be a dash, lowercase letter, or digit, except the last character,
        which cannot be a dash.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#name ComputeResourcePolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#description ComputeResourcePolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_placement_policy(
        self,
    ) -> typing.Optional["ComputeResourcePolicyGroupPlacementPolicy"]:
        '''group_placement_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#group_placement_policy ComputeResourcePolicy#group_placement_policy}
        '''
        result = self._values.get("group_placement_policy")
        return typing.cast(typing.Optional["ComputeResourcePolicyGroupPlacementPolicy"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#id ComputeResourcePolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_schedule_policy(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicy"]:
        '''instance_schedule_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#instance_schedule_policy ComputeResourcePolicy#instance_schedule_policy}
        '''
        result = self._values.get("instance_schedule_policy")
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicy"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#project ComputeResourcePolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where resource policy resides.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#region ComputeResourcePolicy#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_schedule_policy(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicy"]:
        '''snapshot_schedule_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#snapshot_schedule_policy ComputeResourcePolicy#snapshot_schedule_policy}
        '''
        result = self._values.get("snapshot_schedule_policy")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeResourcePolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#timeouts ComputeResourcePolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeResourcePolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyGroupPlacementPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "availability_domain_count": "availabilityDomainCount",
        "collocation": "collocation",
        "vm_count": "vmCount",
    },
)
class ComputeResourcePolicyGroupPlacementPolicy:
    def __init__(
        self,
        *,
        availability_domain_count: typing.Optional[jsii.Number] = None,
        collocation: typing.Optional[builtins.str] = None,
        vm_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability_domain_count: The number of availability domains instances will be spread across. If two instances are in different availability domain, they will not be put in the same low latency network Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#availability_domain_count ComputeResourcePolicy#availability_domain_count}
        :param collocation: Collocation specifies whether to place VMs inside the same availability domain on the same low-latency network. Specify 'COLLOCATED' to enable collocation. Can only be specified with 'vm_count'. If compute instances are created with a COLLOCATED policy, then exactly 'vm_count' instances must be created at the same time with the resource policy attached. Possible values: ["COLLOCATED"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#collocation ComputeResourcePolicy#collocation}
        :param vm_count: Number of VMs in this placement group. Google does not recommend that you use this field unless you use a compact policy and you want your policy to work only if it contains this exact number of VMs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#vm_count ComputeResourcePolicy#vm_count}
        '''
        if __debug__:
            def stub(
                *,
                availability_domain_count: typing.Optional[jsii.Number] = None,
                collocation: typing.Optional[builtins.str] = None,
                vm_count: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument availability_domain_count", value=availability_domain_count, expected_type=type_hints["availability_domain_count"])
            check_type(argname="argument collocation", value=collocation, expected_type=type_hints["collocation"])
            check_type(argname="argument vm_count", value=vm_count, expected_type=type_hints["vm_count"])
        self._values: typing.Dict[str, typing.Any] = {}
        if availability_domain_count is not None:
            self._values["availability_domain_count"] = availability_domain_count
        if collocation is not None:
            self._values["collocation"] = collocation
        if vm_count is not None:
            self._values["vm_count"] = vm_count

    @builtins.property
    def availability_domain_count(self) -> typing.Optional[jsii.Number]:
        '''The number of availability domains instances will be spread across.

        If two instances are in different
        availability domain, they will not be put in the same low latency network

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#availability_domain_count ComputeResourcePolicy#availability_domain_count}
        '''
        result = self._values.get("availability_domain_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def collocation(self) -> typing.Optional[builtins.str]:
        '''Collocation specifies whether to place VMs inside the same availability domain on the same low-latency network.

        Specify 'COLLOCATED' to enable collocation. Can only be specified with 'vm_count'. If compute instances are created
        with a COLLOCATED policy, then exactly 'vm_count' instances must be created at the same time with the resource policy
        attached. Possible values: ["COLLOCATED"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#collocation ComputeResourcePolicy#collocation}
        '''
        result = self._values.get("collocation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_count(self) -> typing.Optional[jsii.Number]:
        '''Number of VMs in this placement group.

        Google does not recommend that you use this field
        unless you use a compact policy and you want your policy to work only if it contains this
        exact number of VMs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#vm_count ComputeResourcePolicy#vm_count}
        '''
        result = self._values.get("vm_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyGroupPlacementPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyGroupPlacementPolicyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyGroupPlacementPolicyOutputReference",
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

    @jsii.member(jsii_name="resetAvailabilityDomainCount")
    def reset_availability_domain_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityDomainCount", []))

    @jsii.member(jsii_name="resetCollocation")
    def reset_collocation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollocation", []))

    @jsii.member(jsii_name="resetVmCount")
    def reset_vm_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmCount", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityDomainCountInput")
    def availability_domain_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "availabilityDomainCountInput"))

    @builtins.property
    @jsii.member(jsii_name="collocationInput")
    def collocation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collocationInput"))

    @builtins.property
    @jsii.member(jsii_name="vmCountInput")
    def vm_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmCountInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityDomainCount")
    def availability_domain_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availabilityDomainCount"))

    @availability_domain_count.setter
    def availability_domain_count(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityDomainCount", value)

    @builtins.property
    @jsii.member(jsii_name="collocation")
    def collocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collocation"))

    @collocation.setter
    def collocation(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collocation", value)

    @builtins.property
    @jsii.member(jsii_name="vmCount")
    def vm_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmCount"))

    @vm_count.setter
    def vm_count(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicyGroupPlacementPolicy]:
        return typing.cast(typing.Optional[ComputeResourcePolicyGroupPlacementPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicyGroupPlacementPolicy],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeResourcePolicyGroupPlacementPolicy],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "time_zone": "timeZone",
        "expiration_time": "expirationTime",
        "start_time": "startTime",
        "vm_start_schedule": "vmStartSchedule",
        "vm_stop_schedule": "vmStopSchedule",
    },
)
class ComputeResourcePolicyInstanceSchedulePolicy:
    def __init__(
        self,
        *,
        time_zone: builtins.str,
        expiration_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        vm_start_schedule: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule", typing.Dict[str, typing.Any]]] = None,
        vm_stop_schedule: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_zone: Specifies the time zone to be used in interpreting the schedule. The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#time_zone ComputeResourcePolicy#time_zone}
        :param expiration_time: The expiration time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#expiration_time ComputeResourcePolicy#expiration_time}
        :param start_time: The start time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        :param vm_start_schedule: vm_start_schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#vm_start_schedule ComputeResourcePolicy#vm_start_schedule}
        :param vm_stop_schedule: vm_stop_schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#vm_stop_schedule ComputeResourcePolicy#vm_stop_schedule}
        '''
        if isinstance(vm_start_schedule, dict):
            vm_start_schedule = ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule(**vm_start_schedule)
        if isinstance(vm_stop_schedule, dict):
            vm_stop_schedule = ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule(**vm_stop_schedule)
        if __debug__:
            def stub(
                *,
                time_zone: builtins.str,
                expiration_time: typing.Optional[builtins.str] = None,
                start_time: typing.Optional[builtins.str] = None,
                vm_start_schedule: typing.Optional[typing.Union[ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule, typing.Dict[str, typing.Any]]] = None,
                vm_stop_schedule: typing.Optional[typing.Union[ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument expiration_time", value=expiration_time, expected_type=type_hints["expiration_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument vm_start_schedule", value=vm_start_schedule, expected_type=type_hints["vm_start_schedule"])
            check_type(argname="argument vm_stop_schedule", value=vm_stop_schedule, expected_type=type_hints["vm_stop_schedule"])
        self._values: typing.Dict[str, typing.Any] = {
            "time_zone": time_zone,
        }
        if expiration_time is not None:
            self._values["expiration_time"] = expiration_time
        if start_time is not None:
            self._values["start_time"] = start_time
        if vm_start_schedule is not None:
            self._values["vm_start_schedule"] = vm_start_schedule
        if vm_stop_schedule is not None:
            self._values["vm_stop_schedule"] = vm_stop_schedule

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''Specifies the time zone to be used in interpreting the schedule.

        The value of this field must be a time zone name
        from the tz database: http://en.wikipedia.org/wiki/Tz_database.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#time_zone ComputeResourcePolicy#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_time(self) -> typing.Optional[builtins.str]:
        '''The expiration time of the schedule. The timestamp is an RFC3339 string.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#expiration_time ComputeResourcePolicy#expiration_time}
        '''
        result = self._values.get("expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The start time of the schedule. The timestamp is an RFC3339 string.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_start_schedule(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"]:
        '''vm_start_schedule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#vm_start_schedule ComputeResourcePolicy#vm_start_schedule}
        '''
        result = self._values.get("vm_start_schedule")
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"], result)

    @builtins.property
    def vm_stop_schedule(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"]:
        '''vm_stop_schedule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#vm_stop_schedule ComputeResourcePolicy#vm_stop_schedule}
        '''
        result = self._values.get("vm_stop_schedule")
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyInstanceSchedulePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyInstanceSchedulePolicyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicyOutputReference",
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

    @jsii.member(jsii_name="putVmStartSchedule")
    def put_vm_start_schedule(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        value = ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule(
            schedule=schedule
        )

        return typing.cast(None, jsii.invoke(self, "putVmStartSchedule", [value]))

    @jsii.member(jsii_name="putVmStopSchedule")
    def put_vm_stop_schedule(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        value = ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule(
            schedule=schedule
        )

        return typing.cast(None, jsii.invoke(self, "putVmStopSchedule", [value]))

    @jsii.member(jsii_name="resetExpirationTime")
    def reset_expiration_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetVmStartSchedule")
    def reset_vm_start_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmStartSchedule", []))

    @jsii.member(jsii_name="resetVmStopSchedule")
    def reset_vm_stop_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmStopSchedule", []))

    @builtins.property
    @jsii.member(jsii_name="vmStartSchedule")
    def vm_start_schedule(
        self,
    ) -> "ComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference":
        return typing.cast("ComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference", jsii.get(self, "vmStartSchedule"))

    @builtins.property
    @jsii.member(jsii_name="vmStopSchedule")
    def vm_stop_schedule(
        self,
    ) -> "ComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference":
        return typing.cast("ComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference", jsii.get(self, "vmStopSchedule"))

    @builtins.property
    @jsii.member(jsii_name="expirationTimeInput")
    def expiration_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="vmStartScheduleInput")
    def vm_start_schedule_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"]:
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"], jsii.get(self, "vmStartScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="vmStopScheduleInput")
    def vm_stop_schedule_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"]:
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"], jsii.get(self, "vmStopScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationTime")
    def expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationTime"))

    @expiration_time.setter
    def expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationTime", value)

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value)

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicyInstanceSchedulePolicy]:
        return typing.cast(typing.Optional[ComputeResourcePolicyInstanceSchedulePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicy],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicy],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule"},
)
class ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule:
    def __init__(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        if __debug__:
            def stub(*, schedule: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[str, typing.Any] = {
            "schedule": schedule,
        }

    @builtins.property
    def schedule(self) -> builtins.str:
        '''Specifies the frequency for the operation, using the unix-cron format.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule"},
)
class ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule:
    def __init__(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        if __debug__:
            def stub(*, schedule: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[str, typing.Any] = {
            "schedule": schedule,
        }

    @builtins.property
    def schedule(self) -> builtins.str:
        '''Specifies the frequency for the operation, using the unix-cron format.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "schedule": "schedule",
        "retention_policy": "retentionPolicy",
        "snapshot_properties": "snapshotProperties",
    },
)
class ComputeResourcePolicySnapshotSchedulePolicy:
    def __init__(
        self,
        *,
        schedule: typing.Union["ComputeResourcePolicySnapshotSchedulePolicySchedule", typing.Dict[str, typing.Any]],
        retention_policy: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy", typing.Dict[str, typing.Any]]] = None,
        snapshot_properties: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#retention_policy ComputeResourcePolicy#retention_policy}
        :param snapshot_properties: snapshot_properties block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#snapshot_properties ComputeResourcePolicy#snapshot_properties}
        '''
        if isinstance(schedule, dict):
            schedule = ComputeResourcePolicySnapshotSchedulePolicySchedule(**schedule)
        if isinstance(retention_policy, dict):
            retention_policy = ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy(**retention_policy)
        if isinstance(snapshot_properties, dict):
            snapshot_properties = ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties(**snapshot_properties)
        if __debug__:
            def stub(
                *,
                schedule: typing.Union[ComputeResourcePolicySnapshotSchedulePolicySchedule, typing.Dict[str, typing.Any]],
                retention_policy: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy, typing.Dict[str, typing.Any]]] = None,
                snapshot_properties: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument snapshot_properties", value=snapshot_properties, expected_type=type_hints["snapshot_properties"])
        self._values: typing.Dict[str, typing.Any] = {
            "schedule": schedule,
        }
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy
        if snapshot_properties is not None:
            self._values["snapshot_properties"] = snapshot_properties

    @builtins.property
    def schedule(self) -> "ComputeResourcePolicySnapshotSchedulePolicySchedule":
        '''schedule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicySchedule", result)

    @builtins.property
    def retention_policy(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"]:
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#retention_policy ComputeResourcePolicy#retention_policy}
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"], result)

    @builtins.property
    def snapshot_properties(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"]:
        '''snapshot_properties block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#snapshot_properties ComputeResourcePolicy#snapshot_properties}
        '''
        result = self._values.get("snapshot_properties")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyOutputReference",
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

    @jsii.member(jsii_name="putRetentionPolicy")
    def put_retention_policy(
        self,
        *,
        max_retention_days: jsii.Number,
        on_source_disk_delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_retention_days: Maximum age of the snapshot that is allowed to be kept. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#max_retention_days ComputeResourcePolicy#max_retention_days}
        :param on_source_disk_delete: Specifies the behavior to apply to scheduled snapshots when the source disk is deleted. Default value: "KEEP_AUTO_SNAPSHOTS" Possible values: ["KEEP_AUTO_SNAPSHOTS", "APPLY_RETENTION_POLICY"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#on_source_disk_delete ComputeResourcePolicy#on_source_disk_delete}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy(
            max_retention_days=max_retention_days,
            on_source_disk_delete=on_source_disk_delete,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionPolicy", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule", typing.Dict[str, typing.Any]]] = None,
        hourly_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule", typing.Dict[str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#daily_schedule ComputeResourcePolicy#daily_schedule}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#hourly_schedule ComputeResourcePolicy#hourly_schedule}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#weekly_schedule ComputeResourcePolicy#weekly_schedule}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicySchedule(
            daily_schedule=daily_schedule,
            hourly_schedule=hourly_schedule,
            weekly_schedule=weekly_schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="putSnapshotProperties")
    def put_snapshot_properties(
        self,
        *,
        chain_name: typing.Optional[builtins.str] = None,
        guest_flush: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param chain_name: Creates the new snapshot in the snapshot chain labeled with the specified name. The chain name must be 1-63 characters long and comply with RFC1035. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#chain_name ComputeResourcePolicy#chain_name}
        :param guest_flush: Whether to perform a 'guest aware' snapshot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#guest_flush ComputeResourcePolicy#guest_flush}
        :param labels: A set of key-value pairs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#labels ComputeResourcePolicy#labels}
        :param storage_locations: Cloud Storage bucket location to store the auto snapshot (regional or multi-regional). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#storage_locations ComputeResourcePolicy#storage_locations}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties(
            chain_name=chain_name,
            guest_flush=guest_flush,
            labels=labels,
            storage_locations=storage_locations,
        )

        return typing.cast(None, jsii.invoke(self, "putSnapshotProperties", [value]))

    @jsii.member(jsii_name="resetRetentionPolicy")
    def reset_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicy", []))

    @jsii.member(jsii_name="resetSnapshotProperties")
    def reset_snapshot_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotProperties", []))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(
        self,
    ) -> "ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference":
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "ComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference":
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="snapshotProperties")
    def snapshot_properties(
        self,
    ) -> "ComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference":
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference", jsii.get(self, "snapshotProperties"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"]:
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySchedule"]:
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotPropertiesInput")
    def snapshot_properties_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"]:
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"], jsii.get(self, "snapshotPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicy]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicy],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicy],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_retention_days": "maxRetentionDays",
        "on_source_disk_delete": "onSourceDiskDelete",
    },
)
class ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy:
    def __init__(
        self,
        *,
        max_retention_days: jsii.Number,
        on_source_disk_delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_retention_days: Maximum age of the snapshot that is allowed to be kept. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#max_retention_days ComputeResourcePolicy#max_retention_days}
        :param on_source_disk_delete: Specifies the behavior to apply to scheduled snapshots when the source disk is deleted. Default value: "KEEP_AUTO_SNAPSHOTS" Possible values: ["KEEP_AUTO_SNAPSHOTS", "APPLY_RETENTION_POLICY"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#on_source_disk_delete ComputeResourcePolicy#on_source_disk_delete}
        '''
        if __debug__:
            def stub(
                *,
                max_retention_days: jsii.Number,
                on_source_disk_delete: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument max_retention_days", value=max_retention_days, expected_type=type_hints["max_retention_days"])
            check_type(argname="argument on_source_disk_delete", value=on_source_disk_delete, expected_type=type_hints["on_source_disk_delete"])
        self._values: typing.Dict[str, typing.Any] = {
            "max_retention_days": max_retention_days,
        }
        if on_source_disk_delete is not None:
            self._values["on_source_disk_delete"] = on_source_disk_delete

    @builtins.property
    def max_retention_days(self) -> jsii.Number:
        '''Maximum age of the snapshot that is allowed to be kept.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#max_retention_days ComputeResourcePolicy#max_retention_days}
        '''
        result = self._values.get("max_retention_days")
        assert result is not None, "Required property 'max_retention_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def on_source_disk_delete(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior to apply to scheduled snapshots when the source disk is deleted.

        Default value: "KEEP_AUTO_SNAPSHOTS" Possible values: ["KEEP_AUTO_SNAPSHOTS", "APPLY_RETENTION_POLICY"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#on_source_disk_delete ComputeResourcePolicy#on_source_disk_delete}
        '''
        result = self._values.get("on_source_disk_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference",
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

    @jsii.member(jsii_name="resetOnSourceDiskDelete")
    def reset_on_source_disk_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnSourceDiskDelete", []))

    @builtins.property
    @jsii.member(jsii_name="maxRetentionDaysInput")
    def max_retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="onSourceDiskDeleteInput")
    def on_source_disk_delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onSourceDiskDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetentionDays")
    def max_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetentionDays"))

    @max_retention_days.setter
    def max_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetentionDays", value)

    @builtins.property
    @jsii.member(jsii_name="onSourceDiskDelete")
    def on_source_disk_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onSourceDiskDelete"))

    @on_source_disk_delete.setter
    def on_source_disk_delete(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onSourceDiskDelete", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "daily_schedule": "dailySchedule",
        "hourly_schedule": "hourlySchedule",
        "weekly_schedule": "weeklySchedule",
    },
)
class ComputeResourcePolicySnapshotSchedulePolicySchedule:
    def __init__(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule", typing.Dict[str, typing.Any]]] = None,
        hourly_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule", typing.Dict[str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#daily_schedule ComputeResourcePolicy#daily_schedule}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#hourly_schedule ComputeResourcePolicy#hourly_schedule}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#weekly_schedule ComputeResourcePolicy#weekly_schedule}
        '''
        if isinstance(daily_schedule, dict):
            daily_schedule = ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule(**daily_schedule)
        if isinstance(hourly_schedule, dict):
            hourly_schedule = ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule(**hourly_schedule)
        if isinstance(weekly_schedule, dict):
            weekly_schedule = ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule(**weekly_schedule)
        if __debug__:
            def stub(
                *,
                daily_schedule: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule, typing.Dict[str, typing.Any]]] = None,
                hourly_schedule: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule, typing.Dict[str, typing.Any]]] = None,
                weekly_schedule: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument daily_schedule", value=daily_schedule, expected_type=type_hints["daily_schedule"])
            check_type(argname="argument hourly_schedule", value=hourly_schedule, expected_type=type_hints["hourly_schedule"])
            check_type(argname="argument weekly_schedule", value=weekly_schedule, expected_type=type_hints["weekly_schedule"])
        self._values: typing.Dict[str, typing.Any] = {}
        if daily_schedule is not None:
            self._values["daily_schedule"] = daily_schedule
        if hourly_schedule is not None:
            self._values["hourly_schedule"] = hourly_schedule
        if weekly_schedule is not None:
            self._values["weekly_schedule"] = weekly_schedule

    @builtins.property
    def daily_schedule(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule"]:
        '''daily_schedule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#daily_schedule ComputeResourcePolicy#daily_schedule}
        '''
        result = self._values.get("daily_schedule")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule"], result)

    @builtins.property
    def hourly_schedule(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule"]:
        '''hourly_schedule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#hourly_schedule ComputeResourcePolicy#hourly_schedule}
        '''
        result = self._values.get("hourly_schedule")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule"], result)

    @builtins.property
    def weekly_schedule(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"]:
        '''weekly_schedule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#weekly_schedule ComputeResourcePolicy#weekly_schedule}
        '''
        result = self._values.get("weekly_schedule")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule",
    jsii_struct_bases=[],
    name_mapping={"days_in_cycle": "daysInCycle", "start_time": "startTime"},
)
class ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule:
    def __init__(self, *, days_in_cycle: jsii.Number, start_time: builtins.str) -> None:
        '''
        :param days_in_cycle: The number of days between snapshots. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#days_in_cycle ComputeResourcePolicy#days_in_cycle}
        :param start_time: This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00. For example, both 13:00-5 and 08:00 are valid. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        if __debug__:
            def stub(*, days_in_cycle: jsii.Number, start_time: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument days_in_cycle", value=days_in_cycle, expected_type=type_hints["days_in_cycle"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[str, typing.Any] = {
            "days_in_cycle": days_in_cycle,
            "start_time": start_time,
        }

    @builtins.property
    def days_in_cycle(self) -> jsii.Number:
        '''The number of days between snapshots.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#days_in_cycle ComputeResourcePolicy#days_in_cycle}
        '''
        result = self._values.get("days_in_cycle")
        assert result is not None, "Required property 'days_in_cycle' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00.

        For example,
        both 13:00-5 and 08:00 are valid.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="daysInCycleInput")
    def days_in_cycle_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInCycleInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="daysInCycle")
    def days_in_cycle(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "daysInCycle"))

    @days_in_cycle.setter
    def days_in_cycle(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysInCycle", value)

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule",
    jsii_struct_bases=[],
    name_mapping={"hours_in_cycle": "hoursInCycle", "start_time": "startTime"},
)
class ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule:
    def __init__(
        self,
        *,
        hours_in_cycle: jsii.Number,
        start_time: builtins.str,
    ) -> None:
        '''
        :param hours_in_cycle: The number of hours between snapshots. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#hours_in_cycle ComputeResourcePolicy#hours_in_cycle}
        :param start_time: Time within the window to start the operations. It must be in an hourly format "HH:MM", where HH : [00-23] and MM : [00] GMT. eg: 21:00 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        if __debug__:
            def stub(*, hours_in_cycle: jsii.Number, start_time: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument hours_in_cycle", value=hours_in_cycle, expected_type=type_hints["hours_in_cycle"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[str, typing.Any] = {
            "hours_in_cycle": hours_in_cycle,
            "start_time": start_time,
        }

    @builtins.property
    def hours_in_cycle(self) -> jsii.Number:
        '''The number of hours between snapshots.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#hours_in_cycle ComputeResourcePolicy#hours_in_cycle}
        '''
        result = self._values.get("hours_in_cycle")
        assert result is not None, "Required property 'hours_in_cycle' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Time within the window to start the operations.

        It must be in an hourly format "HH:MM",
        where HH : [00-23] and MM : [00] GMT.
        eg: 21:00

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="hoursInCycleInput")
    def hours_in_cycle_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInCycleInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="hoursInCycle")
    def hours_in_cycle(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hoursInCycle"))

    @hours_in_cycle.setter
    def hours_in_cycle(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hoursInCycle", value)

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference",
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

    @jsii.member(jsii_name="putDailySchedule")
    def put_daily_schedule(
        self,
        *,
        days_in_cycle: jsii.Number,
        start_time: builtins.str,
    ) -> None:
        '''
        :param days_in_cycle: The number of days between snapshots. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#days_in_cycle ComputeResourcePolicy#days_in_cycle}
        :param start_time: This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00. For example, both 13:00-5 and 08:00 are valid. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule(
            days_in_cycle=days_in_cycle, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putDailySchedule", [value]))

    @jsii.member(jsii_name="putHourlySchedule")
    def put_hourly_schedule(
        self,
        *,
        hours_in_cycle: jsii.Number,
        start_time: builtins.str,
    ) -> None:
        '''
        :param hours_in_cycle: The number of hours between snapshots. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#hours_in_cycle ComputeResourcePolicy#hours_in_cycle}
        :param start_time: Time within the window to start the operations. It must be in an hourly format "HH:MM", where HH : [00-23] and MM : [00] GMT. eg: 21:00 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule(
            hours_in_cycle=hours_in_cycle, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putHourlySchedule", [value]))

    @jsii.member(jsii_name="putWeeklySchedule")
    def put_weekly_schedule(
        self,
        *,
        day_of_weeks: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param day_of_weeks: day_of_weeks block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#day_of_weeks ComputeResourcePolicy#day_of_weeks}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule(
            day_of_weeks=day_of_weeks
        )

        return typing.cast(None, jsii.invoke(self, "putWeeklySchedule", [value]))

    @jsii.member(jsii_name="resetDailySchedule")
    def reset_daily_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailySchedule", []))

    @jsii.member(jsii_name="resetHourlySchedule")
    def reset_hourly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourlySchedule", []))

    @jsii.member(jsii_name="resetWeeklySchedule")
    def reset_weekly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklySchedule", []))

    @builtins.property
    @jsii.member(jsii_name="dailySchedule")
    def daily_schedule(
        self,
    ) -> ComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference:
        return typing.cast(ComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference, jsii.get(self, "dailySchedule"))

    @builtins.property
    @jsii.member(jsii_name="hourlySchedule")
    def hourly_schedule(
        self,
    ) -> ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference:
        return typing.cast(ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference, jsii.get(self, "hourlySchedule"))

    @builtins.property
    @jsii.member(jsii_name="weeklySchedule")
    def weekly_schedule(
        self,
    ) -> "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference":
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference", jsii.get(self, "weeklySchedule"))

    @builtins.property
    @jsii.member(jsii_name="dailyScheduleInput")
    def daily_schedule_input(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule], jsii.get(self, "dailyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="hourlyScheduleInput")
    def hourly_schedule_input(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule], jsii.get(self, "hourlyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyScheduleInput")
    def weekly_schedule_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"]:
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"], jsii.get(self, "weeklyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySchedule],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySchedule],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule",
    jsii_struct_bases=[],
    name_mapping={"day_of_weeks": "dayOfWeeks"},
)
class ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule:
    def __init__(
        self,
        *,
        day_of_weeks: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param day_of_weeks: day_of_weeks block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#day_of_weeks ComputeResourcePolicy#day_of_weeks}
        '''
        if __debug__:
            def stub(
                *,
                day_of_weeks: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument day_of_weeks", value=day_of_weeks, expected_type=type_hints["day_of_weeks"])
        self._values: typing.Dict[str, typing.Any] = {
            "day_of_weeks": day_of_weeks,
        }

    @builtins.property
    def day_of_weeks(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks"]]:
        '''day_of_weeks block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#day_of_weeks ComputeResourcePolicy#day_of_weeks}
        '''
        result = self._values.get("day_of_weeks")
        assert result is not None, "Required property 'day_of_weeks' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "start_time": "startTime"},
)
class ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks:
    def __init__(self, *, day: builtins.str, start_time: builtins.str) -> None:
        '''
        :param day: The day of the week to create the snapshot. e.g. MONDAY Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#day ComputeResourcePolicy#day}
        :param start_time: Time within the window to start the operations. It must be in format "HH:MM", where HH : [00-23] and MM : [00-00] GMT. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        if __debug__:
            def stub(*, day: builtins.str, start_time: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[str, typing.Any] = {
            "day": day,
            "start_time": start_time,
        }

    @builtins.property
    def day(self) -> builtins.str:
        '''The day of the week to create the snapshot.

        e.g. MONDAY Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#day ComputeResourcePolicy#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Time within the window to start the operations.

        It must be in format "HH:MM", where HH : [00-23] and MM : [00-00] GMT.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList",
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
    ) -> "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference",
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
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value)

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference",
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

    @jsii.member(jsii_name="putDayOfWeeks")
    def put_day_of_weeks(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDayOfWeeks", [value]))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeeks")
    def day_of_weeks(
        self,
    ) -> ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList:
        return typing.cast(ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList, jsii.get(self, "dayOfWeeks"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeeksInput")
    def day_of_weeks_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]], jsii.get(self, "dayOfWeeksInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties",
    jsii_struct_bases=[],
    name_mapping={
        "chain_name": "chainName",
        "guest_flush": "guestFlush",
        "labels": "labels",
        "storage_locations": "storageLocations",
    },
)
class ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties:
    def __init__(
        self,
        *,
        chain_name: typing.Optional[builtins.str] = None,
        guest_flush: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param chain_name: Creates the new snapshot in the snapshot chain labeled with the specified name. The chain name must be 1-63 characters long and comply with RFC1035. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#chain_name ComputeResourcePolicy#chain_name}
        :param guest_flush: Whether to perform a 'guest aware' snapshot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#guest_flush ComputeResourcePolicy#guest_flush}
        :param labels: A set of key-value pairs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#labels ComputeResourcePolicy#labels}
        :param storage_locations: Cloud Storage bucket location to store the auto snapshot (regional or multi-regional). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#storage_locations ComputeResourcePolicy#storage_locations}
        '''
        if __debug__:
            def stub(
                *,
                chain_name: typing.Optional[builtins.str] = None,
                guest_flush: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument chain_name", value=chain_name, expected_type=type_hints["chain_name"])
            check_type(argname="argument guest_flush", value=guest_flush, expected_type=type_hints["guest_flush"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument storage_locations", value=storage_locations, expected_type=type_hints["storage_locations"])
        self._values: typing.Dict[str, typing.Any] = {}
        if chain_name is not None:
            self._values["chain_name"] = chain_name
        if guest_flush is not None:
            self._values["guest_flush"] = guest_flush
        if labels is not None:
            self._values["labels"] = labels
        if storage_locations is not None:
            self._values["storage_locations"] = storage_locations

    @builtins.property
    def chain_name(self) -> typing.Optional[builtins.str]:
        '''Creates the new snapshot in the snapshot chain labeled with the  specified name.

        The chain name must be 1-63 characters long and comply
        with RFC1035.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#chain_name ComputeResourcePolicy#chain_name}
        '''
        result = self._values.get("chain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_flush(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Whether to perform a 'guest aware' snapshot.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#guest_flush ComputeResourcePolicy#guest_flush}
        '''
        result = self._values.get("guest_flush")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key-value pairs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#labels ComputeResourcePolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def storage_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cloud Storage bucket location to store the auto snapshot (regional or multi-regional).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#storage_locations ComputeResourcePolicy#storage_locations}
        '''
        result = self._values.get("storage_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference",
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

    @jsii.member(jsii_name="resetChainName")
    def reset_chain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChainName", []))

    @jsii.member(jsii_name="resetGuestFlush")
    def reset_guest_flush(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestFlush", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetStorageLocations")
    def reset_storage_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageLocations", []))

    @builtins.property
    @jsii.member(jsii_name="chainNameInput")
    def chain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="guestFlushInput")
    def guest_flush_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "guestFlushInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageLocationsInput")
    def storage_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "storageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="chainName")
    def chain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chainName"))

    @chain_name.setter
    def chain_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chainName", value)

    @builtins.property
    @jsii.member(jsii_name="guestFlush")
    def guest_flush(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "guestFlush"))

    @guest_flush.setter
    def guest_flush(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestFlush", value)

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
    @jsii.member(jsii_name="storageLocations")
    def storage_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "storageLocations"))

    @storage_locations.setter
    def storage_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageLocations", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ComputeResourcePolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#create ComputeResourcePolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#delete ComputeResourcePolicy#delete}.
        '''
        if __debug__:
            def stub(
                *,
                create: typing.Optional[builtins.str] = None,
                delete: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#create ComputeResourcePolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_resource_policy#delete ComputeResourcePolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyTimeoutsOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

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
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ComputeResourcePolicyTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ComputeResourcePolicyTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ComputeResourcePolicyTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[ComputeResourcePolicyTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ComputeResourcePolicy",
    "ComputeResourcePolicyConfig",
    "ComputeResourcePolicyGroupPlacementPolicy",
    "ComputeResourcePolicyGroupPlacementPolicyOutputReference",
    "ComputeResourcePolicyInstanceSchedulePolicy",
    "ComputeResourcePolicyInstanceSchedulePolicyOutputReference",
    "ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule",
    "ComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference",
    "ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule",
    "ComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicy",
    "ComputeResourcePolicySnapshotSchedulePolicyOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy",
    "ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicySchedule",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties",
    "ComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference",
    "ComputeResourcePolicyTimeouts",
    "ComputeResourcePolicyTimeoutsOutputReference",
]

publication.publish()
