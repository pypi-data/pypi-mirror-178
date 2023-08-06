'''
# `google_identity_platform_project_default_config`

Refer to the Terraform Registory for docs: [`google_identity_platform_project_default_config`](https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config).
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


class IdentityPlatformProjectDefaultConfig(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfig",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config google_identity_platform_project_default_config}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        sign_in: typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigSignIn", typing.Dict[str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config google_identity_platform_project_default_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#id IdentityPlatformProjectDefaultConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#project IdentityPlatformProjectDefaultConfig#project}.
        :param sign_in: sign_in block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#sign_in IdentityPlatformProjectDefaultConfig#sign_in}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#timeouts IdentityPlatformProjectDefaultConfig#timeouts}
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
                id: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                sign_in: typing.Optional[typing.Union[IdentityPlatformProjectDefaultConfigSignIn, typing.Dict[str, typing.Any]]] = None,
                timeouts: typing.Optional[typing.Union[IdentityPlatformProjectDefaultConfigTimeouts, typing.Dict[str, typing.Any]]] = None,
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
        config = IdentityPlatformProjectDefaultConfigConfig(
            id=id,
            project=project,
            sign_in=sign_in,
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

    @jsii.member(jsii_name="putSignIn")
    def put_sign_in(
        self,
        *,
        allow_duplicate_emails: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        anonymous: typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigSignInAnonymous", typing.Dict[str, typing.Any]]] = None,
        email: typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigSignInEmail", typing.Dict[str, typing.Any]]] = None,
        phone_number: typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigSignInPhoneNumber", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_duplicate_emails: Whether to allow more than one account to have the same email. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#allow_duplicate_emails IdentityPlatformProjectDefaultConfig#allow_duplicate_emails}
        :param anonymous: anonymous block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#anonymous IdentityPlatformProjectDefaultConfig#anonymous}
        :param email: email block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#email IdentityPlatformProjectDefaultConfig#email}
        :param phone_number: phone_number block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#phone_number IdentityPlatformProjectDefaultConfig#phone_number}
        '''
        value = IdentityPlatformProjectDefaultConfigSignIn(
            allow_duplicate_emails=allow_duplicate_emails,
            anonymous=anonymous,
            email=email,
            phone_number=phone_number,
        )

        return typing.cast(None, jsii.invoke(self, "putSignIn", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#create IdentityPlatformProjectDefaultConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#delete IdentityPlatformProjectDefaultConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#update IdentityPlatformProjectDefaultConfig#update}.
        '''
        value = IdentityPlatformProjectDefaultConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSignIn")
    def reset_sign_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignIn", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="signIn")
    def sign_in(self) -> "IdentityPlatformProjectDefaultConfigSignInOutputReference":
        return typing.cast("IdentityPlatformProjectDefaultConfigSignInOutputReference", jsii.get(self, "signIn"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "IdentityPlatformProjectDefaultConfigTimeoutsOutputReference":
        return typing.cast("IdentityPlatformProjectDefaultConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="signInInput")
    def sign_in_input(
        self,
    ) -> typing.Optional["IdentityPlatformProjectDefaultConfigSignIn"]:
        return typing.cast(typing.Optional["IdentityPlatformProjectDefaultConfigSignIn"], jsii.get(self, "signInInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

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
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "project": "project",
        "sign_in": "signIn",
        "timeouts": "timeouts",
    },
)
class IdentityPlatformProjectDefaultConfigConfig(cdktf.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        sign_in: typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigSignIn", typing.Dict[str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#id IdentityPlatformProjectDefaultConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#project IdentityPlatformProjectDefaultConfig#project}.
        :param sign_in: sign_in block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#sign_in IdentityPlatformProjectDefaultConfig#sign_in}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#timeouts IdentityPlatformProjectDefaultConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(sign_in, dict):
            sign_in = IdentityPlatformProjectDefaultConfigSignIn(**sign_in)
        if isinstance(timeouts, dict):
            timeouts = IdentityPlatformProjectDefaultConfigTimeouts(**timeouts)
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
                id: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                sign_in: typing.Optional[typing.Union[IdentityPlatformProjectDefaultConfigSignIn, typing.Dict[str, typing.Any]]] = None,
                timeouts: typing.Optional[typing.Union[IdentityPlatformProjectDefaultConfigTimeouts, typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument sign_in", value=sign_in, expected_type=type_hints["sign_in"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {}
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
        if sign_in is not None:
            self._values["sign_in"] = sign_in
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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#id IdentityPlatformProjectDefaultConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#project IdentityPlatformProjectDefaultConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sign_in(self) -> typing.Optional["IdentityPlatformProjectDefaultConfigSignIn"]:
        '''sign_in block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#sign_in IdentityPlatformProjectDefaultConfig#sign_in}
        '''
        result = self._values.get("sign_in")
        return typing.cast(typing.Optional["IdentityPlatformProjectDefaultConfigSignIn"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["IdentityPlatformProjectDefaultConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#timeouts IdentityPlatformProjectDefaultConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IdentityPlatformProjectDefaultConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformProjectDefaultConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigSignIn",
    jsii_struct_bases=[],
    name_mapping={
        "allow_duplicate_emails": "allowDuplicateEmails",
        "anonymous": "anonymous",
        "email": "email",
        "phone_number": "phoneNumber",
    },
)
class IdentityPlatformProjectDefaultConfigSignIn:
    def __init__(
        self,
        *,
        allow_duplicate_emails: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        anonymous: typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigSignInAnonymous", typing.Dict[str, typing.Any]]] = None,
        email: typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigSignInEmail", typing.Dict[str, typing.Any]]] = None,
        phone_number: typing.Optional[typing.Union["IdentityPlatformProjectDefaultConfigSignInPhoneNumber", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_duplicate_emails: Whether to allow more than one account to have the same email. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#allow_duplicate_emails IdentityPlatformProjectDefaultConfig#allow_duplicate_emails}
        :param anonymous: anonymous block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#anonymous IdentityPlatformProjectDefaultConfig#anonymous}
        :param email: email block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#email IdentityPlatformProjectDefaultConfig#email}
        :param phone_number: phone_number block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#phone_number IdentityPlatformProjectDefaultConfig#phone_number}
        '''
        if isinstance(anonymous, dict):
            anonymous = IdentityPlatformProjectDefaultConfigSignInAnonymous(**anonymous)
        if isinstance(email, dict):
            email = IdentityPlatformProjectDefaultConfigSignInEmail(**email)
        if isinstance(phone_number, dict):
            phone_number = IdentityPlatformProjectDefaultConfigSignInPhoneNumber(**phone_number)
        if __debug__:
            def stub(
                *,
                allow_duplicate_emails: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                anonymous: typing.Optional[typing.Union[IdentityPlatformProjectDefaultConfigSignInAnonymous, typing.Dict[str, typing.Any]]] = None,
                email: typing.Optional[typing.Union[IdentityPlatformProjectDefaultConfigSignInEmail, typing.Dict[str, typing.Any]]] = None,
                phone_number: typing.Optional[typing.Union[IdentityPlatformProjectDefaultConfigSignInPhoneNumber, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument allow_duplicate_emails", value=allow_duplicate_emails, expected_type=type_hints["allow_duplicate_emails"])
            check_type(argname="argument anonymous", value=anonymous, expected_type=type_hints["anonymous"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[str, typing.Any] = {}
        if allow_duplicate_emails is not None:
            self._values["allow_duplicate_emails"] = allow_duplicate_emails
        if anonymous is not None:
            self._values["anonymous"] = anonymous
        if email is not None:
            self._values["email"] = email
        if phone_number is not None:
            self._values["phone_number"] = phone_number

    @builtins.property
    def allow_duplicate_emails(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Whether to allow more than one account to have the same email.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#allow_duplicate_emails IdentityPlatformProjectDefaultConfig#allow_duplicate_emails}
        '''
        result = self._values.get("allow_duplicate_emails")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def anonymous(
        self,
    ) -> typing.Optional["IdentityPlatformProjectDefaultConfigSignInAnonymous"]:
        '''anonymous block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#anonymous IdentityPlatformProjectDefaultConfig#anonymous}
        '''
        result = self._values.get("anonymous")
        return typing.cast(typing.Optional["IdentityPlatformProjectDefaultConfigSignInAnonymous"], result)

    @builtins.property
    def email(
        self,
    ) -> typing.Optional["IdentityPlatformProjectDefaultConfigSignInEmail"]:
        '''email block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#email IdentityPlatformProjectDefaultConfig#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional["IdentityPlatformProjectDefaultConfigSignInEmail"], result)

    @builtins.property
    def phone_number(
        self,
    ) -> typing.Optional["IdentityPlatformProjectDefaultConfigSignInPhoneNumber"]:
        '''phone_number block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#phone_number IdentityPlatformProjectDefaultConfig#phone_number}
        '''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional["IdentityPlatformProjectDefaultConfigSignInPhoneNumber"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformProjectDefaultConfigSignIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigSignInAnonymous",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class IdentityPlatformProjectDefaultConfigSignInAnonymous:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether anonymous user auth is enabled for the project or not. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#enabled IdentityPlatformProjectDefaultConfig#enabled}
        '''
        if __debug__:
            def stub(
                *,
                enabled: typing.Union[builtins.bool, cdktf.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        '''Whether anonymous user auth is enabled for the project or not.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#enabled IdentityPlatformProjectDefaultConfig#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformProjectDefaultConfigSignInAnonymous(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformProjectDefaultConfigSignInAnonymousOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigSignInAnonymousOutputReference",
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
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IdentityPlatformProjectDefaultConfigSignInAnonymous]:
        return typing.cast(typing.Optional[IdentityPlatformProjectDefaultConfigSignInAnonymous], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityPlatformProjectDefaultConfigSignInAnonymous],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[IdentityPlatformProjectDefaultConfigSignInAnonymous],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigSignInEmail",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "password_required": "passwordRequired"},
)
class IdentityPlatformProjectDefaultConfigSignInEmail:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        password_required: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether email auth is enabled for the project or not. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#enabled IdentityPlatformProjectDefaultConfig#enabled}
        :param password_required: Whether a password is required for email auth or not. If true, both an email and password must be provided to sign in. If false, a user may sign in via either email/password or email link. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#password_required IdentityPlatformProjectDefaultConfig#password_required}
        '''
        if __debug__:
            def stub(
                *,
                enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                password_required: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument password_required", value=password_required, expected_type=type_hints["password_required"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if password_required is not None:
            self._values["password_required"] = password_required

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Whether email auth is enabled for the project or not.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#enabled IdentityPlatformProjectDefaultConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def password_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Whether a password is required for email auth or not.

        If true, both an email and
        password must be provided to sign in. If false, a user may sign in via either
        email/password or email link.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#password_required IdentityPlatformProjectDefaultConfig#password_required}
        '''
        result = self._values.get("password_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformProjectDefaultConfigSignInEmail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformProjectDefaultConfigSignInEmailOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigSignInEmailOutputReference",
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

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetPasswordRequired")
    def reset_password_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordRequired", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordRequiredInput")
    def password_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "passwordRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="passwordRequired")
    def password_required(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "passwordRequired"))

    @password_required.setter
    def password_required(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordRequired", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IdentityPlatformProjectDefaultConfigSignInEmail]:
        return typing.cast(typing.Optional[IdentityPlatformProjectDefaultConfigSignInEmail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityPlatformProjectDefaultConfigSignInEmail],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[IdentityPlatformProjectDefaultConfigSignInEmail],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigSignInHashConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class IdentityPlatformProjectDefaultConfigSignInHashConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformProjectDefaultConfigSignInHashConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformProjectDefaultConfigSignInHashConfigList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigSignInHashConfigList",
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
    ) -> "IdentityPlatformProjectDefaultConfigSignInHashConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IdentityPlatformProjectDefaultConfigSignInHashConfigOutputReference", jsii.invoke(self, "get", [index]))

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


class IdentityPlatformProjectDefaultConfigSignInHashConfigOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigSignInHashConfigOutputReference",
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
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @builtins.property
    @jsii.member(jsii_name="memoryCost")
    def memory_cost(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryCost"))

    @builtins.property
    @jsii.member(jsii_name="rounds")
    def rounds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rounds"))

    @builtins.property
    @jsii.member(jsii_name="saltSeparator")
    def salt_separator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saltSeparator"))

    @builtins.property
    @jsii.member(jsii_name="signerKey")
    def signer_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signerKey"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IdentityPlatformProjectDefaultConfigSignInHashConfig]:
        return typing.cast(typing.Optional[IdentityPlatformProjectDefaultConfigSignInHashConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityPlatformProjectDefaultConfigSignInHashConfig],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[IdentityPlatformProjectDefaultConfigSignInHashConfig],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class IdentityPlatformProjectDefaultConfigSignInOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigSignInOutputReference",
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

    @jsii.member(jsii_name="putAnonymous")
    def put_anonymous(
        self,
        *,
        enabled: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether anonymous user auth is enabled for the project or not. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#enabled IdentityPlatformProjectDefaultConfig#enabled}
        '''
        value = IdentityPlatformProjectDefaultConfigSignInAnonymous(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAnonymous", [value]))

    @jsii.member(jsii_name="putEmail")
    def put_email(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        password_required: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether email auth is enabled for the project or not. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#enabled IdentityPlatformProjectDefaultConfig#enabled}
        :param password_required: Whether a password is required for email auth or not. If true, both an email and password must be provided to sign in. If false, a user may sign in via either email/password or email link. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#password_required IdentityPlatformProjectDefaultConfig#password_required}
        '''
        value = IdentityPlatformProjectDefaultConfigSignInEmail(
            enabled=enabled, password_required=password_required
        )

        return typing.cast(None, jsii.invoke(self, "putEmail", [value]))

    @jsii.member(jsii_name="putPhoneNumber")
    def put_phone_number(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        test_phone_numbers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Whether phone number auth is enabled for the project or not. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#enabled IdentityPlatformProjectDefaultConfig#enabled}
        :param test_phone_numbers: A map of <test phone number, fake code> that can be used for phone auth testing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#test_phone_numbers IdentityPlatformProjectDefaultConfig#test_phone_numbers}
        '''
        value = IdentityPlatformProjectDefaultConfigSignInPhoneNumber(
            enabled=enabled, test_phone_numbers=test_phone_numbers
        )

        return typing.cast(None, jsii.invoke(self, "putPhoneNumber", [value]))

    @jsii.member(jsii_name="resetAllowDuplicateEmails")
    def reset_allow_duplicate_emails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowDuplicateEmails", []))

    @jsii.member(jsii_name="resetAnonymous")
    def reset_anonymous(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnonymous", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @builtins.property
    @jsii.member(jsii_name="anonymous")
    def anonymous(
        self,
    ) -> IdentityPlatformProjectDefaultConfigSignInAnonymousOutputReference:
        return typing.cast(IdentityPlatformProjectDefaultConfigSignInAnonymousOutputReference, jsii.get(self, "anonymous"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> IdentityPlatformProjectDefaultConfigSignInEmailOutputReference:
        return typing.cast(IdentityPlatformProjectDefaultConfigSignInEmailOutputReference, jsii.get(self, "email"))

    @builtins.property
    @jsii.member(jsii_name="hashConfig")
    def hash_config(self) -> IdentityPlatformProjectDefaultConfigSignInHashConfigList:
        return typing.cast(IdentityPlatformProjectDefaultConfigSignInHashConfigList, jsii.get(self, "hashConfig"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(
        self,
    ) -> "IdentityPlatformProjectDefaultConfigSignInPhoneNumberOutputReference":
        return typing.cast("IdentityPlatformProjectDefaultConfigSignInPhoneNumberOutputReference", jsii.get(self, "phoneNumber"))

    @builtins.property
    @jsii.member(jsii_name="allowDuplicateEmailsInput")
    def allow_duplicate_emails_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "allowDuplicateEmailsInput"))

    @builtins.property
    @jsii.member(jsii_name="anonymousInput")
    def anonymous_input(
        self,
    ) -> typing.Optional[IdentityPlatformProjectDefaultConfigSignInAnonymous]:
        return typing.cast(typing.Optional[IdentityPlatformProjectDefaultConfigSignInAnonymous], jsii.get(self, "anonymousInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(
        self,
    ) -> typing.Optional[IdentityPlatformProjectDefaultConfigSignInEmail]:
        return typing.cast(typing.Optional[IdentityPlatformProjectDefaultConfigSignInEmail], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(
        self,
    ) -> typing.Optional["IdentityPlatformProjectDefaultConfigSignInPhoneNumber"]:
        return typing.cast(typing.Optional["IdentityPlatformProjectDefaultConfigSignInPhoneNumber"], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="allowDuplicateEmails")
    def allow_duplicate_emails(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "allowDuplicateEmails"))

    @allow_duplicate_emails.setter
    def allow_duplicate_emails(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowDuplicateEmails", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IdentityPlatformProjectDefaultConfigSignIn]:
        return typing.cast(typing.Optional[IdentityPlatformProjectDefaultConfigSignIn], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityPlatformProjectDefaultConfigSignIn],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[IdentityPlatformProjectDefaultConfigSignIn],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigSignInPhoneNumber",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "test_phone_numbers": "testPhoneNumbers"},
)
class IdentityPlatformProjectDefaultConfigSignInPhoneNumber:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        test_phone_numbers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Whether phone number auth is enabled for the project or not. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#enabled IdentityPlatformProjectDefaultConfig#enabled}
        :param test_phone_numbers: A map of <test phone number, fake code> that can be used for phone auth testing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#test_phone_numbers IdentityPlatformProjectDefaultConfig#test_phone_numbers}
        '''
        if __debug__:
            def stub(
                *,
                enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                test_phone_numbers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument test_phone_numbers", value=test_phone_numbers, expected_type=type_hints["test_phone_numbers"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if test_phone_numbers is not None:
            self._values["test_phone_numbers"] = test_phone_numbers

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Whether phone number auth is enabled for the project or not.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#enabled IdentityPlatformProjectDefaultConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def test_phone_numbers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of <test phone number, fake code> that can be used for phone auth testing.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#test_phone_numbers IdentityPlatformProjectDefaultConfig#test_phone_numbers}
        '''
        result = self._values.get("test_phone_numbers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformProjectDefaultConfigSignInPhoneNumber(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformProjectDefaultConfigSignInPhoneNumberOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigSignInPhoneNumberOutputReference",
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

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetTestPhoneNumbers")
    def reset_test_phone_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestPhoneNumbers", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="testPhoneNumbersInput")
    def test_phone_numbers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "testPhoneNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="testPhoneNumbers")
    def test_phone_numbers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "testPhoneNumbers"))

    @test_phone_numbers.setter
    def test_phone_numbers(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testPhoneNumbers", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IdentityPlatformProjectDefaultConfigSignInPhoneNumber]:
        return typing.cast(typing.Optional[IdentityPlatformProjectDefaultConfigSignInPhoneNumber], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityPlatformProjectDefaultConfigSignInPhoneNumber],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[IdentityPlatformProjectDefaultConfigSignInPhoneNumber],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class IdentityPlatformProjectDefaultConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#create IdentityPlatformProjectDefaultConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#delete IdentityPlatformProjectDefaultConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#update IdentityPlatformProjectDefaultConfig#update}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#create IdentityPlatformProjectDefaultConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#delete IdentityPlatformProjectDefaultConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/identity_platform_project_default_config#update IdentityPlatformProjectDefaultConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPlatformProjectDefaultConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityPlatformProjectDefaultConfigTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.identityPlatformProjectDefaultConfig.IdentityPlatformProjectDefaultConfigTimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[IdentityPlatformProjectDefaultConfigTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[IdentityPlatformProjectDefaultConfigTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[IdentityPlatformProjectDefaultConfigTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[IdentityPlatformProjectDefaultConfigTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "IdentityPlatformProjectDefaultConfig",
    "IdentityPlatformProjectDefaultConfigConfig",
    "IdentityPlatformProjectDefaultConfigSignIn",
    "IdentityPlatformProjectDefaultConfigSignInAnonymous",
    "IdentityPlatformProjectDefaultConfigSignInAnonymousOutputReference",
    "IdentityPlatformProjectDefaultConfigSignInEmail",
    "IdentityPlatformProjectDefaultConfigSignInEmailOutputReference",
    "IdentityPlatformProjectDefaultConfigSignInHashConfig",
    "IdentityPlatformProjectDefaultConfigSignInHashConfigList",
    "IdentityPlatformProjectDefaultConfigSignInHashConfigOutputReference",
    "IdentityPlatformProjectDefaultConfigSignInOutputReference",
    "IdentityPlatformProjectDefaultConfigSignInPhoneNumber",
    "IdentityPlatformProjectDefaultConfigSignInPhoneNumberOutputReference",
    "IdentityPlatformProjectDefaultConfigTimeouts",
    "IdentityPlatformProjectDefaultConfigTimeoutsOutputReference",
]

publication.publish()
