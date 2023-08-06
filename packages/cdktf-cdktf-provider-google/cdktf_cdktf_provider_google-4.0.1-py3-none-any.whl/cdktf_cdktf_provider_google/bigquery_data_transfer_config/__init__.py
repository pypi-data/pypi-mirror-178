'''
# `google_bigquery_data_transfer_config`

Refer to the Terraform Registory for docs: [`google_bigquery_data_transfer_config`](https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config).
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


class BigqueryDataTransferConfig(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfig",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config google_bigquery_data_transfer_config}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        data_source_id: builtins.str,
        display_name: builtins.str,
        params: typing.Mapping[builtins.str, builtins.str],
        data_refresh_window_days: typing.Optional[jsii.Number] = None,
        destination_dataset_id: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        email_preferences: typing.Optional[typing.Union["BigqueryDataTransferConfigEmailPreferences", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        notification_pubsub_topic: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        schedule_options: typing.Optional[typing.Union["BigqueryDataTransferConfigScheduleOptions", typing.Dict[str, typing.Any]]] = None,
        sensitive_params: typing.Optional[typing.Union["BigqueryDataTransferConfigSensitiveParams", typing.Dict[str, typing.Any]]] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryDataTransferConfigTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config google_bigquery_data_transfer_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_source_id: The data source id. Cannot be changed once the transfer config is created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#data_source_id BigqueryDataTransferConfig#data_source_id}
        :param display_name: The user specified display name for the transfer config. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#display_name BigqueryDataTransferConfig#display_name}
        :param params: Parameters specific to each data source. For more information see the bq tab in the 'Setting up a data transfer' section for each data source. For example the parameters for Cloud Storage transfers are listed here: https://cloud.google.com/bigquery-transfer/docs/cloud-storage-transfer#bq *NOTE** : If you are attempting to update a parameter that cannot be updated (due to api limitations) `please force recreation of the resource <https://www.terraform.io/cli/state/taint#forcing-re-creation-of-resources>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#params BigqueryDataTransferConfig#params}
        :param data_refresh_window_days: The number of days to look back to automatically refresh the data. For example, if dataRefreshWindowDays = 10, then every day BigQuery reingests data for [today-10, today-1], rather than ingesting data for just [today-1]. Only valid if the data source supports the feature. Set the value to 0 to use the default value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#data_refresh_window_days BigqueryDataTransferConfig#data_refresh_window_days}
        :param destination_dataset_id: The BigQuery target dataset id. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#destination_dataset_id BigqueryDataTransferConfig#destination_dataset_id}
        :param disabled: When set to true, no runs are scheduled for a given transfer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#disabled BigqueryDataTransferConfig#disabled}
        :param email_preferences: email_preferences block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#email_preferences BigqueryDataTransferConfig#email_preferences}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#id BigqueryDataTransferConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#location BigqueryDataTransferConfig#location}
        :param notification_pubsub_topic: Pub/Sub topic where notifications will be sent after transfer runs associated with this transfer config finish. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#notification_pubsub_topic BigqueryDataTransferConfig#notification_pubsub_topic}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#project BigqueryDataTransferConfig#project}.
        :param schedule: Data transfer schedule. If the data source does not support a custom schedule, this should be empty. If it is empty, the default value for the data source will be used. The specified times are in UTC. Examples of valid format: 1st,3rd monday of month 15:30, every wed,fri of jan, jun 13:15, and first sunday of quarter 00:00. See more explanation about the format here: https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml#the_schedule_format NOTE: the granularity should be at least 8 hours, or less frequent. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#schedule BigqueryDataTransferConfig#schedule}
        :param schedule_options: schedule_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#schedule_options BigqueryDataTransferConfig#schedule_options}
        :param sensitive_params: sensitive_params block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#sensitive_params BigqueryDataTransferConfig#sensitive_params}
        :param service_account_name: Service account email. If this field is set, transfer config will be created with this service account credentials. It requires that requesting user calling this API has permissions to act as this service account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#service_account_name BigqueryDataTransferConfig#service_account_name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#timeouts BigqueryDataTransferConfig#timeouts}
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
                data_source_id: builtins.str,
                display_name: builtins.str,
                params: typing.Mapping[builtins.str, builtins.str],
                data_refresh_window_days: typing.Optional[jsii.Number] = None,
                destination_dataset_id: typing.Optional[builtins.str] = None,
                disabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                email_preferences: typing.Optional[typing.Union[BigqueryDataTransferConfigEmailPreferences, typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                location: typing.Optional[builtins.str] = None,
                notification_pubsub_topic: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                schedule: typing.Optional[builtins.str] = None,
                schedule_options: typing.Optional[typing.Union[BigqueryDataTransferConfigScheduleOptions, typing.Dict[str, typing.Any]]] = None,
                sensitive_params: typing.Optional[typing.Union[BigqueryDataTransferConfigSensitiveParams, typing.Dict[str, typing.Any]]] = None,
                service_account_name: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union[BigqueryDataTransferConfigTimeouts, typing.Dict[str, typing.Any]]] = None,
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
        config = BigqueryDataTransferConfigConfig(
            data_source_id=data_source_id,
            display_name=display_name,
            params=params,
            data_refresh_window_days=data_refresh_window_days,
            destination_dataset_id=destination_dataset_id,
            disabled=disabled,
            email_preferences=email_preferences,
            id=id,
            location=location,
            notification_pubsub_topic=notification_pubsub_topic,
            project=project,
            schedule=schedule,
            schedule_options=schedule_options,
            sensitive_params=sensitive_params,
            service_account_name=service_account_name,
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

    @jsii.member(jsii_name="putEmailPreferences")
    def put_email_preferences(
        self,
        *,
        enable_failure_email: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        '''
        :param enable_failure_email: If true, email notifications will be sent on transfer run failures. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#enable_failure_email BigqueryDataTransferConfig#enable_failure_email}
        '''
        value = BigqueryDataTransferConfigEmailPreferences(
            enable_failure_email=enable_failure_email
        )

        return typing.cast(None, jsii.invoke(self, "putEmailPreferences", [value]))

    @jsii.member(jsii_name="putScheduleOptions")
    def put_schedule_options(
        self,
        *,
        disable_auto_scheduling: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable_auto_scheduling: If true, automatic scheduling of data transfer runs for this configuration will be disabled. The runs can be started on ad-hoc basis using transferConfigs.startManualRuns API. When automatic scheduling is disabled, the TransferConfig.schedule field will be ignored. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#disable_auto_scheduling BigqueryDataTransferConfig#disable_auto_scheduling}
        :param end_time: Defines time to stop scheduling transfer runs. A transfer run cannot be scheduled at or after the end time. The end time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#end_time BigqueryDataTransferConfig#end_time}
        :param start_time: Specifies time to start scheduling transfer runs. The first run will be scheduled at or after the start time according to a recurrence pattern defined in the schedule string. The start time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#start_time BigqueryDataTransferConfig#start_time}
        '''
        value = BigqueryDataTransferConfigScheduleOptions(
            disable_auto_scheduling=disable_auto_scheduling,
            end_time=end_time,
            start_time=start_time,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduleOptions", [value]))

    @jsii.member(jsii_name="putSensitiveParams")
    def put_sensitive_params(self, *, secret_access_key: builtins.str) -> None:
        '''
        :param secret_access_key: The Secret Access Key of the AWS account transferring data from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#secret_access_key BigqueryDataTransferConfig#secret_access_key}
        '''
        value = BigqueryDataTransferConfigSensitiveParams(
            secret_access_key=secret_access_key
        )

        return typing.cast(None, jsii.invoke(self, "putSensitiveParams", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#create BigqueryDataTransferConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#delete BigqueryDataTransferConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#update BigqueryDataTransferConfig#update}.
        '''
        value = BigqueryDataTransferConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDataRefreshWindowDays")
    def reset_data_refresh_window_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataRefreshWindowDays", []))

    @jsii.member(jsii_name="resetDestinationDatasetId")
    def reset_destination_dataset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationDatasetId", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetEmailPreferences")
    def reset_email_preferences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailPreferences", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetNotificationPubsubTopic")
    def reset_notification_pubsub_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationPubsubTopic", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetScheduleOptions")
    def reset_schedule_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleOptions", []))

    @jsii.member(jsii_name="resetSensitiveParams")
    def reset_sensitive_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitiveParams", []))

    @jsii.member(jsii_name="resetServiceAccountName")
    def reset_service_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountName", []))

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
    @jsii.member(jsii_name="emailPreferences")
    def email_preferences(
        self,
    ) -> "BigqueryDataTransferConfigEmailPreferencesOutputReference":
        return typing.cast("BigqueryDataTransferConfigEmailPreferencesOutputReference", jsii.get(self, "emailPreferences"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="scheduleOptions")
    def schedule_options(
        self,
    ) -> "BigqueryDataTransferConfigScheduleOptionsOutputReference":
        return typing.cast("BigqueryDataTransferConfigScheduleOptionsOutputReference", jsii.get(self, "scheduleOptions"))

    @builtins.property
    @jsii.member(jsii_name="sensitiveParams")
    def sensitive_params(
        self,
    ) -> "BigqueryDataTransferConfigSensitiveParamsOutputReference":
        return typing.cast("BigqueryDataTransferConfigSensitiveParamsOutputReference", jsii.get(self, "sensitiveParams"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigqueryDataTransferConfigTimeoutsOutputReference":
        return typing.cast("BigqueryDataTransferConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataRefreshWindowDaysInput")
    def data_refresh_window_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataRefreshWindowDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceIdInput")
    def data_source_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationDatasetIdInput")
    def destination_dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationDatasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailPreferencesInput")
    def email_preferences_input(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigEmailPreferences"]:
        return typing.cast(typing.Optional["BigqueryDataTransferConfigEmailPreferences"], jsii.get(self, "emailPreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationPubsubTopicInput")
    def notification_pubsub_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationPubsubTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "paramsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleOptionsInput")
    def schedule_options_input(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigScheduleOptions"]:
        return typing.cast(typing.Optional["BigqueryDataTransferConfigScheduleOptions"], jsii.get(self, "scheduleOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitiveParamsInput")
    def sensitive_params_input(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigSensitiveParams"]:
        return typing.cast(typing.Optional["BigqueryDataTransferConfigSensitiveParams"], jsii.get(self, "sensitiveParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountNameInput")
    def service_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["BigqueryDataTransferConfigTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["BigqueryDataTransferConfigTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataRefreshWindowDays")
    def data_refresh_window_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataRefreshWindowDays"))

    @data_refresh_window_days.setter
    def data_refresh_window_days(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataRefreshWindowDays", value)

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @data_source_id.setter
    def data_source_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceId", value)

    @builtins.property
    @jsii.member(jsii_name="destinationDatasetId")
    def destination_dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationDatasetId"))

    @destination_dataset_id.setter
    def destination_dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationDatasetId", value)

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value)

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
    @jsii.member(jsii_name="notificationPubsubTopic")
    def notification_pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationPubsubTopic"))

    @notification_pubsub_topic.setter
    def notification_pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationPubsubTopic", value)

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "params"))

    @params.setter
    def params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "params", value)

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
    @jsii.member(jsii_name="serviceAccountName")
    def service_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountName"))

    @service_account_name.setter
    def service_account_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_source_id": "dataSourceId",
        "display_name": "displayName",
        "params": "params",
        "data_refresh_window_days": "dataRefreshWindowDays",
        "destination_dataset_id": "destinationDatasetId",
        "disabled": "disabled",
        "email_preferences": "emailPreferences",
        "id": "id",
        "location": "location",
        "notification_pubsub_topic": "notificationPubsubTopic",
        "project": "project",
        "schedule": "schedule",
        "schedule_options": "scheduleOptions",
        "sensitive_params": "sensitiveParams",
        "service_account_name": "serviceAccountName",
        "timeouts": "timeouts",
    },
)
class BigqueryDataTransferConfigConfig(cdktf.TerraformMetaArguments):
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
        data_source_id: builtins.str,
        display_name: builtins.str,
        params: typing.Mapping[builtins.str, builtins.str],
        data_refresh_window_days: typing.Optional[jsii.Number] = None,
        destination_dataset_id: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        email_preferences: typing.Optional[typing.Union["BigqueryDataTransferConfigEmailPreferences", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        notification_pubsub_topic: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        schedule_options: typing.Optional[typing.Union["BigqueryDataTransferConfigScheduleOptions", typing.Dict[str, typing.Any]]] = None,
        sensitive_params: typing.Optional[typing.Union["BigqueryDataTransferConfigSensitiveParams", typing.Dict[str, typing.Any]]] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryDataTransferConfigTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_source_id: The data source id. Cannot be changed once the transfer config is created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#data_source_id BigqueryDataTransferConfig#data_source_id}
        :param display_name: The user specified display name for the transfer config. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#display_name BigqueryDataTransferConfig#display_name}
        :param params: Parameters specific to each data source. For more information see the bq tab in the 'Setting up a data transfer' section for each data source. For example the parameters for Cloud Storage transfers are listed here: https://cloud.google.com/bigquery-transfer/docs/cloud-storage-transfer#bq *NOTE** : If you are attempting to update a parameter that cannot be updated (due to api limitations) `please force recreation of the resource <https://www.terraform.io/cli/state/taint#forcing-re-creation-of-resources>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#params BigqueryDataTransferConfig#params}
        :param data_refresh_window_days: The number of days to look back to automatically refresh the data. For example, if dataRefreshWindowDays = 10, then every day BigQuery reingests data for [today-10, today-1], rather than ingesting data for just [today-1]. Only valid if the data source supports the feature. Set the value to 0 to use the default value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#data_refresh_window_days BigqueryDataTransferConfig#data_refresh_window_days}
        :param destination_dataset_id: The BigQuery target dataset id. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#destination_dataset_id BigqueryDataTransferConfig#destination_dataset_id}
        :param disabled: When set to true, no runs are scheduled for a given transfer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#disabled BigqueryDataTransferConfig#disabled}
        :param email_preferences: email_preferences block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#email_preferences BigqueryDataTransferConfig#email_preferences}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#id BigqueryDataTransferConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#location BigqueryDataTransferConfig#location}
        :param notification_pubsub_topic: Pub/Sub topic where notifications will be sent after transfer runs associated with this transfer config finish. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#notification_pubsub_topic BigqueryDataTransferConfig#notification_pubsub_topic}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#project BigqueryDataTransferConfig#project}.
        :param schedule: Data transfer schedule. If the data source does not support a custom schedule, this should be empty. If it is empty, the default value for the data source will be used. The specified times are in UTC. Examples of valid format: 1st,3rd monday of month 15:30, every wed,fri of jan, jun 13:15, and first sunday of quarter 00:00. See more explanation about the format here: https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml#the_schedule_format NOTE: the granularity should be at least 8 hours, or less frequent. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#schedule BigqueryDataTransferConfig#schedule}
        :param schedule_options: schedule_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#schedule_options BigqueryDataTransferConfig#schedule_options}
        :param sensitive_params: sensitive_params block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#sensitive_params BigqueryDataTransferConfig#sensitive_params}
        :param service_account_name: Service account email. If this field is set, transfer config will be created with this service account credentials. It requires that requesting user calling this API has permissions to act as this service account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#service_account_name BigqueryDataTransferConfig#service_account_name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#timeouts BigqueryDataTransferConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(email_preferences, dict):
            email_preferences = BigqueryDataTransferConfigEmailPreferences(**email_preferences)
        if isinstance(schedule_options, dict):
            schedule_options = BigqueryDataTransferConfigScheduleOptions(**schedule_options)
        if isinstance(sensitive_params, dict):
            sensitive_params = BigqueryDataTransferConfigSensitiveParams(**sensitive_params)
        if isinstance(timeouts, dict):
            timeouts = BigqueryDataTransferConfigTimeouts(**timeouts)
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
                data_source_id: builtins.str,
                display_name: builtins.str,
                params: typing.Mapping[builtins.str, builtins.str],
                data_refresh_window_days: typing.Optional[jsii.Number] = None,
                destination_dataset_id: typing.Optional[builtins.str] = None,
                disabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                email_preferences: typing.Optional[typing.Union[BigqueryDataTransferConfigEmailPreferences, typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                location: typing.Optional[builtins.str] = None,
                notification_pubsub_topic: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                schedule: typing.Optional[builtins.str] = None,
                schedule_options: typing.Optional[typing.Union[BigqueryDataTransferConfigScheduleOptions, typing.Dict[str, typing.Any]]] = None,
                sensitive_params: typing.Optional[typing.Union[BigqueryDataTransferConfigSensitiveParams, typing.Dict[str, typing.Any]]] = None,
                service_account_name: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union[BigqueryDataTransferConfigTimeouts, typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument data_source_id", value=data_source_id, expected_type=type_hints["data_source_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
            check_type(argname="argument data_refresh_window_days", value=data_refresh_window_days, expected_type=type_hints["data_refresh_window_days"])
            check_type(argname="argument destination_dataset_id", value=destination_dataset_id, expected_type=type_hints["destination_dataset_id"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument email_preferences", value=email_preferences, expected_type=type_hints["email_preferences"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument notification_pubsub_topic", value=notification_pubsub_topic, expected_type=type_hints["notification_pubsub_topic"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument schedule_options", value=schedule_options, expected_type=type_hints["schedule_options"])
            check_type(argname="argument sensitive_params", value=sensitive_params, expected_type=type_hints["sensitive_params"])
            check_type(argname="argument service_account_name", value=service_account_name, expected_type=type_hints["service_account_name"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "data_source_id": data_source_id,
            "display_name": display_name,
            "params": params,
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
        if data_refresh_window_days is not None:
            self._values["data_refresh_window_days"] = data_refresh_window_days
        if destination_dataset_id is not None:
            self._values["destination_dataset_id"] = destination_dataset_id
        if disabled is not None:
            self._values["disabled"] = disabled
        if email_preferences is not None:
            self._values["email_preferences"] = email_preferences
        if id is not None:
            self._values["id"] = id
        if location is not None:
            self._values["location"] = location
        if notification_pubsub_topic is not None:
            self._values["notification_pubsub_topic"] = notification_pubsub_topic
        if project is not None:
            self._values["project"] = project
        if schedule is not None:
            self._values["schedule"] = schedule
        if schedule_options is not None:
            self._values["schedule_options"] = schedule_options
        if sensitive_params is not None:
            self._values["sensitive_params"] = sensitive_params
        if service_account_name is not None:
            self._values["service_account_name"] = service_account_name
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
    def data_source_id(self) -> builtins.str:
        '''The data source id. Cannot be changed once the transfer config is created.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#data_source_id BigqueryDataTransferConfig#data_source_id}
        '''
        result = self._values.get("data_source_id")
        assert result is not None, "Required property 'data_source_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The user specified display name for the transfer config.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#display_name BigqueryDataTransferConfig#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def params(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Parameters specific to each data source.

        For more information see the bq tab in the 'Setting up a data transfer'
        section for each data source. For example the parameters for Cloud Storage transfers are listed here:
        https://cloud.google.com/bigquery-transfer/docs/cloud-storage-transfer#bq

        *NOTE** : If you are attempting to update a parameter that cannot be updated (due to api limitations) `please force recreation of the resource <https://www.terraform.io/cli/state/taint#forcing-re-creation-of-resources>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#params BigqueryDataTransferConfig#params}
        '''
        result = self._values.get("params")
        assert result is not None, "Required property 'params' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def data_refresh_window_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days to look back to automatically refresh the data.

        For example, if dataRefreshWindowDays = 10, then every day BigQuery
        reingests data for [today-10, today-1], rather than ingesting data for
        just [today-1]. Only valid if the data source supports the feature.
        Set the value to 0 to use the default value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#data_refresh_window_days BigqueryDataTransferConfig#data_refresh_window_days}
        '''
        result = self._values.get("data_refresh_window_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def destination_dataset_id(self) -> typing.Optional[builtins.str]:
        '''The BigQuery target dataset id.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#destination_dataset_id BigqueryDataTransferConfig#destination_dataset_id}
        '''
        result = self._values.get("destination_dataset_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''When set to true, no runs are scheduled for a given transfer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#disabled BigqueryDataTransferConfig#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def email_preferences(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigEmailPreferences"]:
        '''email_preferences block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#email_preferences BigqueryDataTransferConfig#email_preferences}
        '''
        result = self._values.get("email_preferences")
        return typing.cast(typing.Optional["BigqueryDataTransferConfigEmailPreferences"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#id BigqueryDataTransferConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#location BigqueryDataTransferConfig#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_pubsub_topic(self) -> typing.Optional[builtins.str]:
        '''Pub/Sub topic where notifications will be sent after transfer runs associated with this transfer config finish.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#notification_pubsub_topic BigqueryDataTransferConfig#notification_pubsub_topic}
        '''
        result = self._values.get("notification_pubsub_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#project BigqueryDataTransferConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Data transfer schedule.

        If the data source does not support a custom
        schedule, this should be empty. If it is empty, the default value for
        the data source will be used. The specified times are in UTC. Examples
        of valid format: 1st,3rd monday of month 15:30, every wed,fri of jan,
        jun 13:15, and first sunday of quarter 00:00. See more explanation
        about the format here:
        https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml#the_schedule_format
        NOTE: the granularity should be at least 8 hours, or less frequent.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#schedule BigqueryDataTransferConfig#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_options(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigScheduleOptions"]:
        '''schedule_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#schedule_options BigqueryDataTransferConfig#schedule_options}
        '''
        result = self._values.get("schedule_options")
        return typing.cast(typing.Optional["BigqueryDataTransferConfigScheduleOptions"], result)

    @builtins.property
    def sensitive_params(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigSensitiveParams"]:
        '''sensitive_params block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#sensitive_params BigqueryDataTransferConfig#sensitive_params}
        '''
        result = self._values.get("sensitive_params")
        return typing.cast(typing.Optional["BigqueryDataTransferConfigSensitiveParams"], result)

    @builtins.property
    def service_account_name(self) -> typing.Optional[builtins.str]:
        '''Service account email.

        If this field is set, transfer config will
        be created with this service account credentials. It requires that
        requesting user calling this API has permissions to act as this service account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#service_account_name BigqueryDataTransferConfig#service_account_name}
        '''
        result = self._values.get("service_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigqueryDataTransferConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#timeouts BigqueryDataTransferConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigqueryDataTransferConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDataTransferConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigEmailPreferences",
    jsii_struct_bases=[],
    name_mapping={"enable_failure_email": "enableFailureEmail"},
)
class BigqueryDataTransferConfigEmailPreferences:
    def __init__(
        self,
        *,
        enable_failure_email: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        '''
        :param enable_failure_email: If true, email notifications will be sent on transfer run failures. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#enable_failure_email BigqueryDataTransferConfig#enable_failure_email}
        '''
        if __debug__:
            def stub(
                *,
                enable_failure_email: typing.Union[builtins.bool, cdktf.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument enable_failure_email", value=enable_failure_email, expected_type=type_hints["enable_failure_email"])
        self._values: typing.Dict[str, typing.Any] = {
            "enable_failure_email": enable_failure_email,
        }

    @builtins.property
    def enable_failure_email(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        '''If true, email notifications will be sent on transfer run failures.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#enable_failure_email BigqueryDataTransferConfig#enable_failure_email}
        '''
        result = self._values.get("enable_failure_email")
        assert result is not None, "Required property 'enable_failure_email' is missing"
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDataTransferConfigEmailPreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDataTransferConfigEmailPreferencesOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigEmailPreferencesOutputReference",
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
    @jsii.member(jsii_name="enableFailureEmailInput")
    def enable_failure_email_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enableFailureEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="enableFailureEmail")
    def enable_failure_email(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enableFailureEmail"))

    @enable_failure_email.setter
    def enable_failure_email(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFailureEmail", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryDataTransferConfigEmailPreferences]:
        return typing.cast(typing.Optional[BigqueryDataTransferConfigEmailPreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDataTransferConfigEmailPreferences],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[BigqueryDataTransferConfigEmailPreferences],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigScheduleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "disable_auto_scheduling": "disableAutoScheduling",
        "end_time": "endTime",
        "start_time": "startTime",
    },
)
class BigqueryDataTransferConfigScheduleOptions:
    def __init__(
        self,
        *,
        disable_auto_scheduling: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable_auto_scheduling: If true, automatic scheduling of data transfer runs for this configuration will be disabled. The runs can be started on ad-hoc basis using transferConfigs.startManualRuns API. When automatic scheduling is disabled, the TransferConfig.schedule field will be ignored. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#disable_auto_scheduling BigqueryDataTransferConfig#disable_auto_scheduling}
        :param end_time: Defines time to stop scheduling transfer runs. A transfer run cannot be scheduled at or after the end time. The end time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#end_time BigqueryDataTransferConfig#end_time}
        :param start_time: Specifies time to start scheduling transfer runs. The first run will be scheduled at or after the start time according to a recurrence pattern defined in the schedule string. The start time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#start_time BigqueryDataTransferConfig#start_time}
        '''
        if __debug__:
            def stub(
                *,
                disable_auto_scheduling: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                end_time: typing.Optional[builtins.str] = None,
                start_time: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument disable_auto_scheduling", value=disable_auto_scheduling, expected_type=type_hints["disable_auto_scheduling"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[str, typing.Any] = {}
        if disable_auto_scheduling is not None:
            self._values["disable_auto_scheduling"] = disable_auto_scheduling
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def disable_auto_scheduling(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''If true, automatic scheduling of data transfer runs for this configuration will be disabled.

        The runs can be started on ad-hoc
        basis using transferConfigs.startManualRuns API. When automatic
        scheduling is disabled, the TransferConfig.schedule field will
        be ignored.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#disable_auto_scheduling BigqueryDataTransferConfig#disable_auto_scheduling}
        '''
        result = self._values.get("disable_auto_scheduling")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Defines time to stop scheduling transfer runs.

        A transfer run cannot be
        scheduled at or after the end time. The end time can be changed at any
        moment. The time when a data transfer can be triggered manually is not
        limited by this option.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#end_time BigqueryDataTransferConfig#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Specifies time to start scheduling transfer runs.

        The first run will be
        scheduled at or after the start time according to a recurrence pattern
        defined in the schedule string. The start time can be changed at any
        moment. The time when a data transfer can be triggered manually is not
        limited by this option.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#start_time BigqueryDataTransferConfig#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDataTransferConfigScheduleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDataTransferConfigScheduleOptionsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigScheduleOptionsOutputReference",
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

    @jsii.member(jsii_name="resetDisableAutoScheduling")
    def reset_disable_auto_scheduling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableAutoScheduling", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="disableAutoSchedulingInput")
    def disable_auto_scheduling_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "disableAutoSchedulingInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="disableAutoScheduling")
    def disable_auto_scheduling(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "disableAutoScheduling"))

    @disable_auto_scheduling.setter
    def disable_auto_scheduling(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableAutoScheduling", value)

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
    ) -> typing.Optional[BigqueryDataTransferConfigScheduleOptions]:
        return typing.cast(typing.Optional[BigqueryDataTransferConfigScheduleOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDataTransferConfigScheduleOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[BigqueryDataTransferConfigScheduleOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigSensitiveParams",
    jsii_struct_bases=[],
    name_mapping={"secret_access_key": "secretAccessKey"},
)
class BigqueryDataTransferConfigSensitiveParams:
    def __init__(self, *, secret_access_key: builtins.str) -> None:
        '''
        :param secret_access_key: The Secret Access Key of the AWS account transferring data from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#secret_access_key BigqueryDataTransferConfig#secret_access_key}
        '''
        if __debug__:
            def stub(*, secret_access_key: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "secret_access_key": secret_access_key,
        }

    @builtins.property
    def secret_access_key(self) -> builtins.str:
        '''The Secret Access Key of the AWS account transferring data from.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#secret_access_key BigqueryDataTransferConfig#secret_access_key}
        '''
        result = self._values.get("secret_access_key")
        assert result is not None, "Required property 'secret_access_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDataTransferConfigSensitiveParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDataTransferConfigSensitiveParamsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigSensitiveParamsOutputReference",
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
    @jsii.member(jsii_name="secretAccessKeyInput")
    def secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKey"))

    @secret_access_key.setter
    def secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryDataTransferConfigSensitiveParams]:
        return typing.cast(typing.Optional[BigqueryDataTransferConfigSensitiveParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDataTransferConfigSensitiveParams],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[BigqueryDataTransferConfigSensitiveParams],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BigqueryDataTransferConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#create BigqueryDataTransferConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#delete BigqueryDataTransferConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#update BigqueryDataTransferConfig#update}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#create BigqueryDataTransferConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#delete BigqueryDataTransferConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_data_transfer_config#update BigqueryDataTransferConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDataTransferConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDataTransferConfigTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigTimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[BigqueryDataTransferConfigTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BigqueryDataTransferConfigTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BigqueryDataTransferConfigTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[BigqueryDataTransferConfigTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "BigqueryDataTransferConfig",
    "BigqueryDataTransferConfigConfig",
    "BigqueryDataTransferConfigEmailPreferences",
    "BigqueryDataTransferConfigEmailPreferencesOutputReference",
    "BigqueryDataTransferConfigScheduleOptions",
    "BigqueryDataTransferConfigScheduleOptionsOutputReference",
    "BigqueryDataTransferConfigSensitiveParams",
    "BigqueryDataTransferConfigSensitiveParamsOutputReference",
    "BigqueryDataTransferConfigTimeouts",
    "BigqueryDataTransferConfigTimeoutsOutputReference",
]

publication.publish()
