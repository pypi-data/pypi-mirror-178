'''
# `google_datastream_connection_profile`

Refer to the Terraform Registory for docs: [`google_datastream_connection_profile`](https://www.terraform.io/docs/providers/google/r/datastream_connection_profile).
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


class DatastreamConnectionProfile(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfile",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile google_datastream_connection_profile}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        connection_profile_id: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        bigquery_profile: typing.Optional[typing.Union["DatastreamConnectionProfileBigqueryProfile", typing.Dict[str, typing.Any]]] = None,
        forward_ssh_connectivity: typing.Optional[typing.Union["DatastreamConnectionProfileForwardSshConnectivity", typing.Dict[str, typing.Any]]] = None,
        gcs_profile: typing.Optional[typing.Union["DatastreamConnectionProfileGcsProfile", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mysql_profile: typing.Optional[typing.Union["DatastreamConnectionProfileMysqlProfile", typing.Dict[str, typing.Any]]] = None,
        oracle_profile: typing.Optional[typing.Union["DatastreamConnectionProfileOracleProfile", typing.Dict[str, typing.Any]]] = None,
        postgresql_profile: typing.Optional[typing.Union["DatastreamConnectionProfilePostgresqlProfile", typing.Dict[str, typing.Any]]] = None,
        private_connectivity: typing.Optional[typing.Union["DatastreamConnectionProfilePrivateConnectivity", typing.Dict[str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DatastreamConnectionProfileTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile google_datastream_connection_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_profile_id: The connection profile identifier. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#connection_profile_id DatastreamConnectionProfile#connection_profile_id}
        :param display_name: Display name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#display_name DatastreamConnectionProfile#display_name}
        :param location: The name of the location this repository is located in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#location DatastreamConnectionProfile#location}
        :param bigquery_profile: bigquery_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#bigquery_profile DatastreamConnectionProfile#bigquery_profile}
        :param forward_ssh_connectivity: forward_ssh_connectivity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#forward_ssh_connectivity DatastreamConnectionProfile#forward_ssh_connectivity}
        :param gcs_profile: gcs_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#gcs_profile DatastreamConnectionProfile#gcs_profile}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#id DatastreamConnectionProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#labels DatastreamConnectionProfile#labels}
        :param mysql_profile: mysql_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#mysql_profile DatastreamConnectionProfile#mysql_profile}
        :param oracle_profile: oracle_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#oracle_profile DatastreamConnectionProfile#oracle_profile}
        :param postgresql_profile: postgresql_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#postgresql_profile DatastreamConnectionProfile#postgresql_profile}
        :param private_connectivity: private_connectivity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#private_connectivity DatastreamConnectionProfile#private_connectivity}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#project DatastreamConnectionProfile#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#timeouts DatastreamConnectionProfile#timeouts}
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
                connection_profile_id: builtins.str,
                display_name: builtins.str,
                location: builtins.str,
                bigquery_profile: typing.Optional[typing.Union[DatastreamConnectionProfileBigqueryProfile, typing.Dict[str, typing.Any]]] = None,
                forward_ssh_connectivity: typing.Optional[typing.Union[DatastreamConnectionProfileForwardSshConnectivity, typing.Dict[str, typing.Any]]] = None,
                gcs_profile: typing.Optional[typing.Union[DatastreamConnectionProfileGcsProfile, typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                mysql_profile: typing.Optional[typing.Union[DatastreamConnectionProfileMysqlProfile, typing.Dict[str, typing.Any]]] = None,
                oracle_profile: typing.Optional[typing.Union[DatastreamConnectionProfileOracleProfile, typing.Dict[str, typing.Any]]] = None,
                postgresql_profile: typing.Optional[typing.Union[DatastreamConnectionProfilePostgresqlProfile, typing.Dict[str, typing.Any]]] = None,
                private_connectivity: typing.Optional[typing.Union[DatastreamConnectionProfilePrivateConnectivity, typing.Dict[str, typing.Any]]] = None,
                project: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union[DatastreamConnectionProfileTimeouts, typing.Dict[str, typing.Any]]] = None,
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
        config = DatastreamConnectionProfileConfig(
            connection_profile_id=connection_profile_id,
            display_name=display_name,
            location=location,
            bigquery_profile=bigquery_profile,
            forward_ssh_connectivity=forward_ssh_connectivity,
            gcs_profile=gcs_profile,
            id=id,
            labels=labels,
            mysql_profile=mysql_profile,
            oracle_profile=oracle_profile,
            postgresql_profile=postgresql_profile,
            private_connectivity=private_connectivity,
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

    @jsii.member(jsii_name="putBigqueryProfile")
    def put_bigquery_profile(self) -> None:
        value = DatastreamConnectionProfileBigqueryProfile()

        return typing.cast(None, jsii.invoke(self, "putBigqueryProfile", [value]))

    @jsii.member(jsii_name="putForwardSshConnectivity")
    def put_forward_ssh_connectivity(
        self,
        *,
        hostname: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        private_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: Hostname for the SSH tunnel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the SSH tunnel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param password: SSH password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the SSH tunnel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param private_key: SSH private key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#private_key DatastreamConnectionProfile#private_key}
        '''
        value = DatastreamConnectionProfileForwardSshConnectivity(
            hostname=hostname,
            username=username,
            password=password,
            port=port,
            private_key=private_key,
        )

        return typing.cast(None, jsii.invoke(self, "putForwardSshConnectivity", [value]))

    @jsii.member(jsii_name="putGcsProfile")
    def put_gcs_profile(
        self,
        *,
        bucket: builtins.str,
        root_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The Cloud Storage bucket name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#bucket DatastreamConnectionProfile#bucket}
        :param root_path: The root path inside the Cloud Storage bucket. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#root_path DatastreamConnectionProfile#root_path}
        '''
        value = DatastreamConnectionProfileGcsProfile(
            bucket=bucket, root_path=root_path
        )

        return typing.cast(None, jsii.invoke(self, "putGcsProfile", [value]))

    @jsii.member(jsii_name="putMysqlProfile")
    def put_mysql_profile(
        self,
        *,
        hostname: builtins.str,
        password: builtins.str,
        username: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        ssl_config: typing.Optional[typing.Union["DatastreamConnectionProfileMysqlProfileSslConfig", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: Hostname for the MySQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param password: Password for the MySQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param username: Username for the MySQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param port: Port for the MySQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#ssl_config DatastreamConnectionProfile#ssl_config}
        '''
        value = DatastreamConnectionProfileMysqlProfile(
            hostname=hostname,
            password=password,
            username=username,
            port=port,
            ssl_config=ssl_config,
        )

        return typing.cast(None, jsii.invoke(self, "putMysqlProfile", [value]))

    @jsii.member(jsii_name="putOracleProfile")
    def put_oracle_profile(
        self,
        *,
        database_service: builtins.str,
        hostname: builtins.str,
        password: builtins.str,
        username: builtins.str,
        connection_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param database_service: Database for the Oracle connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#database_service DatastreamConnectionProfile#database_service}
        :param hostname: Hostname for the Oracle connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param password: Password for the Oracle connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param username: Username for the Oracle connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param connection_attributes: Connection string attributes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#connection_attributes DatastreamConnectionProfile#connection_attributes}
        :param port: Port for the Oracle connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        value = DatastreamConnectionProfileOracleProfile(
            database_service=database_service,
            hostname=hostname,
            password=password,
            username=username,
            connection_attributes=connection_attributes,
            port=port,
        )

        return typing.cast(None, jsii.invoke(self, "putOracleProfile", [value]))

    @jsii.member(jsii_name="putPostgresqlProfile")
    def put_postgresql_profile(
        self,
        *,
        database: builtins.str,
        hostname: builtins.str,
        password: builtins.str,
        username: builtins.str,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param database: Database for the PostgreSQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#database DatastreamConnectionProfile#database}
        :param hostname: Hostname for the PostgreSQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param password: Password for the PostgreSQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param username: Username for the PostgreSQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param port: Port for the PostgreSQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        value = DatastreamConnectionProfilePostgresqlProfile(
            database=database,
            hostname=hostname,
            password=password,
            username=username,
            port=port,
        )

        return typing.cast(None, jsii.invoke(self, "putPostgresqlProfile", [value]))

    @jsii.member(jsii_name="putPrivateConnectivity")
    def put_private_connectivity(self, *, private_connection: builtins.str) -> None:
        '''
        :param private_connection: A reference to a private connection resource. Format: 'projects/{project}/locations/{location}/privateConnections/{name}'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#private_connection DatastreamConnectionProfile#private_connection}
        '''
        value = DatastreamConnectionProfilePrivateConnectivity(
            private_connection=private_connection
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateConnectivity", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#create DatastreamConnectionProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#delete DatastreamConnectionProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#update DatastreamConnectionProfile#update}.
        '''
        value = DatastreamConnectionProfileTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBigqueryProfile")
    def reset_bigquery_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryProfile", []))

    @jsii.member(jsii_name="resetForwardSshConnectivity")
    def reset_forward_ssh_connectivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardSshConnectivity", []))

    @jsii.member(jsii_name="resetGcsProfile")
    def reset_gcs_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsProfile", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMysqlProfile")
    def reset_mysql_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlProfile", []))

    @jsii.member(jsii_name="resetOracleProfile")
    def reset_oracle_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleProfile", []))

    @jsii.member(jsii_name="resetPostgresqlProfile")
    def reset_postgresql_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresqlProfile", []))

    @jsii.member(jsii_name="resetPrivateConnectivity")
    def reset_private_connectivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateConnectivity", []))

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
    @jsii.member(jsii_name="bigqueryProfile")
    def bigquery_profile(
        self,
    ) -> "DatastreamConnectionProfileBigqueryProfileOutputReference":
        return typing.cast("DatastreamConnectionProfileBigqueryProfileOutputReference", jsii.get(self, "bigqueryProfile"))

    @builtins.property
    @jsii.member(jsii_name="forwardSshConnectivity")
    def forward_ssh_connectivity(
        self,
    ) -> "DatastreamConnectionProfileForwardSshConnectivityOutputReference":
        return typing.cast("DatastreamConnectionProfileForwardSshConnectivityOutputReference", jsii.get(self, "forwardSshConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="gcsProfile")
    def gcs_profile(self) -> "DatastreamConnectionProfileGcsProfileOutputReference":
        return typing.cast("DatastreamConnectionProfileGcsProfileOutputReference", jsii.get(self, "gcsProfile"))

    @builtins.property
    @jsii.member(jsii_name="mysqlProfile")
    def mysql_profile(self) -> "DatastreamConnectionProfileMysqlProfileOutputReference":
        return typing.cast("DatastreamConnectionProfileMysqlProfileOutputReference", jsii.get(self, "mysqlProfile"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="oracleProfile")
    def oracle_profile(
        self,
    ) -> "DatastreamConnectionProfileOracleProfileOutputReference":
        return typing.cast("DatastreamConnectionProfileOracleProfileOutputReference", jsii.get(self, "oracleProfile"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlProfile")
    def postgresql_profile(
        self,
    ) -> "DatastreamConnectionProfilePostgresqlProfileOutputReference":
        return typing.cast("DatastreamConnectionProfilePostgresqlProfileOutputReference", jsii.get(self, "postgresqlProfile"))

    @builtins.property
    @jsii.member(jsii_name="privateConnectivity")
    def private_connectivity(
        self,
    ) -> "DatastreamConnectionProfilePrivateConnectivityOutputReference":
        return typing.cast("DatastreamConnectionProfilePrivateConnectivityOutputReference", jsii.get(self, "privateConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DatastreamConnectionProfileTimeoutsOutputReference":
        return typing.cast("DatastreamConnectionProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryProfileInput")
    def bigquery_profile_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileBigqueryProfile"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileBigqueryProfile"], jsii.get(self, "bigqueryProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionProfileIdInput")
    def connection_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardSshConnectivityInput")
    def forward_ssh_connectivity_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileForwardSshConnectivity"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileForwardSshConnectivity"], jsii.get(self, "forwardSshConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsProfileInput")
    def gcs_profile_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileGcsProfile"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileGcsProfile"], jsii.get(self, "gcsProfileInput"))

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
    @jsii.member(jsii_name="mysqlProfileInput")
    def mysql_profile_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileMysqlProfile"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileMysqlProfile"], jsii.get(self, "mysqlProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleProfileInput")
    def oracle_profile_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileOracleProfile"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileOracleProfile"], jsii.get(self, "oracleProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlProfileInput")
    def postgresql_profile_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfilePostgresqlProfile"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfilePostgresqlProfile"], jsii.get(self, "postgresqlProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="privateConnectivityInput")
    def private_connectivity_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfilePrivateConnectivity"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfilePrivateConnectivity"], jsii.get(self, "privateConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["DatastreamConnectionProfileTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["DatastreamConnectionProfileTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionProfileId")
    def connection_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionProfileId"))

    @connection_profile_id.setter
    def connection_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

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
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileBigqueryProfile",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatastreamConnectionProfileBigqueryProfile:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileBigqueryProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileBigqueryProfileOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileBigqueryProfileOutputReference",
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
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileBigqueryProfile]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileBigqueryProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileBigqueryProfile],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DatastreamConnectionProfileBigqueryProfile],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "connection_profile_id": "connectionProfileId",
        "display_name": "displayName",
        "location": "location",
        "bigquery_profile": "bigqueryProfile",
        "forward_ssh_connectivity": "forwardSshConnectivity",
        "gcs_profile": "gcsProfile",
        "id": "id",
        "labels": "labels",
        "mysql_profile": "mysqlProfile",
        "oracle_profile": "oracleProfile",
        "postgresql_profile": "postgresqlProfile",
        "private_connectivity": "privateConnectivity",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class DatastreamConnectionProfileConfig(cdktf.TerraformMetaArguments):
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
        connection_profile_id: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        bigquery_profile: typing.Optional[typing.Union[DatastreamConnectionProfileBigqueryProfile, typing.Dict[str, typing.Any]]] = None,
        forward_ssh_connectivity: typing.Optional[typing.Union["DatastreamConnectionProfileForwardSshConnectivity", typing.Dict[str, typing.Any]]] = None,
        gcs_profile: typing.Optional[typing.Union["DatastreamConnectionProfileGcsProfile", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mysql_profile: typing.Optional[typing.Union["DatastreamConnectionProfileMysqlProfile", typing.Dict[str, typing.Any]]] = None,
        oracle_profile: typing.Optional[typing.Union["DatastreamConnectionProfileOracleProfile", typing.Dict[str, typing.Any]]] = None,
        postgresql_profile: typing.Optional[typing.Union["DatastreamConnectionProfilePostgresqlProfile", typing.Dict[str, typing.Any]]] = None,
        private_connectivity: typing.Optional[typing.Union["DatastreamConnectionProfilePrivateConnectivity", typing.Dict[str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DatastreamConnectionProfileTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connection_profile_id: The connection profile identifier. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#connection_profile_id DatastreamConnectionProfile#connection_profile_id}
        :param display_name: Display name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#display_name DatastreamConnectionProfile#display_name}
        :param location: The name of the location this repository is located in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#location DatastreamConnectionProfile#location}
        :param bigquery_profile: bigquery_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#bigquery_profile DatastreamConnectionProfile#bigquery_profile}
        :param forward_ssh_connectivity: forward_ssh_connectivity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#forward_ssh_connectivity DatastreamConnectionProfile#forward_ssh_connectivity}
        :param gcs_profile: gcs_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#gcs_profile DatastreamConnectionProfile#gcs_profile}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#id DatastreamConnectionProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#labels DatastreamConnectionProfile#labels}
        :param mysql_profile: mysql_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#mysql_profile DatastreamConnectionProfile#mysql_profile}
        :param oracle_profile: oracle_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#oracle_profile DatastreamConnectionProfile#oracle_profile}
        :param postgresql_profile: postgresql_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#postgresql_profile DatastreamConnectionProfile#postgresql_profile}
        :param private_connectivity: private_connectivity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#private_connectivity DatastreamConnectionProfile#private_connectivity}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#project DatastreamConnectionProfile#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#timeouts DatastreamConnectionProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bigquery_profile, dict):
            bigquery_profile = DatastreamConnectionProfileBigqueryProfile(**bigquery_profile)
        if isinstance(forward_ssh_connectivity, dict):
            forward_ssh_connectivity = DatastreamConnectionProfileForwardSshConnectivity(**forward_ssh_connectivity)
        if isinstance(gcs_profile, dict):
            gcs_profile = DatastreamConnectionProfileGcsProfile(**gcs_profile)
        if isinstance(mysql_profile, dict):
            mysql_profile = DatastreamConnectionProfileMysqlProfile(**mysql_profile)
        if isinstance(oracle_profile, dict):
            oracle_profile = DatastreamConnectionProfileOracleProfile(**oracle_profile)
        if isinstance(postgresql_profile, dict):
            postgresql_profile = DatastreamConnectionProfilePostgresqlProfile(**postgresql_profile)
        if isinstance(private_connectivity, dict):
            private_connectivity = DatastreamConnectionProfilePrivateConnectivity(**private_connectivity)
        if isinstance(timeouts, dict):
            timeouts = DatastreamConnectionProfileTimeouts(**timeouts)
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
                connection_profile_id: builtins.str,
                display_name: builtins.str,
                location: builtins.str,
                bigquery_profile: typing.Optional[typing.Union[DatastreamConnectionProfileBigqueryProfile, typing.Dict[str, typing.Any]]] = None,
                forward_ssh_connectivity: typing.Optional[typing.Union[DatastreamConnectionProfileForwardSshConnectivity, typing.Dict[str, typing.Any]]] = None,
                gcs_profile: typing.Optional[typing.Union[DatastreamConnectionProfileGcsProfile, typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                mysql_profile: typing.Optional[typing.Union[DatastreamConnectionProfileMysqlProfile, typing.Dict[str, typing.Any]]] = None,
                oracle_profile: typing.Optional[typing.Union[DatastreamConnectionProfileOracleProfile, typing.Dict[str, typing.Any]]] = None,
                postgresql_profile: typing.Optional[typing.Union[DatastreamConnectionProfilePostgresqlProfile, typing.Dict[str, typing.Any]]] = None,
                private_connectivity: typing.Optional[typing.Union[DatastreamConnectionProfilePrivateConnectivity, typing.Dict[str, typing.Any]]] = None,
                project: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union[DatastreamConnectionProfileTimeouts, typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument connection_profile_id", value=connection_profile_id, expected_type=type_hints["connection_profile_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument bigquery_profile", value=bigquery_profile, expected_type=type_hints["bigquery_profile"])
            check_type(argname="argument forward_ssh_connectivity", value=forward_ssh_connectivity, expected_type=type_hints["forward_ssh_connectivity"])
            check_type(argname="argument gcs_profile", value=gcs_profile, expected_type=type_hints["gcs_profile"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mysql_profile", value=mysql_profile, expected_type=type_hints["mysql_profile"])
            check_type(argname="argument oracle_profile", value=oracle_profile, expected_type=type_hints["oracle_profile"])
            check_type(argname="argument postgresql_profile", value=postgresql_profile, expected_type=type_hints["postgresql_profile"])
            check_type(argname="argument private_connectivity", value=private_connectivity, expected_type=type_hints["private_connectivity"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "connection_profile_id": connection_profile_id,
            "display_name": display_name,
            "location": location,
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
        if bigquery_profile is not None:
            self._values["bigquery_profile"] = bigquery_profile
        if forward_ssh_connectivity is not None:
            self._values["forward_ssh_connectivity"] = forward_ssh_connectivity
        if gcs_profile is not None:
            self._values["gcs_profile"] = gcs_profile
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if mysql_profile is not None:
            self._values["mysql_profile"] = mysql_profile
        if oracle_profile is not None:
            self._values["oracle_profile"] = oracle_profile
        if postgresql_profile is not None:
            self._values["postgresql_profile"] = postgresql_profile
        if private_connectivity is not None:
            self._values["private_connectivity"] = private_connectivity
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
    def connection_profile_id(self) -> builtins.str:
        '''The connection profile identifier.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#connection_profile_id DatastreamConnectionProfile#connection_profile_id}
        '''
        result = self._values.get("connection_profile_id")
        assert result is not None, "Required property 'connection_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Display name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#display_name DatastreamConnectionProfile#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this repository is located in.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#location DatastreamConnectionProfile#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bigquery_profile(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileBigqueryProfile]:
        '''bigquery_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#bigquery_profile DatastreamConnectionProfile#bigquery_profile}
        '''
        result = self._values.get("bigquery_profile")
        return typing.cast(typing.Optional[DatastreamConnectionProfileBigqueryProfile], result)

    @builtins.property
    def forward_ssh_connectivity(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileForwardSshConnectivity"]:
        '''forward_ssh_connectivity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#forward_ssh_connectivity DatastreamConnectionProfile#forward_ssh_connectivity}
        '''
        result = self._values.get("forward_ssh_connectivity")
        return typing.cast(typing.Optional["DatastreamConnectionProfileForwardSshConnectivity"], result)

    @builtins.property
    def gcs_profile(self) -> typing.Optional["DatastreamConnectionProfileGcsProfile"]:
        '''gcs_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#gcs_profile DatastreamConnectionProfile#gcs_profile}
        '''
        result = self._values.get("gcs_profile")
        return typing.cast(typing.Optional["DatastreamConnectionProfileGcsProfile"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#id DatastreamConnectionProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#labels DatastreamConnectionProfile#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mysql_profile(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileMysqlProfile"]:
        '''mysql_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#mysql_profile DatastreamConnectionProfile#mysql_profile}
        '''
        result = self._values.get("mysql_profile")
        return typing.cast(typing.Optional["DatastreamConnectionProfileMysqlProfile"], result)

    @builtins.property
    def oracle_profile(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileOracleProfile"]:
        '''oracle_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#oracle_profile DatastreamConnectionProfile#oracle_profile}
        '''
        result = self._values.get("oracle_profile")
        return typing.cast(typing.Optional["DatastreamConnectionProfileOracleProfile"], result)

    @builtins.property
    def postgresql_profile(
        self,
    ) -> typing.Optional["DatastreamConnectionProfilePostgresqlProfile"]:
        '''postgresql_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#postgresql_profile DatastreamConnectionProfile#postgresql_profile}
        '''
        result = self._values.get("postgresql_profile")
        return typing.cast(typing.Optional["DatastreamConnectionProfilePostgresqlProfile"], result)

    @builtins.property
    def private_connectivity(
        self,
    ) -> typing.Optional["DatastreamConnectionProfilePrivateConnectivity"]:
        '''private_connectivity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#private_connectivity DatastreamConnectionProfile#private_connectivity}
        '''
        result = self._values.get("private_connectivity")
        return typing.cast(typing.Optional["DatastreamConnectionProfilePrivateConnectivity"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#project DatastreamConnectionProfile#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DatastreamConnectionProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#timeouts DatastreamConnectionProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DatastreamConnectionProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileForwardSshConnectivity",
    jsii_struct_bases=[],
    name_mapping={
        "hostname": "hostname",
        "username": "username",
        "password": "password",
        "port": "port",
        "private_key": "privateKey",
    },
)
class DatastreamConnectionProfileForwardSshConnectivity:
    def __init__(
        self,
        *,
        hostname: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        private_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: Hostname for the SSH tunnel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the SSH tunnel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param password: SSH password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the SSH tunnel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param private_key: SSH private key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#private_key DatastreamConnectionProfile#private_key}
        '''
        if __debug__:
            def stub(
                *,
                hostname: builtins.str,
                username: builtins.str,
                password: typing.Optional[builtins.str] = None,
                port: typing.Optional[jsii.Number] = None,
                private_key: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "hostname": hostname,
            "username": username,
        }
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if private_key is not None:
            self._values["private_key"] = private_key

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the SSH tunnel.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the SSH tunnel.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''SSH password.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the SSH tunnel.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''SSH private key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#private_key DatastreamConnectionProfile#private_key}
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileForwardSshConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileForwardSshConnectivityOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileForwardSshConnectivityOutputReference",
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

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPrivateKey")
    def reset_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKey", []))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileForwardSshConnectivity]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileForwardSshConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileForwardSshConnectivity],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DatastreamConnectionProfileForwardSshConnectivity],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileGcsProfile",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "root_path": "rootPath"},
)
class DatastreamConnectionProfileGcsProfile:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        root_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The Cloud Storage bucket name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#bucket DatastreamConnectionProfile#bucket}
        :param root_path: The root path inside the Cloud Storage bucket. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#root_path DatastreamConnectionProfile#root_path}
        '''
        if __debug__:
            def stub(
                *,
                bucket: builtins.str,
                root_path: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument root_path", value=root_path, expected_type=type_hints["root_path"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if root_path is not None:
            self._values["root_path"] = root_path

    @builtins.property
    def bucket(self) -> builtins.str:
        '''The Cloud Storage bucket name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#bucket DatastreamConnectionProfile#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_path(self) -> typing.Optional[builtins.str]:
        '''The root path inside the Cloud Storage bucket.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#root_path DatastreamConnectionProfile#root_path}
        '''
        result = self._values.get("root_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileGcsProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileGcsProfileOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileGcsProfileOutputReference",
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

    @jsii.member(jsii_name="resetRootPath")
    def reset_root_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootPath", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="rootPathInput")
    def root_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootPathInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value)

    @builtins.property
    @jsii.member(jsii_name="rootPath")
    def root_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootPath"))

    @root_path.setter
    def root_path(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootPath", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DatastreamConnectionProfileGcsProfile]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileGcsProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileGcsProfile],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DatastreamConnectionProfileGcsProfile],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileMysqlProfile",
    jsii_struct_bases=[],
    name_mapping={
        "hostname": "hostname",
        "password": "password",
        "username": "username",
        "port": "port",
        "ssl_config": "sslConfig",
    },
)
class DatastreamConnectionProfileMysqlProfile:
    def __init__(
        self,
        *,
        hostname: builtins.str,
        password: builtins.str,
        username: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        ssl_config: typing.Optional[typing.Union["DatastreamConnectionProfileMysqlProfileSslConfig", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: Hostname for the MySQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param password: Password for the MySQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param username: Username for the MySQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param port: Port for the MySQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#ssl_config DatastreamConnectionProfile#ssl_config}
        '''
        if isinstance(ssl_config, dict):
            ssl_config = DatastreamConnectionProfileMysqlProfileSslConfig(**ssl_config)
        if __debug__:
            def stub(
                *,
                hostname: builtins.str,
                password: builtins.str,
                username: builtins.str,
                port: typing.Optional[jsii.Number] = None,
                ssl_config: typing.Optional[typing.Union[DatastreamConnectionProfileMysqlProfileSslConfig, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument ssl_config", value=ssl_config, expected_type=type_hints["ssl_config"])
        self._values: typing.Dict[str, typing.Any] = {
            "hostname": hostname,
            "password": password,
            "username": username,
        }
        if port is not None:
            self._values["port"] = port
        if ssl_config is not None:
            self._values["ssl_config"] = ssl_config

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the MySQL connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Password for the MySQL connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the MySQL connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the MySQL connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssl_config(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileMysqlProfileSslConfig"]:
        '''ssl_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#ssl_config DatastreamConnectionProfile#ssl_config}
        '''
        result = self._values.get("ssl_config")
        return typing.cast(typing.Optional["DatastreamConnectionProfileMysqlProfileSslConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileMysqlProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileMysqlProfileOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileMysqlProfileOutputReference",
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

    @jsii.member(jsii_name="putSslConfig")
    def put_ssl_config(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: PEM-encoded certificate of the CA that signed the source database server's certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#ca_certificate DatastreamConnectionProfile#ca_certificate}
        :param client_certificate: PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' and the 'caCertificate' fields are mandatory. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#client_certificate DatastreamConnectionProfile#client_certificate}
        :param client_key: PEM-encoded private key associated with the Client Certificate. If this field is used then the 'client_certificate' and the 'ca_certificate' fields are mandatory. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#client_key DatastreamConnectionProfile#client_key}
        '''
        value = DatastreamConnectionProfileMysqlProfileSslConfig(
            ca_certificate=ca_certificate,
            client_certificate=client_certificate,
            client_key=client_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSslConfig", [value]))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetSslConfig")
    def reset_ssl_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslConfig", []))

    @builtins.property
    @jsii.member(jsii_name="sslConfig")
    def ssl_config(
        self,
    ) -> "DatastreamConnectionProfileMysqlProfileSslConfigOutputReference":
        return typing.cast("DatastreamConnectionProfileMysqlProfileSslConfigOutputReference", jsii.get(self, "sslConfig"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="sslConfigInput")
    def ssl_config_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileMysqlProfileSslConfig"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileMysqlProfileSslConfig"], jsii.get(self, "sslConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileMysqlProfile]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileMysqlProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileMysqlProfile],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DatastreamConnectionProfileMysqlProfile],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileMysqlProfileSslConfig",
    jsii_struct_bases=[],
    name_mapping={
        "ca_certificate": "caCertificate",
        "client_certificate": "clientCertificate",
        "client_key": "clientKey",
    },
)
class DatastreamConnectionProfileMysqlProfileSslConfig:
    def __init__(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: PEM-encoded certificate of the CA that signed the source database server's certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#ca_certificate DatastreamConnectionProfile#ca_certificate}
        :param client_certificate: PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' and the 'caCertificate' fields are mandatory. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#client_certificate DatastreamConnectionProfile#client_certificate}
        :param client_key: PEM-encoded private key associated with the Client Certificate. If this field is used then the 'client_certificate' and the 'ca_certificate' fields are mandatory. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#client_key DatastreamConnectionProfile#client_key}
        '''
        if __debug__:
            def stub(
                *,
                ca_certificate: typing.Optional[builtins.str] = None,
                client_certificate: typing.Optional[builtins.str] = None,
                client_key: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument ca_certificate", value=ca_certificate, expected_type=type_hints["ca_certificate"])
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument client_key", value=client_key, expected_type=type_hints["client_key"])
        self._values: typing.Dict[str, typing.Any] = {}
        if ca_certificate is not None:
            self._values["ca_certificate"] = ca_certificate
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if client_key is not None:
            self._values["client_key"] = client_key

    @builtins.property
    def ca_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded certificate of the CA that signed the source database server's certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#ca_certificate DatastreamConnectionProfile#ca_certificate}
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded certificate that will be used by the replica to authenticate against the source database server.

        If this field
        is used then the 'clientKey' and the 'caCertificate' fields are
        mandatory.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#client_certificate DatastreamConnectionProfile#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded private key associated with the Client Certificate.

        If this field is used then the 'client_certificate' and the
        'ca_certificate' fields are mandatory.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#client_key DatastreamConnectionProfile#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileMysqlProfileSslConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileMysqlProfileSslConfigOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileMysqlProfileSslConfigOutputReference",
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

    @jsii.member(jsii_name="resetCaCertificate")
    def reset_ca_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCertificate", []))

    @jsii.member(jsii_name="resetClientCertificate")
    def reset_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificate", []))

    @jsii.member(jsii_name="resetClientKey")
    def reset_client_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientKey", []))

    @builtins.property
    @jsii.member(jsii_name="caCertificateSet")
    def ca_certificate_set(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "caCertificateSet"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateSet")
    def client_certificate_set(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "clientCertificateSet"))

    @builtins.property
    @jsii.member(jsii_name="clientKeySet")
    def client_key_set(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "clientKeySet"))

    @builtins.property
    @jsii.member(jsii_name="caCertificateInput")
    def ca_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateInput")
    def client_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="clientKeyInput")
    def client_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertificate")
    def ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertificate"))

    @ca_certificate.setter
    def ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificate", value)

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value)

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileMysqlProfileSslConfig]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileMysqlProfileSslConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileMysqlProfileSslConfig],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DatastreamConnectionProfileMysqlProfileSslConfig],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileOracleProfile",
    jsii_struct_bases=[],
    name_mapping={
        "database_service": "databaseService",
        "hostname": "hostname",
        "password": "password",
        "username": "username",
        "connection_attributes": "connectionAttributes",
        "port": "port",
    },
)
class DatastreamConnectionProfileOracleProfile:
    def __init__(
        self,
        *,
        database_service: builtins.str,
        hostname: builtins.str,
        password: builtins.str,
        username: builtins.str,
        connection_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param database_service: Database for the Oracle connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#database_service DatastreamConnectionProfile#database_service}
        :param hostname: Hostname for the Oracle connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param password: Password for the Oracle connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param username: Username for the Oracle connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param connection_attributes: Connection string attributes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#connection_attributes DatastreamConnectionProfile#connection_attributes}
        :param port: Port for the Oracle connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        if __debug__:
            def stub(
                *,
                database_service: builtins.str,
                hostname: builtins.str,
                password: builtins.str,
                username: builtins.str,
                connection_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                port: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument database_service", value=database_service, expected_type=type_hints["database_service"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument connection_attributes", value=connection_attributes, expected_type=type_hints["connection_attributes"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[str, typing.Any] = {
            "database_service": database_service,
            "hostname": hostname,
            "password": password,
            "username": username,
        }
        if connection_attributes is not None:
            self._values["connection_attributes"] = connection_attributes
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def database_service(self) -> builtins.str:
        '''Database for the Oracle connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#database_service DatastreamConnectionProfile#database_service}
        '''
        result = self._values.get("database_service")
        assert result is not None, "Required property 'database_service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the Oracle connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Password for the Oracle connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the Oracle connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Connection string attributes.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#connection_attributes DatastreamConnectionProfile#connection_attributes}
        '''
        result = self._values.get("connection_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the Oracle connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileOracleProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileOracleProfileOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileOracleProfileOutputReference",
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

    @jsii.member(jsii_name="resetConnectionAttributes")
    def reset_connection_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionAttributes", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="connectionAttributesInput")
    def connection_attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "connectionAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseServiceInput")
    def database_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionAttributes")
    def connection_attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "connectionAttributes"))

    @connection_attributes.setter
    def connection_attributes(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="databaseService")
    def database_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseService"))

    @database_service.setter
    def database_service(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseService", value)

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileOracleProfile]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileOracleProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileOracleProfile],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DatastreamConnectionProfileOracleProfile],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfilePostgresqlProfile",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "hostname": "hostname",
        "password": "password",
        "username": "username",
        "port": "port",
    },
)
class DatastreamConnectionProfilePostgresqlProfile:
    def __init__(
        self,
        *,
        database: builtins.str,
        hostname: builtins.str,
        password: builtins.str,
        username: builtins.str,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param database: Database for the PostgreSQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#database DatastreamConnectionProfile#database}
        :param hostname: Hostname for the PostgreSQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param password: Password for the PostgreSQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param username: Username for the PostgreSQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param port: Port for the PostgreSQL connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        if __debug__:
            def stub(
                *,
                database: builtins.str,
                hostname: builtins.str,
                password: builtins.str,
                username: builtins.str,
                port: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[str, typing.Any] = {
            "database": database,
            "hostname": hostname,
            "password": password,
            "username": username,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def database(self) -> builtins.str:
        '''Database for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#database DatastreamConnectionProfile#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Password for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#password DatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#username DatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfilePostgresqlProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfilePostgresqlProfileOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfilePostgresqlProfileOutputReference",
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

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value)

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfilePostgresqlProfile]:
        return typing.cast(typing.Optional[DatastreamConnectionProfilePostgresqlProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfilePostgresqlProfile],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DatastreamConnectionProfilePostgresqlProfile],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfilePrivateConnectivity",
    jsii_struct_bases=[],
    name_mapping={"private_connection": "privateConnection"},
)
class DatastreamConnectionProfilePrivateConnectivity:
    def __init__(self, *, private_connection: builtins.str) -> None:
        '''
        :param private_connection: A reference to a private connection resource. Format: 'projects/{project}/locations/{location}/privateConnections/{name}'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#private_connection DatastreamConnectionProfile#private_connection}
        '''
        if __debug__:
            def stub(*, private_connection: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument private_connection", value=private_connection, expected_type=type_hints["private_connection"])
        self._values: typing.Dict[str, typing.Any] = {
            "private_connection": private_connection,
        }

    @builtins.property
    def private_connection(self) -> builtins.str:
        '''A reference to a private connection resource. Format: 'projects/{project}/locations/{location}/privateConnections/{name}'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#private_connection DatastreamConnectionProfile#private_connection}
        '''
        result = self._values.get("private_connection")
        assert result is not None, "Required property 'private_connection' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfilePrivateConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfilePrivateConnectivityOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfilePrivateConnectivityOutputReference",
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
    @jsii.member(jsii_name="privateConnectionInput")
    def private_connection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="privateConnection")
    def private_connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateConnection"))

    @private_connection.setter
    def private_connection(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfilePrivateConnectivity]:
        return typing.cast(typing.Optional[DatastreamConnectionProfilePrivateConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfilePrivateConnectivity],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[DatastreamConnectionProfilePrivateConnectivity],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DatastreamConnectionProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#create DatastreamConnectionProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#delete DatastreamConnectionProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#update DatastreamConnectionProfile#update}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#create DatastreamConnectionProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#delete DatastreamConnectionProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/datastream_connection_profile#update DatastreamConnectionProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileTimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[DatastreamConnectionProfileTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DatastreamConnectionProfileTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DatastreamConnectionProfileTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[DatastreamConnectionProfileTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DatastreamConnectionProfile",
    "DatastreamConnectionProfileBigqueryProfile",
    "DatastreamConnectionProfileBigqueryProfileOutputReference",
    "DatastreamConnectionProfileConfig",
    "DatastreamConnectionProfileForwardSshConnectivity",
    "DatastreamConnectionProfileForwardSshConnectivityOutputReference",
    "DatastreamConnectionProfileGcsProfile",
    "DatastreamConnectionProfileGcsProfileOutputReference",
    "DatastreamConnectionProfileMysqlProfile",
    "DatastreamConnectionProfileMysqlProfileOutputReference",
    "DatastreamConnectionProfileMysqlProfileSslConfig",
    "DatastreamConnectionProfileMysqlProfileSslConfigOutputReference",
    "DatastreamConnectionProfileOracleProfile",
    "DatastreamConnectionProfileOracleProfileOutputReference",
    "DatastreamConnectionProfilePostgresqlProfile",
    "DatastreamConnectionProfilePostgresqlProfileOutputReference",
    "DatastreamConnectionProfilePrivateConnectivity",
    "DatastreamConnectionProfilePrivateConnectivityOutputReference",
    "DatastreamConnectionProfileTimeouts",
    "DatastreamConnectionProfileTimeoutsOutputReference",
]

publication.publish()
