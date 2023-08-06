'''
# `google_bigquery_analytics_hub_listing`

Refer to the Terraform Registory for docs: [`google_bigquery_analytics_hub_listing`](https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing).
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


class BigqueryAnalyticsHubListing(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListing",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing google_bigquery_analytics_hub_listing}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        bigquery_dataset: typing.Union["BigqueryAnalyticsHubListingBigqueryDataset", typing.Dict[str, typing.Any]],
        data_exchange_id: builtins.str,
        display_name: builtins.str,
        listing_id: builtins.str,
        location: builtins.str,
        categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        data_provider: typing.Optional[typing.Union["BigqueryAnalyticsHubListingDataProvider", typing.Dict[str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[typing.Union["BigqueryAnalyticsHubListingPublisher", typing.Dict[str, typing.Any]]] = None,
        request_access: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryAnalyticsHubListingTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing google_bigquery_analytics_hub_listing} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bigquery_dataset: bigquery_dataset block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#bigquery_dataset BigqueryAnalyticsHubListing#bigquery_dataset}
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#data_exchange_id BigqueryAnalyticsHubListing#data_exchange_id}
        :param display_name: Human-readable display name of the listing. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#display_name BigqueryAnalyticsHubListing#display_name}
        :param listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#listing_id BigqueryAnalyticsHubListing#listing_id}
        :param location: The name of the location this data exchange listing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#location BigqueryAnalyticsHubListing#location}
        :param categories: Categories of the listing. Up to two categories are allowed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#categories BigqueryAnalyticsHubListing#categories}
        :param data_provider: data_provider block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#data_provider BigqueryAnalyticsHubListing#data_provider}
        :param description: Short description of the listing. The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#description BigqueryAnalyticsHubListing#description}
        :param documentation: Documentation describing the listing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#documentation BigqueryAnalyticsHubListing#documentation}
        :param icon: Base64 encoded image representing the listing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#icon BigqueryAnalyticsHubListing#icon}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#id BigqueryAnalyticsHubListing#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param primary_contact: Email or URL of the primary point of contact of the listing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#project BigqueryAnalyticsHubListing#project}.
        :param publisher: publisher block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#publisher BigqueryAnalyticsHubListing#publisher}
        :param request_access: Email or URL of the request access of the listing. Subscribers can use this reference to request access. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#request_access BigqueryAnalyticsHubListing#request_access}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#timeouts BigqueryAnalyticsHubListing#timeouts}
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
                bigquery_dataset: typing.Union[BigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[str, typing.Any]],
                data_exchange_id: builtins.str,
                display_name: builtins.str,
                listing_id: builtins.str,
                location: builtins.str,
                categories: typing.Optional[typing.Sequence[builtins.str]] = None,
                data_provider: typing.Optional[typing.Union[BigqueryAnalyticsHubListingDataProvider, typing.Dict[str, typing.Any]]] = None,
                description: typing.Optional[builtins.str] = None,
                documentation: typing.Optional[builtins.str] = None,
                icon: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                primary_contact: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                publisher: typing.Optional[typing.Union[BigqueryAnalyticsHubListingPublisher, typing.Dict[str, typing.Any]]] = None,
                request_access: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union[BigqueryAnalyticsHubListingTimeouts, typing.Dict[str, typing.Any]]] = None,
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
        config = BigqueryAnalyticsHubListingConfig(
            bigquery_dataset=bigquery_dataset,
            data_exchange_id=data_exchange_id,
            display_name=display_name,
            listing_id=listing_id,
            location=location,
            categories=categories,
            data_provider=data_provider,
            description=description,
            documentation=documentation,
            icon=icon,
            id=id,
            primary_contact=primary_contact,
            project=project,
            publisher=publisher,
            request_access=request_access,
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

    @jsii.member(jsii_name="putBigqueryDataset")
    def put_bigquery_dataset(self, *, dataset: builtins.str) -> None:
        '''
        :param dataset: Resource name of the dataset source for this listing. e.g. projects/myproject/datasets/123. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#dataset BigqueryAnalyticsHubListing#dataset}
        '''
        value = BigqueryAnalyticsHubListingBigqueryDataset(dataset=dataset)

        return typing.cast(None, jsii.invoke(self, "putBigqueryDataset", [value]))

    @jsii.member(jsii_name="putDataProvider")
    def put_data_provider(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the data provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the data provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        value = BigqueryAnalyticsHubListingDataProvider(
            name=name, primary_contact=primary_contact
        )

        return typing.cast(None, jsii.invoke(self, "putDataProvider", [value]))

    @jsii.member(jsii_name="putPublisher")
    def put_publisher(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the listing publisher. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the listing publisher. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        value = BigqueryAnalyticsHubListingPublisher(
            name=name, primary_contact=primary_contact
        )

        return typing.cast(None, jsii.invoke(self, "putPublisher", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#create BigqueryAnalyticsHubListing#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#delete BigqueryAnalyticsHubListing#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#update BigqueryAnalyticsHubListing#update}.
        '''
        value = BigqueryAnalyticsHubListingTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCategories")
    def reset_categories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategories", []))

    @jsii.member(jsii_name="resetDataProvider")
    def reset_data_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProvider", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDocumentation")
    def reset_documentation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentation", []))

    @jsii.member(jsii_name="resetIcon")
    def reset_icon(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcon", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPrimaryContact")
    def reset_primary_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContact", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPublisher")
    def reset_publisher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublisher", []))

    @jsii.member(jsii_name="resetRequestAccess")
    def reset_request_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestAccess", []))

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
    @jsii.member(jsii_name="bigqueryDataset")
    def bigquery_dataset(
        self,
    ) -> "BigqueryAnalyticsHubListingBigqueryDatasetOutputReference":
        return typing.cast("BigqueryAnalyticsHubListingBigqueryDatasetOutputReference", jsii.get(self, "bigqueryDataset"))

    @builtins.property
    @jsii.member(jsii_name="dataProvider")
    def data_provider(self) -> "BigqueryAnalyticsHubListingDataProviderOutputReference":
        return typing.cast("BigqueryAnalyticsHubListingDataProviderOutputReference", jsii.get(self, "dataProvider"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> "BigqueryAnalyticsHubListingPublisherOutputReference":
        return typing.cast("BigqueryAnalyticsHubListingPublisherOutputReference", jsii.get(self, "publisher"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigqueryAnalyticsHubListingTimeoutsOutputReference":
        return typing.cast("BigqueryAnalyticsHubListingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDatasetInput")
    def bigquery_dataset_input(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubListingBigqueryDataset"]:
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingBigqueryDataset"], jsii.get(self, "bigqueryDatasetInput"))

    @builtins.property
    @jsii.member(jsii_name="categoriesInput")
    def categories_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "categoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataExchangeIdInput")
    def data_exchange_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataExchangeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProviderInput")
    def data_provider_input(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubListingDataProvider"]:
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingDataProvider"], jsii.get(self, "dataProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="documentationInput")
    def documentation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentationInput"))

    @builtins.property
    @jsii.member(jsii_name="iconInput")
    def icon_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iconInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="listingIdInput")
    def listing_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listingIdInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContactInput")
    def primary_contact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryContactInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubListingPublisher"]:
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingPublisher"], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="requestAccessInput")
    def request_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["BigqueryAnalyticsHubListingTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["BigqueryAnalyticsHubListingTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="categories")
    def categories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "categories"))

    @categories.setter
    def categories(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "categories", value)

    @builtins.property
    @jsii.member(jsii_name="dataExchangeId")
    def data_exchange_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataExchangeId"))

    @data_exchange_id.setter
    def data_exchange_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataExchangeId", value)

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
    @jsii.member(jsii_name="documentation")
    def documentation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentation"))

    @documentation.setter
    def documentation(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentation", value)

    @builtins.property
    @jsii.member(jsii_name="icon")
    def icon(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "icon"))

    @icon.setter
    def icon(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icon", value)

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
    @jsii.member(jsii_name="listingId")
    def listing_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listingId"))

    @listing_id.setter
    def listing_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listingId", value)

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
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value)

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
    @jsii.member(jsii_name="requestAccess")
    def request_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestAccess"))

    @request_access.setter
    def request_access(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestAccess", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingBigqueryDataset",
    jsii_struct_bases=[],
    name_mapping={"dataset": "dataset"},
)
class BigqueryAnalyticsHubListingBigqueryDataset:
    def __init__(self, *, dataset: builtins.str) -> None:
        '''
        :param dataset: Resource name of the dataset source for this listing. e.g. projects/myproject/datasets/123. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#dataset BigqueryAnalyticsHubListing#dataset}
        '''
        if __debug__:
            def stub(*, dataset: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
        self._values: typing.Dict[str, typing.Any] = {
            "dataset": dataset,
        }

    @builtins.property
    def dataset(self) -> builtins.str:
        '''Resource name of the dataset source for this listing. e.g. projects/myproject/datasets/123.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#dataset BigqueryAnalyticsHubListing#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingBigqueryDataset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubListingBigqueryDatasetOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingBigqueryDatasetOutputReference",
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
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @dataset.setter
    def dataset(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataset", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryAnalyticsHubListingBigqueryDataset]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubListingBigqueryDataset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryAnalyticsHubListingBigqueryDataset],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[BigqueryAnalyticsHubListingBigqueryDataset],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bigquery_dataset": "bigqueryDataset",
        "data_exchange_id": "dataExchangeId",
        "display_name": "displayName",
        "listing_id": "listingId",
        "location": "location",
        "categories": "categories",
        "data_provider": "dataProvider",
        "description": "description",
        "documentation": "documentation",
        "icon": "icon",
        "id": "id",
        "primary_contact": "primaryContact",
        "project": "project",
        "publisher": "publisher",
        "request_access": "requestAccess",
        "timeouts": "timeouts",
    },
)
class BigqueryAnalyticsHubListingConfig(cdktf.TerraformMetaArguments):
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
        bigquery_dataset: typing.Union[BigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[str, typing.Any]],
        data_exchange_id: builtins.str,
        display_name: builtins.str,
        listing_id: builtins.str,
        location: builtins.str,
        categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        data_provider: typing.Optional[typing.Union["BigqueryAnalyticsHubListingDataProvider", typing.Dict[str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[typing.Union["BigqueryAnalyticsHubListingPublisher", typing.Dict[str, typing.Any]]] = None,
        request_access: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryAnalyticsHubListingTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bigquery_dataset: bigquery_dataset block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#bigquery_dataset BigqueryAnalyticsHubListing#bigquery_dataset}
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#data_exchange_id BigqueryAnalyticsHubListing#data_exchange_id}
        :param display_name: Human-readable display name of the listing. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#display_name BigqueryAnalyticsHubListing#display_name}
        :param listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#listing_id BigqueryAnalyticsHubListing#listing_id}
        :param location: The name of the location this data exchange listing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#location BigqueryAnalyticsHubListing#location}
        :param categories: Categories of the listing. Up to two categories are allowed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#categories BigqueryAnalyticsHubListing#categories}
        :param data_provider: data_provider block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#data_provider BigqueryAnalyticsHubListing#data_provider}
        :param description: Short description of the listing. The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#description BigqueryAnalyticsHubListing#description}
        :param documentation: Documentation describing the listing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#documentation BigqueryAnalyticsHubListing#documentation}
        :param icon: Base64 encoded image representing the listing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#icon BigqueryAnalyticsHubListing#icon}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#id BigqueryAnalyticsHubListing#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param primary_contact: Email or URL of the primary point of contact of the listing. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#project BigqueryAnalyticsHubListing#project}.
        :param publisher: publisher block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#publisher BigqueryAnalyticsHubListing#publisher}
        :param request_access: Email or URL of the request access of the listing. Subscribers can use this reference to request access. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#request_access BigqueryAnalyticsHubListing#request_access}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#timeouts BigqueryAnalyticsHubListing#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bigquery_dataset, dict):
            bigquery_dataset = BigqueryAnalyticsHubListingBigqueryDataset(**bigquery_dataset)
        if isinstance(data_provider, dict):
            data_provider = BigqueryAnalyticsHubListingDataProvider(**data_provider)
        if isinstance(publisher, dict):
            publisher = BigqueryAnalyticsHubListingPublisher(**publisher)
        if isinstance(timeouts, dict):
            timeouts = BigqueryAnalyticsHubListingTimeouts(**timeouts)
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
                bigquery_dataset: typing.Union[BigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[str, typing.Any]],
                data_exchange_id: builtins.str,
                display_name: builtins.str,
                listing_id: builtins.str,
                location: builtins.str,
                categories: typing.Optional[typing.Sequence[builtins.str]] = None,
                data_provider: typing.Optional[typing.Union[BigqueryAnalyticsHubListingDataProvider, typing.Dict[str, typing.Any]]] = None,
                description: typing.Optional[builtins.str] = None,
                documentation: typing.Optional[builtins.str] = None,
                icon: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                primary_contact: typing.Optional[builtins.str] = None,
                project: typing.Optional[builtins.str] = None,
                publisher: typing.Optional[typing.Union[BigqueryAnalyticsHubListingPublisher, typing.Dict[str, typing.Any]]] = None,
                request_access: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union[BigqueryAnalyticsHubListingTimeouts, typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument bigquery_dataset", value=bigquery_dataset, expected_type=type_hints["bigquery_dataset"])
            check_type(argname="argument data_exchange_id", value=data_exchange_id, expected_type=type_hints["data_exchange_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument listing_id", value=listing_id, expected_type=type_hints["listing_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument categories", value=categories, expected_type=type_hints["categories"])
            check_type(argname="argument data_provider", value=data_provider, expected_type=type_hints["data_provider"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument documentation", value=documentation, expected_type=type_hints["documentation"])
            check_type(argname="argument icon", value=icon, expected_type=type_hints["icon"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument request_access", value=request_access, expected_type=type_hints["request_access"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "bigquery_dataset": bigquery_dataset,
            "data_exchange_id": data_exchange_id,
            "display_name": display_name,
            "listing_id": listing_id,
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
        if categories is not None:
            self._values["categories"] = categories
        if data_provider is not None:
            self._values["data_provider"] = data_provider
        if description is not None:
            self._values["description"] = description
        if documentation is not None:
            self._values["documentation"] = documentation
        if icon is not None:
            self._values["icon"] = icon
        if id is not None:
            self._values["id"] = id
        if primary_contact is not None:
            self._values["primary_contact"] = primary_contact
        if project is not None:
            self._values["project"] = project
        if publisher is not None:
            self._values["publisher"] = publisher
        if request_access is not None:
            self._values["request_access"] = request_access
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
    def bigquery_dataset(self) -> BigqueryAnalyticsHubListingBigqueryDataset:
        '''bigquery_dataset block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#bigquery_dataset BigqueryAnalyticsHubListing#bigquery_dataset}
        '''
        result = self._values.get("bigquery_dataset")
        assert result is not None, "Required property 'bigquery_dataset' is missing"
        return typing.cast(BigqueryAnalyticsHubListingBigqueryDataset, result)

    @builtins.property
    def data_exchange_id(self) -> builtins.str:
        '''The ID of the data exchange.

        Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#data_exchange_id BigqueryAnalyticsHubListing#data_exchange_id}
        '''
        result = self._values.get("data_exchange_id")
        assert result is not None, "Required property 'data_exchange_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Human-readable display name of the listing.

        The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#display_name BigqueryAnalyticsHubListing#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def listing_id(self) -> builtins.str:
        '''The ID of the listing.

        Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#listing_id BigqueryAnalyticsHubListing#listing_id}
        '''
        result = self._values.get("listing_id")
        assert result is not None, "Required property 'listing_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this data exchange listing.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#location BigqueryAnalyticsHubListing#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Categories of the listing. Up to two categories are allowed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#categories BigqueryAnalyticsHubListing#categories}
        '''
        result = self._values.get("categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def data_provider(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubListingDataProvider"]:
        '''data_provider block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#data_provider BigqueryAnalyticsHubListing#data_provider}
        '''
        result = self._values.get("data_provider")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingDataProvider"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Short description of the listing.

        The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#description BigqueryAnalyticsHubListing#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def documentation(self) -> typing.Optional[builtins.str]:
        '''Documentation describing the listing.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#documentation BigqueryAnalyticsHubListing#documentation}
        '''
        result = self._values.get("documentation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def icon(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded image representing the listing.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#icon BigqueryAnalyticsHubListing#icon}
        '''
        result = self._values.get("icon")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#id BigqueryAnalyticsHubListing#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the primary point of contact of the listing.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#project BigqueryAnalyticsHubListing#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher(self) -> typing.Optional["BigqueryAnalyticsHubListingPublisher"]:
        '''publisher block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#publisher BigqueryAnalyticsHubListing#publisher}
        '''
        result = self._values.get("publisher")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingPublisher"], result)

    @builtins.property
    def request_access(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the request access of the listing. Subscribers can use this reference to request access.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#request_access BigqueryAnalyticsHubListing#request_access}
        '''
        result = self._values.get("request_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigqueryAnalyticsHubListingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#timeouts BigqueryAnalyticsHubListing#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingDataProvider",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "primary_contact": "primaryContact"},
)
class BigqueryAnalyticsHubListingDataProvider:
    def __init__(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the data provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the data provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        if __debug__:
            def stub(
                *,
                name: builtins.str,
                primary_contact: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if primary_contact is not None:
            self._values["primary_contact"] = primary_contact

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the data provider.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the data provider.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingDataProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubListingDataProviderOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingDataProviderOutputReference",
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

    @jsii.member(jsii_name="resetPrimaryContact")
    def reset_primary_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContact", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContactInput")
    def primary_contact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryContactInput"))

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
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryAnalyticsHubListingDataProvider]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubListingDataProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryAnalyticsHubListingDataProvider],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[BigqueryAnalyticsHubListingDataProvider],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingPublisher",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "primary_contact": "primaryContact"},
)
class BigqueryAnalyticsHubListingPublisher:
    def __init__(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the listing publisher. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the listing publisher. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        if __debug__:
            def stub(
                *,
                name: builtins.str,
                primary_contact: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if primary_contact is not None:
            self._values["primary_contact"] = primary_contact

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the listing publisher.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the listing publisher.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingPublisher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubListingPublisherOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingPublisherOutputReference",
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

    @jsii.member(jsii_name="resetPrimaryContact")
    def reset_primary_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContact", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContactInput")
    def primary_contact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryContactInput"))

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
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryAnalyticsHubListingPublisher]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubListingPublisher], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryAnalyticsHubListingPublisher],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[BigqueryAnalyticsHubListingPublisher],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BigqueryAnalyticsHubListingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#create BigqueryAnalyticsHubListing#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#delete BigqueryAnalyticsHubListing#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#update BigqueryAnalyticsHubListing#update}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#create BigqueryAnalyticsHubListing#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#delete BigqueryAnalyticsHubListing#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_analytics_hub_listing#update BigqueryAnalyticsHubListing#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubListingTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingTimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[BigqueryAnalyticsHubListingTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BigqueryAnalyticsHubListingTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BigqueryAnalyticsHubListingTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[BigqueryAnalyticsHubListingTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "BigqueryAnalyticsHubListing",
    "BigqueryAnalyticsHubListingBigqueryDataset",
    "BigqueryAnalyticsHubListingBigqueryDatasetOutputReference",
    "BigqueryAnalyticsHubListingConfig",
    "BigqueryAnalyticsHubListingDataProvider",
    "BigqueryAnalyticsHubListingDataProviderOutputReference",
    "BigqueryAnalyticsHubListingPublisher",
    "BigqueryAnalyticsHubListingPublisherOutputReference",
    "BigqueryAnalyticsHubListingTimeouts",
    "BigqueryAnalyticsHubListingTimeoutsOutputReference",
]

publication.publish()
