'''
# `google_cloud_run_domain_mapping`

Refer to the Terraform Registory for docs: [`google_cloud_run_domain_mapping`](https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping).
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


class CloudRunDomainMapping(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMapping",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping google_cloud_run_domain_mapping}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        metadata: typing.Union["CloudRunDomainMappingMetadata", typing.Dict[str, typing.Any]],
        name: builtins.str,
        spec: typing.Union["CloudRunDomainMappingSpec", typing.Dict[str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudRunDomainMappingTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping google_cloud_run_domain_mapping} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the cloud run instance. eg us-central1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#location CloudRunDomainMapping#location}
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#metadata CloudRunDomainMapping#metadata}
        :param name: Name should be a `verified <https://support.google.com/webmasters/answer/9008080>`_ domain. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#name CloudRunDomainMapping#name}
        :param spec: spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#spec CloudRunDomainMapping#spec}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#id CloudRunDomainMapping#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#project CloudRunDomainMapping#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#timeouts CloudRunDomainMapping#timeouts}
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
                metadata: typing.Union[CloudRunDomainMappingMetadata, typing.Dict[str, typing.Any]],
                name: builtins.str,
                spec: typing.Union[CloudRunDomainMappingSpec, typing.Dict[str, typing.Any]],
                id: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union[CloudRunDomainMappingTimeouts, typing.Dict[str, typing.Any]]] = None,
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
        config = CloudRunDomainMappingConfig(
            location=location,
            metadata=metadata,
            name=name,
            spec=spec,
            id=id,
            project=project,
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

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        *,
        namespace: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param namespace: In Cloud Run the namespace must be equal to either the project ID or project number. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#namespace CloudRunDomainMapping#namespace}
        :param annotations: Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. More info: http://kubernetes.io/docs/user-guide/annotations *Note**: The Cloud Run API may add additional annotations that were not provided in your config. If terraform plan shows a diff where a server-side annotation is added, you can add it to your config or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#annotations CloudRunDomainMapping#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and routes. More info: http://kubernetes.io/docs/user-guide/labels Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#labels CloudRunDomainMapping#labels}
        '''
        value = CloudRunDomainMappingMetadata(
            namespace=namespace, annotations=annotations, labels=labels
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        route_name: builtins.str,
        certificate_mode: typing.Optional[builtins.str] = None,
        force_override: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param route_name: The name of the Cloud Run Service that this DomainMapping applies to. The route must exist. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#route_name CloudRunDomainMapping#route_name}
        :param certificate_mode: The mode of the certificate. Default value: "AUTOMATIC" Possible values: ["NONE", "AUTOMATIC"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#certificate_mode CloudRunDomainMapping#certificate_mode}
        :param force_override: If set, the mapping will override any mapping set before this spec was set. It is recommended that the user leaves this empty to receive an error warning about a potential conflict and only set it once the respective UI has given such a warning. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#force_override CloudRunDomainMapping#force_override}
        '''
        value = CloudRunDomainMappingSpec(
            route_name=route_name,
            certificate_mode=certificate_mode,
            force_override=force_override,
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#create CloudRunDomainMapping#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#delete CloudRunDomainMapping#delete}.
        '''
        value = CloudRunDomainMappingTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "CloudRunDomainMappingMetadataOutputReference":
        return typing.cast("CloudRunDomainMappingMetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "CloudRunDomainMappingSpecOutputReference":
        return typing.cast("CloudRunDomainMappingSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "CloudRunDomainMappingStatusList":
        return typing.cast("CloudRunDomainMappingStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudRunDomainMappingTimeoutsOutputReference":
        return typing.cast("CloudRunDomainMappingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["CloudRunDomainMappingMetadata"]:
        return typing.cast(typing.Optional["CloudRunDomainMappingMetadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["CloudRunDomainMappingSpec"]:
        return typing.cast(typing.Optional["CloudRunDomainMappingSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["CloudRunDomainMappingTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["CloudRunDomainMappingTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

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


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingConfig",
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
        "metadata": "metadata",
        "name": "name",
        "spec": "spec",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class CloudRunDomainMappingConfig(cdktf.TerraformMetaArguments):
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
        metadata: typing.Union["CloudRunDomainMappingMetadata", typing.Dict[str, typing.Any]],
        name: builtins.str,
        spec: typing.Union["CloudRunDomainMappingSpec", typing.Dict[str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudRunDomainMappingTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the cloud run instance. eg us-central1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#location CloudRunDomainMapping#location}
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#metadata CloudRunDomainMapping#metadata}
        :param name: Name should be a `verified <https://support.google.com/webmasters/answer/9008080>`_ domain. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#name CloudRunDomainMapping#name}
        :param spec: spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#spec CloudRunDomainMapping#spec}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#id CloudRunDomainMapping#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#project CloudRunDomainMapping#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#timeouts CloudRunDomainMapping#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = CloudRunDomainMappingMetadata(**metadata)
        if isinstance(spec, dict):
            spec = CloudRunDomainMappingSpec(**spec)
        if isinstance(timeouts, dict):
            timeouts = CloudRunDomainMappingTimeouts(**timeouts)
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
                metadata: typing.Union[CloudRunDomainMappingMetadata, typing.Dict[str, typing.Any]],
                name: builtins.str,
                spec: typing.Union[CloudRunDomainMappingSpec, typing.Dict[str, typing.Any]],
                id: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union[CloudRunDomainMappingTimeouts, typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "location": location,
            "metadata": metadata,
            "name": name,
            "spec": spec,
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
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
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
        '''The location of the cloud run instance. eg us-central1.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#location CloudRunDomainMapping#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata(self) -> "CloudRunDomainMappingMetadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#metadata CloudRunDomainMapping#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("CloudRunDomainMappingMetadata", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name should be a `verified <https://support.google.com/webmasters/answer/9008080>`_ domain.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#name CloudRunDomainMapping#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec(self) -> "CloudRunDomainMappingSpec":
        '''spec block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#spec CloudRunDomainMapping#spec}
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("CloudRunDomainMappingSpec", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#id CloudRunDomainMapping#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#project CloudRunDomainMapping#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudRunDomainMappingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#timeouts CloudRunDomainMapping#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudRunDomainMappingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunDomainMappingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "namespace": "namespace",
        "annotations": "annotations",
        "labels": "labels",
    },
)
class CloudRunDomainMappingMetadata:
    def __init__(
        self,
        *,
        namespace: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param namespace: In Cloud Run the namespace must be equal to either the project ID or project number. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#namespace CloudRunDomainMapping#namespace}
        :param annotations: Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. More info: http://kubernetes.io/docs/user-guide/annotations *Note**: The Cloud Run API may add additional annotations that were not provided in your config. If terraform plan shows a diff where a server-side annotation is added, you can add it to your config or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#annotations CloudRunDomainMapping#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and routes. More info: http://kubernetes.io/docs/user-guide/labels Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#labels CloudRunDomainMapping#labels}
        '''
        if __debug__:
            def stub(
                *,
                namespace: builtins.str,
                annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[str, typing.Any] = {
            "namespace": namespace,
        }
        if annotations is not None:
            self._values["annotations"] = annotations
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def namespace(self) -> builtins.str:
        '''In Cloud Run the namespace must be equal to either the project ID or project number.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#namespace CloudRunDomainMapping#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata.

        More
        info: http://kubernetes.io/docs/user-guide/annotations

        *Note**: The Cloud Run API may add additional annotations that were not provided in your config.
        If terraform plan shows a diff where a server-side annotation is added, you can add it to your config
        or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#annotations CloudRunDomainMapping#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) objects.

        May match selectors of replication controllers
        and routes.
        More info: http://kubernetes.io/docs/user-guide/labels

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#labels CloudRunDomainMapping#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunDomainMappingMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunDomainMappingMetadataOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingMetadataOutputReference",
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

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @builtins.property
    @jsii.member(jsii_name="resourceVersion")
    def resource_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceVersion"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

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
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunDomainMappingMetadata]:
        return typing.cast(typing.Optional[CloudRunDomainMappingMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunDomainMappingMetadata],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[CloudRunDomainMappingMetadata]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingSpec",
    jsii_struct_bases=[],
    name_mapping={
        "route_name": "routeName",
        "certificate_mode": "certificateMode",
        "force_override": "forceOverride",
    },
)
class CloudRunDomainMappingSpec:
    def __init__(
        self,
        *,
        route_name: builtins.str,
        certificate_mode: typing.Optional[builtins.str] = None,
        force_override: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param route_name: The name of the Cloud Run Service that this DomainMapping applies to. The route must exist. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#route_name CloudRunDomainMapping#route_name}
        :param certificate_mode: The mode of the certificate. Default value: "AUTOMATIC" Possible values: ["NONE", "AUTOMATIC"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#certificate_mode CloudRunDomainMapping#certificate_mode}
        :param force_override: If set, the mapping will override any mapping set before this spec was set. It is recommended that the user leaves this empty to receive an error warning about a potential conflict and only set it once the respective UI has given such a warning. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#force_override CloudRunDomainMapping#force_override}
        '''
        if __debug__:
            def stub(
                *,
                route_name: builtins.str,
                certificate_mode: typing.Optional[builtins.str] = None,
                force_override: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument route_name", value=route_name, expected_type=type_hints["route_name"])
            check_type(argname="argument certificate_mode", value=certificate_mode, expected_type=type_hints["certificate_mode"])
            check_type(argname="argument force_override", value=force_override, expected_type=type_hints["force_override"])
        self._values: typing.Dict[str, typing.Any] = {
            "route_name": route_name,
        }
        if certificate_mode is not None:
            self._values["certificate_mode"] = certificate_mode
        if force_override is not None:
            self._values["force_override"] = force_override

    @builtins.property
    def route_name(self) -> builtins.str:
        '''The name of the Cloud Run Service that this DomainMapping applies to. The route must exist.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#route_name CloudRunDomainMapping#route_name}
        '''
        result = self._values.get("route_name")
        assert result is not None, "Required property 'route_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_mode(self) -> typing.Optional[builtins.str]:
        '''The mode of the certificate. Default value: "AUTOMATIC" Possible values: ["NONE", "AUTOMATIC"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#certificate_mode CloudRunDomainMapping#certificate_mode}
        '''
        result = self._values.get("certificate_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_override(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''If set, the mapping will override any mapping set before this spec was set.

        It is recommended that the user leaves this empty to receive an error
        warning about a potential conflict and only set it once the respective UI
        has given such a warning.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#force_override CloudRunDomainMapping#force_override}
        '''
        result = self._values.get("force_override")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunDomainMappingSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunDomainMappingSpecOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingSpecOutputReference",
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

    @jsii.member(jsii_name="resetCertificateMode")
    def reset_certificate_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateMode", []))

    @jsii.member(jsii_name="resetForceOverride")
    def reset_force_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceOverride", []))

    @builtins.property
    @jsii.member(jsii_name="certificateModeInput")
    def certificate_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateModeInput"))

    @builtins.property
    @jsii.member(jsii_name="forceOverrideInput")
    def force_override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "forceOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="routeNameInput")
    def route_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateMode")
    def certificate_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateMode"))

    @certificate_mode.setter
    def certificate_mode(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateMode", value)

    @builtins.property
    @jsii.member(jsii_name="forceOverride")
    def force_override(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "forceOverride"))

    @force_override.setter
    def force_override(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceOverride", value)

    @builtins.property
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeName"))

    @route_name.setter
    def route_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunDomainMappingSpec]:
        return typing.cast(typing.Optional[CloudRunDomainMappingSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudRunDomainMappingSpec]) -> None:
        if __debug__:
            def stub(value: typing.Optional[CloudRunDomainMappingSpec]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunDomainMappingStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunDomainMappingStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunDomainMappingStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunDomainMappingStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunDomainMappingStatusConditionsList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingStatusConditionsList",
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
    ) -> "CloudRunDomainMappingStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunDomainMappingStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

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


class CloudRunDomainMappingStatusConditionsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingStatusConditionsOutputReference",
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
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunDomainMappingStatusConditions]:
        return typing.cast(typing.Optional[CloudRunDomainMappingStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunDomainMappingStatusConditions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[CloudRunDomainMappingStatusConditions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CloudRunDomainMappingStatusList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingStatusList",
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
    def get(self, index: jsii.Number) -> "CloudRunDomainMappingStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunDomainMappingStatusOutputReference", jsii.invoke(self, "get", [index]))

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


class CloudRunDomainMappingStatusOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingStatusOutputReference",
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
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> CloudRunDomainMappingStatusConditionsList:
        return typing.cast(CloudRunDomainMappingStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="mappedRouteName")
    def mapped_route_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mappedRouteName"))

    @builtins.property
    @jsii.member(jsii_name="observedGeneration")
    def observed_generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "observedGeneration"))

    @builtins.property
    @jsii.member(jsii_name="resourceRecords")
    def resource_records(self) -> "CloudRunDomainMappingStatusResourceRecordsList":
        return typing.cast("CloudRunDomainMappingStatusResourceRecordsList", jsii.get(self, "resourceRecords"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunDomainMappingStatus]:
        return typing.cast(typing.Optional[CloudRunDomainMappingStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunDomainMappingStatus],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[CloudRunDomainMappingStatus]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingStatusResourceRecords",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunDomainMappingStatusResourceRecords:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunDomainMappingStatusResourceRecords(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunDomainMappingStatusResourceRecordsList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingStatusResourceRecordsList",
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
    ) -> "CloudRunDomainMappingStatusResourceRecordsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunDomainMappingStatusResourceRecordsOutputReference", jsii.invoke(self, "get", [index]))

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


class CloudRunDomainMappingStatusResourceRecordsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingStatusResourceRecordsOutputReference",
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="rrdata")
    def rrdata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rrdata"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunDomainMappingStatusResourceRecords]:
        return typing.cast(typing.Optional[CloudRunDomainMappingStatusResourceRecords], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunDomainMappingStatusResourceRecords],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[CloudRunDomainMappingStatusResourceRecords],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class CloudRunDomainMappingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#create CloudRunDomainMapping#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#delete CloudRunDomainMapping#delete}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#create CloudRunDomainMapping#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloud_run_domain_mapping#delete CloudRunDomainMapping#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunDomainMappingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunDomainMappingTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunDomainMapping.CloudRunDomainMappingTimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[CloudRunDomainMappingTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CloudRunDomainMappingTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CloudRunDomainMappingTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[CloudRunDomainMappingTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CloudRunDomainMapping",
    "CloudRunDomainMappingConfig",
    "CloudRunDomainMappingMetadata",
    "CloudRunDomainMappingMetadataOutputReference",
    "CloudRunDomainMappingSpec",
    "CloudRunDomainMappingSpecOutputReference",
    "CloudRunDomainMappingStatus",
    "CloudRunDomainMappingStatusConditions",
    "CloudRunDomainMappingStatusConditionsList",
    "CloudRunDomainMappingStatusConditionsOutputReference",
    "CloudRunDomainMappingStatusList",
    "CloudRunDomainMappingStatusOutputReference",
    "CloudRunDomainMappingStatusResourceRecords",
    "CloudRunDomainMappingStatusResourceRecordsList",
    "CloudRunDomainMappingStatusResourceRecordsOutputReference",
    "CloudRunDomainMappingTimeouts",
    "CloudRunDomainMappingTimeoutsOutputReference",
]

publication.publish()
