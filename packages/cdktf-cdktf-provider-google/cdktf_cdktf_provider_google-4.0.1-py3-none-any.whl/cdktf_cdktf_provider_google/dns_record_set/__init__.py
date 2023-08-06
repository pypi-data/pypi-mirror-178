'''
# `google_dns_record_set`

Refer to the Terraform Registory for docs: [`google_dns_record_set`](https://www.terraform.io/docs/providers/google/r/dns_record_set).
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


class DnsRecordSet(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSet",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/dns_record_set google_dns_record_set}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        managed_zone: builtins.str,
        name: builtins.str,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        routing_policy: typing.Optional[typing.Union["DnsRecordSetRoutingPolicy", typing.Dict[str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
        ttl: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/dns_record_set google_dns_record_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param managed_zone: The name of the zone in which this record set will reside. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#managed_zone DnsRecordSet#managed_zone}
        :param name: The DNS name this record set will apply to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#name DnsRecordSet#name}
        :param type: The DNS record set type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#type DnsRecordSet#type}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#id DnsRecordSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#project DnsRecordSet#project}
        :param routing_policy: routing_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#routing_policy DnsRecordSet#routing_policy}
        :param rrdatas: The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string data contains spaces, add surrounding " if you don't want your string to get split on spaces. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add "" inside the Terraform configuration string (e.g. "first255characters""morecharacters"). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#rrdatas DnsRecordSet#rrdatas}
        :param ttl: The time-to-live of this record set (seconds). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ttl DnsRecordSet#ttl}
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
                managed_zone: builtins.str,
                name: builtins.str,
                type: builtins.str,
                id: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                routing_policy: typing.Optional[typing.Union[DnsRecordSetRoutingPolicy, typing.Dict[str, typing.Any]]] = None,
                rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
                ttl: typing.Optional[jsii.Number] = None,
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
        config = DnsRecordSetConfig(
            managed_zone=managed_zone,
            name=name,
            type=type,
            id=id,
            project=project,
            routing_policy=routing_policy,
            rrdatas=rrdatas,
            ttl=ttl,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putRoutingPolicy")
    def put_routing_policy(
        self,
        *,
        enable_geo_fencing: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        geo: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyGeo", typing.Dict[str, typing.Any]]]]] = None,
        primary_backup: typing.Optional[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackup", typing.Dict[str, typing.Any]]] = None,
        wrr: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyWrr", typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enable_geo_fencing: Specifies whether to enable fencing for geo queries. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#enable_geo_fencing DnsRecordSet#enable_geo_fencing}
        :param geo: geo block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#geo DnsRecordSet#geo}
        :param primary_backup: primary_backup block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#primary_backup DnsRecordSet#primary_backup}
        :param wrr: wrr block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#wrr DnsRecordSet#wrr}
        '''
        value = DnsRecordSetRoutingPolicy(
            enable_geo_fencing=enable_geo_fencing,
            geo=geo,
            primary_backup=primary_backup,
            wrr=wrr,
        )

        return typing.cast(None, jsii.invoke(self, "putRoutingPolicy", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRoutingPolicy")
    def reset_routing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingPolicy", []))

    @jsii.member(jsii_name="resetRrdatas")
    def reset_rrdatas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRrdatas", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="routingPolicy")
    def routing_policy(self) -> "DnsRecordSetRoutingPolicyOutputReference":
        return typing.cast("DnsRecordSetRoutingPolicyOutputReference", jsii.get(self, "routingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="managedZoneInput")
    def managed_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="routingPolicyInput")
    def routing_policy_input(self) -> typing.Optional["DnsRecordSetRoutingPolicy"]:
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicy"], jsii.get(self, "routingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="rrdatasInput")
    def rrdatas_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rrdatasInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

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
    @jsii.member(jsii_name="managedZone")
    def managed_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedZone"))

    @managed_zone.setter
    def managed_zone(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedZone", value)

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
    @jsii.member(jsii_name="rrdatas")
    def rrdatas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rrdatas"))

    @rrdatas.setter
    def rrdatas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value)

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "managed_zone": "managedZone",
        "name": "name",
        "type": "type",
        "id": "id",
        "project": "project",
        "routing_policy": "routingPolicy",
        "rrdatas": "rrdatas",
        "ttl": "ttl",
    },
)
class DnsRecordSetConfig(cdktf.TerraformMetaArguments):
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
        managed_zone: builtins.str,
        name: builtins.str,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        routing_policy: typing.Optional[typing.Union["DnsRecordSetRoutingPolicy", typing.Dict[str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
        ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param managed_zone: The name of the zone in which this record set will reside. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#managed_zone DnsRecordSet#managed_zone}
        :param name: The DNS name this record set will apply to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#name DnsRecordSet#name}
        :param type: The DNS record set type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#type DnsRecordSet#type}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#id DnsRecordSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#project DnsRecordSet#project}
        :param routing_policy: routing_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#routing_policy DnsRecordSet#routing_policy}
        :param rrdatas: The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string data contains spaces, add surrounding " if you don't want your string to get split on spaces. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add "" inside the Terraform configuration string (e.g. "first255characters""morecharacters"). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#rrdatas DnsRecordSet#rrdatas}
        :param ttl: The time-to-live of this record set (seconds). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ttl DnsRecordSet#ttl}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(routing_policy, dict):
            routing_policy = DnsRecordSetRoutingPolicy(**routing_policy)
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
                managed_zone: builtins.str,
                name: builtins.str,
                type: builtins.str,
                id: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                routing_policy: typing.Optional[typing.Union[DnsRecordSetRoutingPolicy, typing.Dict[str, typing.Any]]] = None,
                rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
                ttl: typing.Optional[jsii.Number] = None,
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
            check_type(argname="argument managed_zone", value=managed_zone, expected_type=type_hints["managed_zone"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument routing_policy", value=routing_policy, expected_type=type_hints["routing_policy"])
            check_type(argname="argument rrdatas", value=rrdatas, expected_type=type_hints["rrdatas"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[str, typing.Any] = {
            "managed_zone": managed_zone,
            "name": name,
            "type": type,
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
        if routing_policy is not None:
            self._values["routing_policy"] = routing_policy
        if rrdatas is not None:
            self._values["rrdatas"] = rrdatas
        if ttl is not None:
            self._values["ttl"] = ttl

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
    def managed_zone(self) -> builtins.str:
        '''The name of the zone in which this record set will reside.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#managed_zone DnsRecordSet#managed_zone}
        '''
        result = self._values.get("managed_zone")
        assert result is not None, "Required property 'managed_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The DNS name this record set will apply to.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#name DnsRecordSet#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The DNS record set type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#type DnsRecordSet#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#id DnsRecordSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#project DnsRecordSet#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_policy(self) -> typing.Optional["DnsRecordSetRoutingPolicy"]:
        '''routing_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#routing_policy DnsRecordSet#routing_policy}
        '''
        result = self._values.get("routing_policy")
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicy"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The string data for the records in this record set whose meaning depends on the DNS type.

        For TXT record, if the string data contains spaces, add surrounding " if you don't want your string to get split on spaces. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add "" inside the Terraform configuration string (e.g. "first255characters""morecharacters").

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#rrdatas DnsRecordSet#rrdatas}
        '''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''The time-to-live of this record set (seconds).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ttl DnsRecordSet#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "enable_geo_fencing": "enableGeoFencing",
        "geo": "geo",
        "primary_backup": "primaryBackup",
        "wrr": "wrr",
    },
)
class DnsRecordSetRoutingPolicy:
    def __init__(
        self,
        *,
        enable_geo_fencing: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        geo: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyGeo", typing.Dict[str, typing.Any]]]]] = None,
        primary_backup: typing.Optional[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackup", typing.Dict[str, typing.Any]]] = None,
        wrr: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyWrr", typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enable_geo_fencing: Specifies whether to enable fencing for geo queries. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#enable_geo_fencing DnsRecordSet#enable_geo_fencing}
        :param geo: geo block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#geo DnsRecordSet#geo}
        :param primary_backup: primary_backup block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#primary_backup DnsRecordSet#primary_backup}
        :param wrr: wrr block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#wrr DnsRecordSet#wrr}
        '''
        if isinstance(primary_backup, dict):
            primary_backup = DnsRecordSetRoutingPolicyPrimaryBackup(**primary_backup)
        if __debug__:
            def stub(
                *,
                enable_geo_fencing: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                geo: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeo, typing.Dict[str, typing.Any]]]]] = None,
                primary_backup: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackup, typing.Dict[str, typing.Any]]] = None,
                wrr: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrr, typing.Dict[str, typing.Any]]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument enable_geo_fencing", value=enable_geo_fencing, expected_type=type_hints["enable_geo_fencing"])
            check_type(argname="argument geo", value=geo, expected_type=type_hints["geo"])
            check_type(argname="argument primary_backup", value=primary_backup, expected_type=type_hints["primary_backup"])
            check_type(argname="argument wrr", value=wrr, expected_type=type_hints["wrr"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enable_geo_fencing is not None:
            self._values["enable_geo_fencing"] = enable_geo_fencing
        if geo is not None:
            self._values["geo"] = geo
        if primary_backup is not None:
            self._values["primary_backup"] = primary_backup
        if wrr is not None:
            self._values["wrr"] = wrr

    @builtins.property
    def enable_geo_fencing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Specifies whether to enable fencing for geo queries.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#enable_geo_fencing DnsRecordSet#enable_geo_fencing}
        '''
        result = self._values.get("enable_geo_fencing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def geo(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyGeo"]]]:
        '''geo block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#geo DnsRecordSet#geo}
        '''
        result = self._values.get("geo")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyGeo"]]], result)

    @builtins.property
    def primary_backup(
        self,
    ) -> typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackup"]:
        '''primary_backup block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#primary_backup DnsRecordSet#primary_backup}
        '''
        result = self._values.get("primary_backup")
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackup"], result)

    @builtins.property
    def wrr(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrr"]]]:
        '''wrr block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#wrr DnsRecordSet#wrr}
        '''
        result = self._values.get("wrr")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrr"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeo",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "health_checked_targets": "healthCheckedTargets",
        "rrdatas": "rrdatas",
    },
)
class DnsRecordSetRoutingPolicyGeo:
    def __init__(
        self,
        *,
        location: builtins.str,
        health_checked_targets: typing.Optional[typing.Union["DnsRecordSetRoutingPolicyGeoHealthCheckedTargets", typing.Dict[str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: The location name defined in Google Cloud. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#location DnsRecordSet#location}
        :param health_checked_targets: health_checked_targets block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        :param rrdatas: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#rrdatas DnsRecordSet#rrdatas}.
        '''
        if isinstance(health_checked_targets, dict):
            health_checked_targets = DnsRecordSetRoutingPolicyGeoHealthCheckedTargets(**health_checked_targets)
        if __debug__:
            def stub(
                *,
                location: builtins.str,
                health_checked_targets: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets, typing.Dict[str, typing.Any]]] = None,
                rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument health_checked_targets", value=health_checked_targets, expected_type=type_hints["health_checked_targets"])
            check_type(argname="argument rrdatas", value=rrdatas, expected_type=type_hints["rrdatas"])
        self._values: typing.Dict[str, typing.Any] = {
            "location": location,
        }
        if health_checked_targets is not None:
            self._values["health_checked_targets"] = health_checked_targets
        if rrdatas is not None:
            self._values["rrdatas"] = rrdatas

    @builtins.property
    def location(self) -> builtins.str:
        '''The location name defined in Google Cloud.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#location DnsRecordSet#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def health_checked_targets(
        self,
    ) -> typing.Optional["DnsRecordSetRoutingPolicyGeoHealthCheckedTargets"]:
        '''health_checked_targets block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        '''
        result = self._values.get("health_checked_targets")
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyGeoHealthCheckedTargets"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#rrdatas DnsRecordSet#rrdatas}.'''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyGeo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoHealthCheckedTargets",
    jsii_struct_bases=[],
    name_mapping={"internal_load_balancers": "internalLoadBalancers"},
)
class DnsRecordSetRoutingPolicyGeoHealthCheckedTargets:
    def __init__(
        self,
        *,
        internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            def stub(
                *,
                internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument internal_load_balancers", value=internal_load_balancers, expected_type=type_hints["internal_load_balancers"])
        self._values: typing.Dict[str, typing.Any] = {
            "internal_load_balancers": internal_load_balancers,
        }

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers"]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        assert result is not None, "Required property 'internal_load_balancers' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyGeoHealthCheckedTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address": "ipAddress",
        "ip_protocol": "ipProtocol",
        "load_balancer_type": "loadBalancerType",
        "network_url": "networkUrl",
        "port": "port",
        "project": "project",
        "region": "region",
    },
)
class DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers:
    def __init__(
        self,
        *,
        ip_address: builtins.str,
        ip_protocol: builtins.str,
        load_balancer_type: builtins.str,
        network_url: builtins.str,
        port: builtins.str,
        project: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_address DnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#network_url DnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#port DnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#project DnsRecordSet#project}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#region DnsRecordSet#region}
        '''
        if __debug__:
            def stub(
                *,
                ip_address: builtins.str,
                ip_protocol: builtins.str,
                load_balancer_type: builtins.str,
                network_url: builtins.str,
                port: builtins.str,
                project: builtins.str,
                region: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[str, typing.Any] = {
            "ip_address": ip_address,
            "ip_protocol": ip_protocol,
            "load_balancer_type": load_balancer_type,
            "network_url": network_url,
            "port": port,
            "project": project,
        }
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The frontend IP address of the load balancer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_address DnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> builtins.str:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        assert result is not None, "Required property 'load_balancer_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#network_url DnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#port DnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#project DnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#region DnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList",
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
    ) -> "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
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

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerTypeInput")
    def load_balancer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value)

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

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

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference",
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

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInternalLoadBalancers", [value]))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancers")
    def internal_load_balancers(
        self,
    ) -> DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList:
        return typing.cast(DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyGeoList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoList",
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
    def get(self, index: jsii.Number) -> "DnsRecordSetRoutingPolicyGeoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyGeoOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyGeoOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoOutputReference",
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

    @jsii.member(jsii_name="putHealthCheckedTargets")
    def put_health_checked_targets(
        self,
        *,
        internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        value = DnsRecordSetRoutingPolicyGeoHealthCheckedTargets(
            internal_load_balancers=internal_load_balancers
        )

        return typing.cast(None, jsii.invoke(self, "putHealthCheckedTargets", [value]))

    @jsii.member(jsii_name="resetHealthCheckedTargets")
    def reset_health_checked_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckedTargets", []))

    @jsii.member(jsii_name="resetRrdatas")
    def reset_rrdatas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRrdatas", []))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargets")
    def health_checked_targets(
        self,
    ) -> DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference:
        return typing.cast(DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference, jsii.get(self, "healthCheckedTargets"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargetsInput")
    def health_checked_targets_input(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets], jsii.get(self, "healthCheckedTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="rrdatasInput")
    def rrdatas_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rrdatasInput"))

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
    @jsii.member(jsii_name="rrdatas")
    def rrdatas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rrdatas"))

    @rrdatas.setter
    def rrdatas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DnsRecordSetRoutingPolicyGeo, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DnsRecordSetRoutingPolicyGeo, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyGeo, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyGeo, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyOutputReference",
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

    @jsii.member(jsii_name="putGeo")
    def put_geo(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeo, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeo, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGeo", [value]))

    @jsii.member(jsii_name="putPrimaryBackup")
    def put_primary_backup(
        self,
        *,
        backup_geo: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo", typing.Dict[str, typing.Any]]]],
        primary: typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupPrimary", typing.Dict[str, typing.Any]],
        enable_geo_fencing_for_backups: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        trickle_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_geo: backup_geo block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#backup_geo DnsRecordSet#backup_geo}
        :param primary: primary block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#primary DnsRecordSet#primary}
        :param enable_geo_fencing_for_backups: Specifies whether to enable fencing for backup geo queries. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#enable_geo_fencing_for_backups DnsRecordSet#enable_geo_fencing_for_backups}
        :param trickle_ratio: Specifies the percentage of traffic to send to the backup targets even when the primary targets are healthy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#trickle_ratio DnsRecordSet#trickle_ratio}
        '''
        value = DnsRecordSetRoutingPolicyPrimaryBackup(
            backup_geo=backup_geo,
            primary=primary,
            enable_geo_fencing_for_backups=enable_geo_fencing_for_backups,
            trickle_ratio=trickle_ratio,
        )

        return typing.cast(None, jsii.invoke(self, "putPrimaryBackup", [value]))

    @jsii.member(jsii_name="putWrr")
    def put_wrr(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyWrr", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrr, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWrr", [value]))

    @jsii.member(jsii_name="resetEnableGeoFencing")
    def reset_enable_geo_fencing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableGeoFencing", []))

    @jsii.member(jsii_name="resetGeo")
    def reset_geo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeo", []))

    @jsii.member(jsii_name="resetPrimaryBackup")
    def reset_primary_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryBackup", []))

    @jsii.member(jsii_name="resetWrr")
    def reset_wrr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWrr", []))

    @builtins.property
    @jsii.member(jsii_name="geo")
    def geo(self) -> DnsRecordSetRoutingPolicyGeoList:
        return typing.cast(DnsRecordSetRoutingPolicyGeoList, jsii.get(self, "geo"))

    @builtins.property
    @jsii.member(jsii_name="primaryBackup")
    def primary_backup(self) -> "DnsRecordSetRoutingPolicyPrimaryBackupOutputReference":
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupOutputReference", jsii.get(self, "primaryBackup"))

    @builtins.property
    @jsii.member(jsii_name="wrr")
    def wrr(self) -> "DnsRecordSetRoutingPolicyWrrList":
        return typing.cast("DnsRecordSetRoutingPolicyWrrList", jsii.get(self, "wrr"))

    @builtins.property
    @jsii.member(jsii_name="enableGeoFencingInput")
    def enable_geo_fencing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enableGeoFencingInput"))

    @builtins.property
    @jsii.member(jsii_name="geoInput")
    def geo_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]], jsii.get(self, "geoInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryBackupInput")
    def primary_backup_input(
        self,
    ) -> typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackup"]:
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackup"], jsii.get(self, "primaryBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="wrrInput")
    def wrr_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrr"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrr"]]], jsii.get(self, "wrrInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGeoFencing")
    def enable_geo_fencing(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enableGeoFencing"))

    @enable_geo_fencing.setter
    def enable_geo_fencing(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableGeoFencing", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsRecordSetRoutingPolicy]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DnsRecordSetRoutingPolicy]) -> None:
        if __debug__:
            def stub(value: typing.Optional[DnsRecordSetRoutingPolicy]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackup",
    jsii_struct_bases=[],
    name_mapping={
        "backup_geo": "backupGeo",
        "primary": "primary",
        "enable_geo_fencing_for_backups": "enableGeoFencingForBackups",
        "trickle_ratio": "trickleRatio",
    },
)
class DnsRecordSetRoutingPolicyPrimaryBackup:
    def __init__(
        self,
        *,
        backup_geo: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo", typing.Dict[str, typing.Any]]]],
        primary: typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupPrimary", typing.Dict[str, typing.Any]],
        enable_geo_fencing_for_backups: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        trickle_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_geo: backup_geo block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#backup_geo DnsRecordSet#backup_geo}
        :param primary: primary block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#primary DnsRecordSet#primary}
        :param enable_geo_fencing_for_backups: Specifies whether to enable fencing for backup geo queries. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#enable_geo_fencing_for_backups DnsRecordSet#enable_geo_fencing_for_backups}
        :param trickle_ratio: Specifies the percentage of traffic to send to the backup targets even when the primary targets are healthy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#trickle_ratio DnsRecordSet#trickle_ratio}
        '''
        if isinstance(primary, dict):
            primary = DnsRecordSetRoutingPolicyPrimaryBackupPrimary(**primary)
        if __debug__:
            def stub(
                *,
                backup_geo: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, typing.Dict[str, typing.Any]]]],
                primary: typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimary, typing.Dict[str, typing.Any]],
                enable_geo_fencing_for_backups: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                trickle_ratio: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument backup_geo", value=backup_geo, expected_type=type_hints["backup_geo"])
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
            check_type(argname="argument enable_geo_fencing_for_backups", value=enable_geo_fencing_for_backups, expected_type=type_hints["enable_geo_fencing_for_backups"])
            check_type(argname="argument trickle_ratio", value=trickle_ratio, expected_type=type_hints["trickle_ratio"])
        self._values: typing.Dict[str, typing.Any] = {
            "backup_geo": backup_geo,
            "primary": primary,
        }
        if enable_geo_fencing_for_backups is not None:
            self._values["enable_geo_fencing_for_backups"] = enable_geo_fencing_for_backups
        if trickle_ratio is not None:
            self._values["trickle_ratio"] = trickle_ratio

    @builtins.property
    def backup_geo(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo"]]:
        '''backup_geo block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#backup_geo DnsRecordSet#backup_geo}
        '''
        result = self._values.get("backup_geo")
        assert result is not None, "Required property 'backup_geo' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo"]], result)

    @builtins.property
    def primary(self) -> "DnsRecordSetRoutingPolicyPrimaryBackupPrimary":
        '''primary block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#primary DnsRecordSet#primary}
        '''
        result = self._values.get("primary")
        assert result is not None, "Required property 'primary' is missing"
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupPrimary", result)

    @builtins.property
    def enable_geo_fencing_for_backups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Specifies whether to enable fencing for backup geo queries.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#enable_geo_fencing_for_backups DnsRecordSet#enable_geo_fencing_for_backups}
        '''
        result = self._values.get("enable_geo_fencing_for_backups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def trickle_ratio(self) -> typing.Optional[jsii.Number]:
        '''Specifies the percentage of traffic to send to the backup targets even when the primary targets are healthy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#trickle_ratio DnsRecordSet#trickle_ratio}
        '''
        result = self._values.get("trickle_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "health_checked_targets": "healthCheckedTargets",
        "rrdatas": "rrdatas",
    },
)
class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo:
    def __init__(
        self,
        *,
        location: builtins.str,
        health_checked_targets: typing.Optional[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets", typing.Dict[str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: The location name defined in Google Cloud. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#location DnsRecordSet#location}
        :param health_checked_targets: health_checked_targets block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        :param rrdatas: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#rrdatas DnsRecordSet#rrdatas}.
        '''
        if isinstance(health_checked_targets, dict):
            health_checked_targets = DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets(**health_checked_targets)
        if __debug__:
            def stub(
                *,
                location: builtins.str,
                health_checked_targets: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets, typing.Dict[str, typing.Any]]] = None,
                rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument health_checked_targets", value=health_checked_targets, expected_type=type_hints["health_checked_targets"])
            check_type(argname="argument rrdatas", value=rrdatas, expected_type=type_hints["rrdatas"])
        self._values: typing.Dict[str, typing.Any] = {
            "location": location,
        }
        if health_checked_targets is not None:
            self._values["health_checked_targets"] = health_checked_targets
        if rrdatas is not None:
            self._values["rrdatas"] = rrdatas

    @builtins.property
    def location(self) -> builtins.str:
        '''The location name defined in Google Cloud.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#location DnsRecordSet#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def health_checked_targets(
        self,
    ) -> typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets"]:
        '''health_checked_targets block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        '''
        result = self._values.get("health_checked_targets")
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#rrdatas DnsRecordSet#rrdatas}.'''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets",
    jsii_struct_bases=[],
    name_mapping={"internal_load_balancers": "internalLoadBalancers"},
)
class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets:
    def __init__(
        self,
        *,
        internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            def stub(
                *,
                internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument internal_load_balancers", value=internal_load_balancers, expected_type=type_hints["internal_load_balancers"])
        self._values: typing.Dict[str, typing.Any] = {
            "internal_load_balancers": internal_load_balancers,
        }

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers"]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        assert result is not None, "Required property 'internal_load_balancers' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address": "ipAddress",
        "ip_protocol": "ipProtocol",
        "load_balancer_type": "loadBalancerType",
        "network_url": "networkUrl",
        "port": "port",
        "project": "project",
        "region": "region",
    },
)
class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers:
    def __init__(
        self,
        *,
        ip_address: builtins.str,
        ip_protocol: builtins.str,
        load_balancer_type: builtins.str,
        network_url: builtins.str,
        port: builtins.str,
        project: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_address DnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#network_url DnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#port DnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#project DnsRecordSet#project}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#region DnsRecordSet#region}
        '''
        if __debug__:
            def stub(
                *,
                ip_address: builtins.str,
                ip_protocol: builtins.str,
                load_balancer_type: builtins.str,
                network_url: builtins.str,
                port: builtins.str,
                project: builtins.str,
                region: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[str, typing.Any] = {
            "ip_address": ip_address,
            "ip_protocol": ip_protocol,
            "load_balancer_type": load_balancer_type,
            "network_url": network_url,
            "port": port,
            "project": project,
        }
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The frontend IP address of the load balancer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_address DnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> builtins.str:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        assert result is not None, "Required property 'load_balancer_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#network_url DnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#port DnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#project DnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#region DnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList",
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
    ) -> "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
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

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerTypeInput")
    def load_balancer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value)

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

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

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference",
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

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInternalLoadBalancers", [value]))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancers")
    def internal_load_balancers(
        self,
    ) -> DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList:
        return typing.cast(DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList",
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
    ) -> "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference",
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

    @jsii.member(jsii_name="putHealthCheckedTargets")
    def put_health_checked_targets(
        self,
        *,
        internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        value = DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets(
            internal_load_balancers=internal_load_balancers
        )

        return typing.cast(None, jsii.invoke(self, "putHealthCheckedTargets", [value]))

    @jsii.member(jsii_name="resetHealthCheckedTargets")
    def reset_health_checked_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckedTargets", []))

    @jsii.member(jsii_name="resetRrdatas")
    def reset_rrdatas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRrdatas", []))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargets")
    def health_checked_targets(
        self,
    ) -> DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference:
        return typing.cast(DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference, jsii.get(self, "healthCheckedTargets"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargetsInput")
    def health_checked_targets_input(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets], jsii.get(self, "healthCheckedTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="rrdatasInput")
    def rrdatas_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rrdatasInput"))

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
    @jsii.member(jsii_name="rrdatas")
    def rrdatas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rrdatas"))

    @rrdatas.setter
    def rrdatas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyPrimaryBackupOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupOutputReference",
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

    @jsii.member(jsii_name="putBackupGeo")
    def put_backup_geo(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackupGeo", [value]))

    @jsii.member(jsii_name="putPrimary")
    def put_primary(
        self,
        *,
        internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        value = DnsRecordSetRoutingPolicyPrimaryBackupPrimary(
            internal_load_balancers=internal_load_balancers
        )

        return typing.cast(None, jsii.invoke(self, "putPrimary", [value]))

    @jsii.member(jsii_name="resetEnableGeoFencingForBackups")
    def reset_enable_geo_fencing_for_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableGeoFencingForBackups", []))

    @jsii.member(jsii_name="resetTrickleRatio")
    def reset_trickle_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrickleRatio", []))

    @builtins.property
    @jsii.member(jsii_name="backupGeo")
    def backup_geo(self) -> DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList:
        return typing.cast(DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList, jsii.get(self, "backupGeo"))

    @builtins.property
    @jsii.member(jsii_name="primary")
    def primary(self) -> "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference":
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference", jsii.get(self, "primary"))

    @builtins.property
    @jsii.member(jsii_name="backupGeoInput")
    def backup_geo_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]], jsii.get(self, "backupGeoInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGeoFencingForBackupsInput")
    def enable_geo_fencing_for_backups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enableGeoFencingForBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryInput")
    def primary_input(
        self,
    ) -> typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackupPrimary"]:
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackupPrimary"], jsii.get(self, "primaryInput"))

    @builtins.property
    @jsii.member(jsii_name="trickleRatioInput")
    def trickle_ratio_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "trickleRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGeoFencingForBackups")
    def enable_geo_fencing_for_backups(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enableGeoFencingForBackups"))

    @enable_geo_fencing_for_backups.setter
    def enable_geo_fencing_for_backups(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableGeoFencingForBackups", value)

    @builtins.property
    @jsii.member(jsii_name="trickleRatio")
    def trickle_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "trickleRatio"))

    @trickle_ratio.setter
    def trickle_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trickleRatio", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackup]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackup],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackup],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupPrimary",
    jsii_struct_bases=[],
    name_mapping={"internal_load_balancers": "internalLoadBalancers"},
)
class DnsRecordSetRoutingPolicyPrimaryBackupPrimary:
    def __init__(
        self,
        *,
        internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            def stub(
                *,
                internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument internal_load_balancers", value=internal_load_balancers, expected_type=type_hints["internal_load_balancers"])
        self._values: typing.Dict[str, typing.Any] = {
            "internal_load_balancers": internal_load_balancers,
        }

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers"]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        assert result is not None, "Required property 'internal_load_balancers' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackupPrimary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address": "ipAddress",
        "ip_protocol": "ipProtocol",
        "load_balancer_type": "loadBalancerType",
        "network_url": "networkUrl",
        "port": "port",
        "project": "project",
        "region": "region",
    },
)
class DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers:
    def __init__(
        self,
        *,
        ip_address: builtins.str,
        ip_protocol: builtins.str,
        load_balancer_type: builtins.str,
        network_url: builtins.str,
        port: builtins.str,
        project: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_address DnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#network_url DnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#port DnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#project DnsRecordSet#project}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#region DnsRecordSet#region}
        '''
        if __debug__:
            def stub(
                *,
                ip_address: builtins.str,
                ip_protocol: builtins.str,
                load_balancer_type: builtins.str,
                network_url: builtins.str,
                port: builtins.str,
                project: builtins.str,
                region: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[str, typing.Any] = {
            "ip_address": ip_address,
            "ip_protocol": ip_protocol,
            "load_balancer_type": load_balancer_type,
            "network_url": network_url,
            "port": port,
            "project": project,
        }
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The frontend IP address of the load balancer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_address DnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> builtins.str:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        assert result is not None, "Required property 'load_balancer_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#network_url DnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#port DnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#project DnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#region DnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList",
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
    ) -> "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference",
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

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerTypeInput")
    def load_balancer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value)

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

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

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference",
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

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInternalLoadBalancers", [value]))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancers")
    def internal_load_balancers(
        self,
    ) -> DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList:
        return typing.cast(DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupPrimary]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupPrimary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupPrimary],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupPrimary],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrr",
    jsii_struct_bases=[],
    name_mapping={
        "weight": "weight",
        "health_checked_targets": "healthCheckedTargets",
        "rrdatas": "rrdatas",
    },
)
class DnsRecordSetRoutingPolicyWrr:
    def __init__(
        self,
        *,
        weight: jsii.Number,
        health_checked_targets: typing.Optional[typing.Union["DnsRecordSetRoutingPolicyWrrHealthCheckedTargets", typing.Dict[str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param weight: The ratio of traffic routed to the target. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#weight DnsRecordSet#weight}
        :param health_checked_targets: health_checked_targets block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        :param rrdatas: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#rrdatas DnsRecordSet#rrdatas}.
        '''
        if isinstance(health_checked_targets, dict):
            health_checked_targets = DnsRecordSetRoutingPolicyWrrHealthCheckedTargets(**health_checked_targets)
        if __debug__:
            def stub(
                *,
                weight: jsii.Number,
                health_checked_targets: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets, typing.Dict[str, typing.Any]]] = None,
                rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            check_type(argname="argument health_checked_targets", value=health_checked_targets, expected_type=type_hints["health_checked_targets"])
            check_type(argname="argument rrdatas", value=rrdatas, expected_type=type_hints["rrdatas"])
        self._values: typing.Dict[str, typing.Any] = {
            "weight": weight,
        }
        if health_checked_targets is not None:
            self._values["health_checked_targets"] = health_checked_targets
        if rrdatas is not None:
            self._values["rrdatas"] = rrdatas

    @builtins.property
    def weight(self) -> jsii.Number:
        '''The ratio of traffic routed to the target.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#weight DnsRecordSet#weight}
        '''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def health_checked_targets(
        self,
    ) -> typing.Optional["DnsRecordSetRoutingPolicyWrrHealthCheckedTargets"]:
        '''health_checked_targets block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        '''
        result = self._values.get("health_checked_targets")
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyWrrHealthCheckedTargets"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#rrdatas DnsRecordSet#rrdatas}.'''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyWrr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrHealthCheckedTargets",
    jsii_struct_bases=[],
    name_mapping={"internal_load_balancers": "internalLoadBalancers"},
)
class DnsRecordSetRoutingPolicyWrrHealthCheckedTargets:
    def __init__(
        self,
        *,
        internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            def stub(
                *,
                internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument internal_load_balancers", value=internal_load_balancers, expected_type=type_hints["internal_load_balancers"])
        self._values: typing.Dict[str, typing.Any] = {
            "internal_load_balancers": internal_load_balancers,
        }

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers"]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        assert result is not None, "Required property 'internal_load_balancers' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyWrrHealthCheckedTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address": "ipAddress",
        "ip_protocol": "ipProtocol",
        "load_balancer_type": "loadBalancerType",
        "network_url": "networkUrl",
        "port": "port",
        "project": "project",
        "region": "region",
    },
)
class DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers:
    def __init__(
        self,
        *,
        ip_address: builtins.str,
        ip_protocol: builtins.str,
        load_balancer_type: builtins.str,
        network_url: builtins.str,
        port: builtins.str,
        project: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_address DnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#network_url DnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#port DnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#project DnsRecordSet#project}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#region DnsRecordSet#region}
        '''
        if __debug__:
            def stub(
                *,
                ip_address: builtins.str,
                ip_protocol: builtins.str,
                load_balancer_type: builtins.str,
                network_url: builtins.str,
                port: builtins.str,
                project: builtins.str,
                region: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[str, typing.Any] = {
            "ip_address": ip_address,
            "ip_protocol": ip_protocol,
            "load_balancer_type": load_balancer_type,
            "network_url": network_url,
            "port": port,
            "project": project,
        }
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The frontend IP address of the load balancer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_address DnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> builtins.str:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        assert result is not None, "Required property 'load_balancer_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#network_url DnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#port DnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#project DnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#region DnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList",
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
    ) -> "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference",
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

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerTypeInput")
    def load_balancer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value)

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

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

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference",
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

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInternalLoadBalancers", [value]))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancers")
    def internal_load_balancers(
        self,
    ) -> DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList:
        return typing.cast(DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyWrrList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrList",
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
    def get(self, index: jsii.Number) -> "DnsRecordSetRoutingPolicyWrrOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyWrrOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrr]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrr]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrr]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrr]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DnsRecordSetRoutingPolicyWrrOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrOutputReference",
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

    @jsii.member(jsii_name="putHealthCheckedTargets")
    def put_health_checked_targets(
        self,
        *,
        internal_load_balancers: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        value = DnsRecordSetRoutingPolicyWrrHealthCheckedTargets(
            internal_load_balancers=internal_load_balancers
        )

        return typing.cast(None, jsii.invoke(self, "putHealthCheckedTargets", [value]))

    @jsii.member(jsii_name="resetHealthCheckedTargets")
    def reset_health_checked_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckedTargets", []))

    @jsii.member(jsii_name="resetRrdatas")
    def reset_rrdatas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRrdatas", []))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargets")
    def health_checked_targets(
        self,
    ) -> DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference:
        return typing.cast(DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference, jsii.get(self, "healthCheckedTargets"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargetsInput")
    def health_checked_targets_input(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets], jsii.get(self, "healthCheckedTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="rrdatasInput")
    def rrdatas_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rrdatasInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="rrdatas")
    def rrdatas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rrdatas"))

    @rrdatas.setter
    def rrdatas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value)

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DnsRecordSetRoutingPolicyWrr, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DnsRecordSetRoutingPolicyWrr, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyWrr, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyWrr, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DnsRecordSet",
    "DnsRecordSetConfig",
    "DnsRecordSetRoutingPolicy",
    "DnsRecordSetRoutingPolicyGeo",
    "DnsRecordSetRoutingPolicyGeoHealthCheckedTargets",
    "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers",
    "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList",
    "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
    "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference",
    "DnsRecordSetRoutingPolicyGeoList",
    "DnsRecordSetRoutingPolicyGeoOutputReference",
    "DnsRecordSetRoutingPolicyOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackup",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackupOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackupPrimary",
    "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers",
    "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList",
    "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference",
    "DnsRecordSetRoutingPolicyWrr",
    "DnsRecordSetRoutingPolicyWrrHealthCheckedTargets",
    "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers",
    "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList",
    "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference",
    "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference",
    "DnsRecordSetRoutingPolicyWrrList",
    "DnsRecordSetRoutingPolicyWrrOutputReference",
]

publication.publish()
