'''
# `google_game_services_game_server_config`

Refer to the Terraform Registory for docs: [`google_game_services_game_server_config`](https://www.terraform.io/docs/providers/google/r/game_services_game_server_config).
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


class GameServicesGameServerConfig(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfig",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config google_game_services_game_server_config}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        config_id: builtins.str,
        deployment_id: builtins.str,
        fleet_configs: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigFleetConfigs", typing.Dict[str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        scaling_configs: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigs", typing.Dict[str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GameServicesGameServerConfigTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config google_game_services_game_server_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param config_id: A unique id for the deployment config. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#config_id GameServicesGameServerConfig#config_id}
        :param deployment_id: A unique id for the deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#deployment_id GameServicesGameServerConfig#deployment_id}
        :param fleet_configs: fleet_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_configs GameServicesGameServerConfig#fleet_configs}
        :param description: The description of the game server config. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#description GameServicesGameServerConfig#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#id GameServicesGameServerConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this game server config. Each label is a key-value pair. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#labels GameServicesGameServerConfig#labels}
        :param location: Location of the Deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#location GameServicesGameServerConfig#location}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#project GameServicesGameServerConfig#project}.
        :param scaling_configs: scaling_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#scaling_configs GameServicesGameServerConfig#scaling_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#timeouts GameServicesGameServerConfig#timeouts}
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
                config_id: builtins.str,
                deployment_id: builtins.str,
                fleet_configs: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigFleetConfigs, typing.Dict[str, typing.Any]]]],
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                location: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                scaling_configs: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigs, typing.Dict[str, typing.Any]]]]] = None,
                timeouts: typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, typing.Dict[str, typing.Any]]] = None,
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
        config = GameServicesGameServerConfigConfig(
            config_id=config_id,
            deployment_id=deployment_id,
            fleet_configs=fleet_configs,
            description=description,
            id=id,
            labels=labels,
            location=location,
            project=project,
            scaling_configs=scaling_configs,
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

    @jsii.member(jsii_name="putFleetConfigs")
    def put_fleet_configs(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigFleetConfigs", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigFleetConfigs, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFleetConfigs", [value]))

    @jsii.member(jsii_name="putScalingConfigs")
    def put_scaling_configs(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigs", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigs, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScalingConfigs", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#create GameServicesGameServerConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#delete GameServicesGameServerConfig#delete}.
        '''
        value = GameServicesGameServerConfigTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetScalingConfigs")
    def reset_scaling_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingConfigs", []))

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
    @jsii.member(jsii_name="fleetConfigs")
    def fleet_configs(self) -> "GameServicesGameServerConfigFleetConfigsList":
        return typing.cast("GameServicesGameServerConfigFleetConfigsList", jsii.get(self, "fleetConfigs"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfigs")
    def scaling_configs(self) -> "GameServicesGameServerConfigScalingConfigsList":
        return typing.cast("GameServicesGameServerConfigScalingConfigsList", jsii.get(self, "scalingConfigs"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GameServicesGameServerConfigTimeoutsOutputReference":
        return typing.cast("GameServicesGameServerConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configIdInput")
    def config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentIdInput")
    def deployment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetConfigsInput")
    def fleet_configs_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigFleetConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigFleetConfigs"]]], jsii.get(self, "fleetConfigsInput"))

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
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfigsInput")
    def scaling_configs_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigs"]]], jsii.get(self, "scalingConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["GameServicesGameServerConfigTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["GameServicesGameServerConfigTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="configId")
    def config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configId"))

    @config_id.setter
    def config_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configId", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentId"))

    @deployment_id.setter
    def deployment_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentId", value)

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


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "config_id": "configId",
        "deployment_id": "deploymentId",
        "fleet_configs": "fleetConfigs",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "project": "project",
        "scaling_configs": "scalingConfigs",
        "timeouts": "timeouts",
    },
)
class GameServicesGameServerConfigConfig(cdktf.TerraformMetaArguments):
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
        config_id: builtins.str,
        deployment_id: builtins.str,
        fleet_configs: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigFleetConfigs", typing.Dict[str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        scaling_configs: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigs", typing.Dict[str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GameServicesGameServerConfigTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param config_id: A unique id for the deployment config. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#config_id GameServicesGameServerConfig#config_id}
        :param deployment_id: A unique id for the deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#deployment_id GameServicesGameServerConfig#deployment_id}
        :param fleet_configs: fleet_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_configs GameServicesGameServerConfig#fleet_configs}
        :param description: The description of the game server config. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#description GameServicesGameServerConfig#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#id GameServicesGameServerConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this game server config. Each label is a key-value pair. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#labels GameServicesGameServerConfig#labels}
        :param location: Location of the Deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#location GameServicesGameServerConfig#location}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#project GameServicesGameServerConfig#project}.
        :param scaling_configs: scaling_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#scaling_configs GameServicesGameServerConfig#scaling_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#timeouts GameServicesGameServerConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GameServicesGameServerConfigTimeouts(**timeouts)
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
                config_id: builtins.str,
                deployment_id: builtins.str,
                fleet_configs: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigFleetConfigs, typing.Dict[str, typing.Any]]]],
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                location: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                scaling_configs: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigs, typing.Dict[str, typing.Any]]]]] = None,
                timeouts: typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument config_id", value=config_id, expected_type=type_hints["config_id"])
            check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
            check_type(argname="argument fleet_configs", value=fleet_configs, expected_type=type_hints["fleet_configs"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument scaling_configs", value=scaling_configs, expected_type=type_hints["scaling_configs"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "config_id": config_id,
            "deployment_id": deployment_id,
            "fleet_configs": fleet_configs,
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
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if project is not None:
            self._values["project"] = project
        if scaling_configs is not None:
            self._values["scaling_configs"] = scaling_configs
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
    def config_id(self) -> builtins.str:
        '''A unique id for the deployment config.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#config_id GameServicesGameServerConfig#config_id}
        '''
        result = self._values.get("config_id")
        assert result is not None, "Required property 'config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_id(self) -> builtins.str:
        '''A unique id for the deployment.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#deployment_id GameServicesGameServerConfig#deployment_id}
        '''
        result = self._values.get("deployment_id")
        assert result is not None, "Required property 'deployment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fleet_configs(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigFleetConfigs"]]:
        '''fleet_configs block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_configs GameServicesGameServerConfig#fleet_configs}
        '''
        result = self._values.get("fleet_configs")
        assert result is not None, "Required property 'fleet_configs' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigFleetConfigs"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the game server config.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#description GameServicesGameServerConfig#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#id GameServicesGameServerConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels associated with this game server config. Each label is a key-value pair.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#labels GameServicesGameServerConfig#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Location of the Deployment.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#location GameServicesGameServerConfig#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#project GameServicesGameServerConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_configs(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigs"]]]:
        '''scaling_configs block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#scaling_configs GameServicesGameServerConfig#scaling_configs}
        '''
        result = self._values.get("scaling_configs")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigs"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GameServicesGameServerConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#timeouts GameServicesGameServerConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GameServicesGameServerConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigFleetConfigs",
    jsii_struct_bases=[],
    name_mapping={"fleet_spec": "fleetSpec", "name": "name"},
)
class GameServicesGameServerConfigFleetConfigs:
    def __init__(
        self,
        *,
        fleet_spec: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fleet_spec: The fleet spec, which is sent to Agones to configure fleet. The spec can be passed as inline json but it is recommended to use a file reference instead. File references can contain the json or yaml format of the fleet spec. Eg: fleet_spec = jsonencode(yamldecode(file("fleet_configs.yaml"))) fleet_spec = file("fleet_configs.json") The format of the spec can be found : 'https://agones.dev/site/docs/reference/fleet/'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_spec GameServicesGameServerConfig#fleet_spec}
        :param name: The name of the FleetConfig. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#name GameServicesGameServerConfig#name}
        '''
        if __debug__:
            def stub(
                *,
                fleet_spec: builtins.str,
                name: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument fleet_spec", value=fleet_spec, expected_type=type_hints["fleet_spec"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {
            "fleet_spec": fleet_spec,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def fleet_spec(self) -> builtins.str:
        '''The fleet spec, which is sent to Agones to configure fleet.

        The spec can be passed as inline json but it is recommended to use a file reference
        instead. File references can contain the json or yaml format of the fleet spec. Eg:

        fleet_spec = jsonencode(yamldecode(file("fleet_configs.yaml")))
        fleet_spec = file("fleet_configs.json")

        The format of the spec can be found :
        'https://agones.dev/site/docs/reference/fleet/'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_spec GameServicesGameServerConfig#fleet_spec}
        '''
        result = self._values.get("fleet_spec")
        assert result is not None, "Required property 'fleet_spec' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the FleetConfig.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#name GameServicesGameServerConfig#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigFleetConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerConfigFleetConfigsList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigFleetConfigsList",
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
    ) -> "GameServicesGameServerConfigFleetConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GameServicesGameServerConfigFleetConfigsOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigFleetConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigFleetConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigFleetConfigs]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigFleetConfigs]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GameServicesGameServerConfigFleetConfigsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigFleetConfigsOutputReference",
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

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="fleetSpecInput")
    def fleet_spec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fleetSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetSpec")
    def fleet_spec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fleetSpec"))

    @fleet_spec.setter
    def fleet_spec(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fleetSpec", value)

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
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GameServicesGameServerConfigFleetConfigs, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerConfigFleetConfigs, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerConfigFleetConfigs, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[GameServicesGameServerConfigFleetConfigs, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "fleet_autoscaler_spec": "fleetAutoscalerSpec",
        "name": "name",
        "schedules": "schedules",
        "selectors": "selectors",
    },
)
class GameServicesGameServerConfigScalingConfigs:
    def __init__(
        self,
        *,
        fleet_autoscaler_spec: builtins.str,
        name: builtins.str,
        schedules: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigsSchedules", typing.Dict[str, typing.Any]]]]] = None,
        selectors: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigsSelectors", typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param fleet_autoscaler_spec: Fleet autoscaler spec, which is sent to Agones. Example spec can be found : https://agones.dev/site/docs/reference/fleetautoscaler/. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_autoscaler_spec GameServicesGameServerConfig#fleet_autoscaler_spec}
        :param name: The name of the ScalingConfig. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#name GameServicesGameServerConfig#name}
        :param schedules: schedules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#schedules GameServicesGameServerConfig#schedules}
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#selectors GameServicesGameServerConfig#selectors}
        '''
        if __debug__:
            def stub(
                *,
                fleet_autoscaler_spec: builtins.str,
                name: builtins.str,
                schedules: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, typing.Dict[str, typing.Any]]]]] = None,
                selectors: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, typing.Dict[str, typing.Any]]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument fleet_autoscaler_spec", value=fleet_autoscaler_spec, expected_type=type_hints["fleet_autoscaler_spec"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedules", value=schedules, expected_type=type_hints["schedules"])
            check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
        self._values: typing.Dict[str, typing.Any] = {
            "fleet_autoscaler_spec": fleet_autoscaler_spec,
            "name": name,
        }
        if schedules is not None:
            self._values["schedules"] = schedules
        if selectors is not None:
            self._values["selectors"] = selectors

    @builtins.property
    def fleet_autoscaler_spec(self) -> builtins.str:
        '''Fleet autoscaler spec, which is sent to Agones. Example spec can be found : https://agones.dev/site/docs/reference/fleetautoscaler/.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_autoscaler_spec GameServicesGameServerConfig#fleet_autoscaler_spec}
        '''
        result = self._values.get("fleet_autoscaler_spec")
        assert result is not None, "Required property 'fleet_autoscaler_spec' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the ScalingConfig.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#name GameServicesGameServerConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedules(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSchedules"]]]:
        '''schedules block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#schedules GameServicesGameServerConfig#schedules}
        '''
        result = self._values.get("schedules")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSchedules"]]], result)

    @builtins.property
    def selectors(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSelectors"]]]:
        '''selectors block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#selectors GameServicesGameServerConfig#selectors}
        '''
        result = self._values.get("selectors")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSelectors"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigScalingConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerConfigScalingConfigsList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsList",
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
    ) -> "GameServicesGameServerConfigScalingConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GameServicesGameServerConfigScalingConfigsOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigs]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigs]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GameServicesGameServerConfigScalingConfigsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsOutputReference",
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

    @jsii.member(jsii_name="putSchedules")
    def put_schedules(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigsSchedules", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchedules", [value]))

    @jsii.member(jsii_name="putSelectors")
    def put_selectors(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigsSelectors", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelectors", [value]))

    @jsii.member(jsii_name="resetSchedules")
    def reset_schedules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedules", []))

    @jsii.member(jsii_name="resetSelectors")
    def reset_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectors", []))

    @builtins.property
    @jsii.member(jsii_name="schedules")
    def schedules(self) -> "GameServicesGameServerConfigScalingConfigsSchedulesList":
        return typing.cast("GameServicesGameServerConfigScalingConfigsSchedulesList", jsii.get(self, "schedules"))

    @builtins.property
    @jsii.member(jsii_name="selectors")
    def selectors(self) -> "GameServicesGameServerConfigScalingConfigsSelectorsList":
        return typing.cast("GameServicesGameServerConfigScalingConfigsSelectorsList", jsii.get(self, "selectors"))

    @builtins.property
    @jsii.member(jsii_name="fleetAutoscalerSpecInput")
    def fleet_autoscaler_spec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fleetAutoscalerSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulesInput")
    def schedules_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSchedules"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSchedules"]]], jsii.get(self, "schedulesInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorsInput")
    def selectors_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSelectors"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSelectors"]]], jsii.get(self, "selectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetAutoscalerSpec")
    def fleet_autoscaler_spec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fleetAutoscalerSpec"))

    @fleet_autoscaler_spec.setter
    def fleet_autoscaler_spec(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fleetAutoscalerSpec", value)

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
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigs, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigs, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigs, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigs, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSchedules",
    jsii_struct_bases=[],
    name_mapping={
        "cron_job_duration": "cronJobDuration",
        "cron_spec": "cronSpec",
        "end_time": "endTime",
        "start_time": "startTime",
    },
)
class GameServicesGameServerConfigScalingConfigsSchedules:
    def __init__(
        self,
        *,
        cron_job_duration: typing.Optional[builtins.str] = None,
        cron_spec: typing.Optional[builtins.str] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cron_job_duration: The duration for the cron job event. The duration of the event is effective after the cron job's start time. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#cron_job_duration GameServicesGameServerConfig#cron_job_duration}
        :param cron_spec: The cron definition of the scheduled event. See https://en.wikipedia.org/wiki/Cron. Cron spec specifies the local time as defined by the realm. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#cron_spec GameServicesGameServerConfig#cron_spec}
        :param end_time: The end time of the event. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#end_time GameServicesGameServerConfig#end_time}
        :param start_time: The start time of the event. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#start_time GameServicesGameServerConfig#start_time}
        '''
        if __debug__:
            def stub(
                *,
                cron_job_duration: typing.Optional[builtins.str] = None,
                cron_spec: typing.Optional[builtins.str] = None,
                end_time: typing.Optional[builtins.str] = None,
                start_time: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument cron_job_duration", value=cron_job_duration, expected_type=type_hints["cron_job_duration"])
            check_type(argname="argument cron_spec", value=cron_spec, expected_type=type_hints["cron_spec"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[str, typing.Any] = {}
        if cron_job_duration is not None:
            self._values["cron_job_duration"] = cron_job_duration
        if cron_spec is not None:
            self._values["cron_spec"] = cron_spec
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def cron_job_duration(self) -> typing.Optional[builtins.str]:
        '''The duration for the cron job event. The duration of the event is effective after the cron job's start time.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#cron_job_duration GameServicesGameServerConfig#cron_job_duration}
        '''
        result = self._values.get("cron_job_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cron_spec(self) -> typing.Optional[builtins.str]:
        '''The cron definition of the scheduled event. See https://en.wikipedia.org/wiki/Cron. Cron spec specifies the local time as defined by the realm.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#cron_spec GameServicesGameServerConfig#cron_spec}
        '''
        result = self._values.get("cron_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''The end time of the event.

        A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#end_time GameServicesGameServerConfig#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The start time of the event.

        A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#start_time GameServicesGameServerConfig#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigScalingConfigsSchedules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerConfigScalingConfigsSchedulesList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSchedulesList",
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
    ) -> "GameServicesGameServerConfigScalingConfigsSchedulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GameServicesGameServerConfigScalingConfigsSchedulesOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSchedules]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSchedules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSchedules]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSchedules]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GameServicesGameServerConfigScalingConfigsSchedulesOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSchedulesOutputReference",
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

    @jsii.member(jsii_name="resetCronJobDuration")
    def reset_cron_job_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronJobDuration", []))

    @jsii.member(jsii_name="resetCronSpec")
    def reset_cron_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronSpec", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="cronJobDurationInput")
    def cron_job_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronJobDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="cronSpecInput")
    def cron_spec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="cronJobDuration")
    def cron_job_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronJobDuration"))

    @cron_job_duration.setter
    def cron_job_duration(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronJobDuration", value)

    @builtins.property
    @jsii.member(jsii_name="cronSpec")
    def cron_spec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronSpec"))

    @cron_spec.setter
    def cron_spec(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronSpec", value)

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value)

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
    ) -> typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSelectors",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class GameServicesGameServerConfigScalingConfigsSelectors:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Set of labels to group by. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#labels GameServicesGameServerConfig#labels}
        '''
        if __debug__:
            def stub(
                *,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of labels to group by.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#labels GameServicesGameServerConfig#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigScalingConfigsSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerConfigScalingConfigsSelectorsList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSelectorsList",
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
    ) -> "GameServicesGameServerConfigScalingConfigsSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GameServicesGameServerConfigScalingConfigsSelectorsOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSelectors]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSelectors]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GameServicesGameServerConfigScalingConfigsSelectorsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSelectorsOutputReference",
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

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

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
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GameServicesGameServerConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#create GameServicesGameServerConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#delete GameServicesGameServerConfig#delete}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#create GameServicesGameServerConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#delete GameServicesGameServerConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerConfigTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigTimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GameServicesGameServerConfig",
    "GameServicesGameServerConfigConfig",
    "GameServicesGameServerConfigFleetConfigs",
    "GameServicesGameServerConfigFleetConfigsList",
    "GameServicesGameServerConfigFleetConfigsOutputReference",
    "GameServicesGameServerConfigScalingConfigs",
    "GameServicesGameServerConfigScalingConfigsList",
    "GameServicesGameServerConfigScalingConfigsOutputReference",
    "GameServicesGameServerConfigScalingConfigsSchedules",
    "GameServicesGameServerConfigScalingConfigsSchedulesList",
    "GameServicesGameServerConfigScalingConfigsSchedulesOutputReference",
    "GameServicesGameServerConfigScalingConfigsSelectors",
    "GameServicesGameServerConfigScalingConfigsSelectorsList",
    "GameServicesGameServerConfigScalingConfigsSelectorsOutputReference",
    "GameServicesGameServerConfigTimeouts",
    "GameServicesGameServerConfigTimeoutsOutputReference",
]

publication.publish()
