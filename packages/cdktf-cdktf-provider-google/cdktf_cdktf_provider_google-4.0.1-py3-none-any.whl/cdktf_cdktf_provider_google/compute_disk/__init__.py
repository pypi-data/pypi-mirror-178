'''
# `google_compute_disk`

Refer to the Terraform Registory for docs: [`google_compute_disk`](https://www.terraform.io/docs/providers/google/r/compute_disk).
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


class ComputeDisk(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDisk",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/compute_disk google_compute_disk}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        disk_encryption_key: typing.Optional[typing.Union["ComputeDiskDiskEncryptionKey", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        physical_block_size_bytes: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        provisioned_iops: typing.Optional[jsii.Number] = None,
        size: typing.Optional[jsii.Number] = None,
        snapshot: typing.Optional[builtins.str] = None,
        source_disk: typing.Optional[builtins.str] = None,
        source_image_encryption_key: typing.Optional[typing.Union["ComputeDiskSourceImageEncryptionKey", typing.Dict[str, typing.Any]]] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeDiskSourceSnapshotEncryptionKey", typing.Dict[str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeDiskTimeouts", typing.Dict[str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/compute_disk google_compute_disk} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#name ComputeDisk#name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#description ComputeDisk#description}
        :param disk_encryption_key: disk_encryption_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#disk_encryption_key ComputeDisk#disk_encryption_key}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#id ComputeDisk#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image: The image from which to initialize this disk. This can be one of: the image's 'self_link', 'projects/{project}/global/images/{image}', 'projects/{project}/global/images/family/{family}', 'global/images/{image}', 'global/images/family/{family}', 'family/{family}', '{project}/{family}', '{project}/{image}', '{family}', or '{image}'. If referred by family, the images names must include the family name. If they don't, use the `google_compute_image data source </docs/providers/google/d/compute_image.html>`_. For instance, the image 'centos-6-v20180104' includes its family name 'centos-6'. These images can be referred by family name here. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#image ComputeDisk#image}
        :param labels: Labels to apply to this disk. A list of key->value pairs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#labels ComputeDisk#labels}
        :param physical_block_size_bytes: Physical block size of the persistent disk, in bytes. If not present in a request, a default value is used. Currently supported sizes are 4096 and 16384, other sizes may be added in the future. If an unsupported value is requested, the error message will list the supported values for the caller's project. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#physical_block_size_bytes ComputeDisk#physical_block_size_bytes}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#project ComputeDisk#project}.
        :param provisioned_iops: Indicates how many IOPS must be provisioned for the disk. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#provisioned_iops ComputeDisk#provisioned_iops}
        :param size: Size of the persistent disk, specified in GB. You can specify this field when creating a persistent disk using the 'image' or 'snapshot' parameter, or specify it alone to create an empty persistent disk. If you specify this field along with 'image' or 'snapshot', the value must not be less than the size of the image or the size of the snapshot. ~>**NOTE** If you change the size, Terraform updates the disk size if upsizing is detected but recreates the disk if downsizing is requested. You can add 'lifecycle.prevent_destroy' in the config to prevent destroying and recreating. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#size ComputeDisk#size}
        :param snapshot: The source snapshot used to create this disk. You can provide this as a partial or full URL to the resource. If the snapshot is in another project than this disk, you must supply a full URL. For example, the following are valid values: 'https://www.googleapis.com/compute/v1/projects/project/global/snapshots/snapshot' 'projects/project/global/snapshots/snapshot' 'global/snapshots/snapshot' 'snapshot' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#snapshot ComputeDisk#snapshot}
        :param source_disk: The source disk used to create this disk. You can provide this as a partial or full URL to the resource. For example, the following are valid values: https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/disks/{disk} https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/disks/{disk} projects/{project}/zones/{zone}/disks/{disk} projects/{project}/regions/{region}/disks/{disk} zones/{zone}/disks/{disk} regions/{region}/disks/{disk} Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#source_disk ComputeDisk#source_disk}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#source_image_encryption_key ComputeDisk#source_image_encryption_key}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#source_snapshot_encryption_key ComputeDisk#source_snapshot_encryption_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#timeouts ComputeDisk#timeouts}
        :param type: URL of the disk type resource describing which disk type to use to create the disk. Provide this when creating the disk. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#type ComputeDisk#type}
        :param zone: A reference to the zone where the disk resides. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#zone ComputeDisk#zone}
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
                disk_encryption_key: typing.Optional[typing.Union[ComputeDiskDiskEncryptionKey, typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                image: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                physical_block_size_bytes: typing.Optional[jsii.Number] = None,
                project: typing.Optional[builtins.str] = None,
                provisioned_iops: typing.Optional[jsii.Number] = None,
                size: typing.Optional[jsii.Number] = None,
                snapshot: typing.Optional[builtins.str] = None,
                source_disk: typing.Optional[builtins.str] = None,
                source_image_encryption_key: typing.Optional[typing.Union[ComputeDiskSourceImageEncryptionKey, typing.Dict[str, typing.Any]]] = None,
                source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeDiskSourceSnapshotEncryptionKey, typing.Dict[str, typing.Any]]] = None,
                timeouts: typing.Optional[typing.Union[ComputeDiskTimeouts, typing.Dict[str, typing.Any]]] = None,
                type: typing.Optional[builtins.str] = None,
                zone: typing.Optional[builtins.str] = None,
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
        config = ComputeDiskConfig(
            name=name,
            description=description,
            disk_encryption_key=disk_encryption_key,
            id=id,
            image=image,
            labels=labels,
            physical_block_size_bytes=physical_block_size_bytes,
            project=project,
            provisioned_iops=provisioned_iops,
            size=size,
            snapshot=snapshot,
            source_disk=source_disk,
            source_image_encryption_key=source_image_encryption_key,
            source_snapshot_encryption_key=source_snapshot_encryption_key,
            timeouts=timeouts,
            type=type,
            zone=zone,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putDiskEncryptionKey")
    def put_disk_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        value = ComputeDiskDiskEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskEncryptionKey", [value]))

    @jsii.member(jsii_name="putSourceImageEncryptionKey")
    def put_source_image_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        value = ComputeDiskSourceImageEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceImageEncryptionKey", [value]))

    @jsii.member(jsii_name="putSourceSnapshotEncryptionKey")
    def put_source_snapshot_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        value = ComputeDiskSourceSnapshotEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceSnapshotEncryptionKey", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#create ComputeDisk#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#delete ComputeDisk#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#update ComputeDisk#update}.
        '''
        value = ComputeDiskTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDiskEncryptionKey")
    def reset_disk_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionKey", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetPhysicalBlockSizeBytes")
    def reset_physical_block_size_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhysicalBlockSizeBytes", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProvisionedIops")
    def reset_provisioned_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedIops", []))

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetSnapshot")
    def reset_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshot", []))

    @jsii.member(jsii_name="resetSourceDisk")
    def reset_source_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceDisk", []))

    @jsii.member(jsii_name="resetSourceImageEncryptionKey")
    def reset_source_image_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceImageEncryptionKey", []))

    @jsii.member(jsii_name="resetSourceSnapshotEncryptionKey")
    def reset_source_snapshot_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceSnapshotEncryptionKey", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKey")
    def disk_encryption_key(self) -> "ComputeDiskDiskEncryptionKeyOutputReference":
        return typing.cast("ComputeDiskDiskEncryptionKeyOutputReference", jsii.get(self, "diskEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="labelFingerprint")
    def label_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="lastAttachTimestamp")
    def last_attach_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastAttachTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="lastDetachTimestamp")
    def last_detach_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastDetachTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="sourceDiskId")
    def source_disk_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDiskId"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageEncryptionKey")
    def source_image_encryption_key(
        self,
    ) -> "ComputeDiskSourceImageEncryptionKeyOutputReference":
        return typing.cast("ComputeDiskSourceImageEncryptionKeyOutputReference", jsii.get(self, "sourceImageEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageId")
    def source_image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceImageId"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKey")
    def source_snapshot_encryption_key(
        self,
    ) -> "ComputeDiskSourceSnapshotEncryptionKeyOutputReference":
        return typing.cast("ComputeDiskSourceSnapshotEncryptionKeyOutputReference", jsii.get(self, "sourceSnapshotEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotId")
    def source_snapshot_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSnapshotId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeDiskTimeoutsOutputReference":
        return typing.cast("ComputeDiskTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyInput")
    def disk_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeDiskDiskEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeDiskDiskEncryptionKey"], jsii.get(self, "diskEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalBlockSizeBytesInput")
    def physical_block_size_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "physicalBlockSizeBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedIopsInput")
    def provisioned_iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotInput")
    def snapshot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDiskInput")
    def source_disk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageEncryptionKeyInput")
    def source_image_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeDiskSourceImageEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeDiskSourceImageEncryptionKey"], jsii.get(self, "sourceImageEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKeyInput")
    def source_snapshot_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeDiskSourceSnapshotEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeDiskSourceSnapshotEncryptionKey"], jsii.get(self, "sourceSnapshotEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["ComputeDiskTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ComputeDiskTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

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
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value)

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
    @jsii.member(jsii_name="physicalBlockSizeBytes")
    def physical_block_size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "physicalBlockSizeBytes"))

    @physical_block_size_bytes.setter
    def physical_block_size_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "physicalBlockSizeBytes", value)

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
    @jsii.member(jsii_name="provisionedIops")
    def provisioned_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedIops"))

    @provisioned_iops.setter
    def provisioned_iops(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedIops", value)

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value)

    @builtins.property
    @jsii.member(jsii_name="snapshot")
    def snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshot"))

    @snapshot.setter
    def snapshot(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshot", value)

    @builtins.property
    @jsii.member(jsii_name="sourceDisk")
    def source_disk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDisk"))

    @source_disk.setter
    def source_disk(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDisk", value)

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

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskConfig",
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
        "disk_encryption_key": "diskEncryptionKey",
        "id": "id",
        "image": "image",
        "labels": "labels",
        "physical_block_size_bytes": "physicalBlockSizeBytes",
        "project": "project",
        "provisioned_iops": "provisionedIops",
        "size": "size",
        "snapshot": "snapshot",
        "source_disk": "sourceDisk",
        "source_image_encryption_key": "sourceImageEncryptionKey",
        "source_snapshot_encryption_key": "sourceSnapshotEncryptionKey",
        "timeouts": "timeouts",
        "type": "type",
        "zone": "zone",
    },
)
class ComputeDiskConfig(cdktf.TerraformMetaArguments):
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
        disk_encryption_key: typing.Optional[typing.Union["ComputeDiskDiskEncryptionKey", typing.Dict[str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        physical_block_size_bytes: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        provisioned_iops: typing.Optional[jsii.Number] = None,
        size: typing.Optional[jsii.Number] = None,
        snapshot: typing.Optional[builtins.str] = None,
        source_disk: typing.Optional[builtins.str] = None,
        source_image_encryption_key: typing.Optional[typing.Union["ComputeDiskSourceImageEncryptionKey", typing.Dict[str, typing.Any]]] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeDiskSourceSnapshotEncryptionKey", typing.Dict[str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeDiskTimeouts", typing.Dict[str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#name ComputeDisk#name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#description ComputeDisk#description}
        :param disk_encryption_key: disk_encryption_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#disk_encryption_key ComputeDisk#disk_encryption_key}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#id ComputeDisk#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image: The image from which to initialize this disk. This can be one of: the image's 'self_link', 'projects/{project}/global/images/{image}', 'projects/{project}/global/images/family/{family}', 'global/images/{image}', 'global/images/family/{family}', 'family/{family}', '{project}/{family}', '{project}/{image}', '{family}', or '{image}'. If referred by family, the images names must include the family name. If they don't, use the `google_compute_image data source </docs/providers/google/d/compute_image.html>`_. For instance, the image 'centos-6-v20180104' includes its family name 'centos-6'. These images can be referred by family name here. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#image ComputeDisk#image}
        :param labels: Labels to apply to this disk. A list of key->value pairs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#labels ComputeDisk#labels}
        :param physical_block_size_bytes: Physical block size of the persistent disk, in bytes. If not present in a request, a default value is used. Currently supported sizes are 4096 and 16384, other sizes may be added in the future. If an unsupported value is requested, the error message will list the supported values for the caller's project. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#physical_block_size_bytes ComputeDisk#physical_block_size_bytes}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#project ComputeDisk#project}.
        :param provisioned_iops: Indicates how many IOPS must be provisioned for the disk. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#provisioned_iops ComputeDisk#provisioned_iops}
        :param size: Size of the persistent disk, specified in GB. You can specify this field when creating a persistent disk using the 'image' or 'snapshot' parameter, or specify it alone to create an empty persistent disk. If you specify this field along with 'image' or 'snapshot', the value must not be less than the size of the image or the size of the snapshot. ~>**NOTE** If you change the size, Terraform updates the disk size if upsizing is detected but recreates the disk if downsizing is requested. You can add 'lifecycle.prevent_destroy' in the config to prevent destroying and recreating. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#size ComputeDisk#size}
        :param snapshot: The source snapshot used to create this disk. You can provide this as a partial or full URL to the resource. If the snapshot is in another project than this disk, you must supply a full URL. For example, the following are valid values: 'https://www.googleapis.com/compute/v1/projects/project/global/snapshots/snapshot' 'projects/project/global/snapshots/snapshot' 'global/snapshots/snapshot' 'snapshot' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#snapshot ComputeDisk#snapshot}
        :param source_disk: The source disk used to create this disk. You can provide this as a partial or full URL to the resource. For example, the following are valid values: https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/disks/{disk} https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/disks/{disk} projects/{project}/zones/{zone}/disks/{disk} projects/{project}/regions/{region}/disks/{disk} zones/{zone}/disks/{disk} regions/{region}/disks/{disk} Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#source_disk ComputeDisk#source_disk}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#source_image_encryption_key ComputeDisk#source_image_encryption_key}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#source_snapshot_encryption_key ComputeDisk#source_snapshot_encryption_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#timeouts ComputeDisk#timeouts}
        :param type: URL of the disk type resource describing which disk type to use to create the disk. Provide this when creating the disk. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#type ComputeDisk#type}
        :param zone: A reference to the zone where the disk resides. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#zone ComputeDisk#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(disk_encryption_key, dict):
            disk_encryption_key = ComputeDiskDiskEncryptionKey(**disk_encryption_key)
        if isinstance(source_image_encryption_key, dict):
            source_image_encryption_key = ComputeDiskSourceImageEncryptionKey(**source_image_encryption_key)
        if isinstance(source_snapshot_encryption_key, dict):
            source_snapshot_encryption_key = ComputeDiskSourceSnapshotEncryptionKey(**source_snapshot_encryption_key)
        if isinstance(timeouts, dict):
            timeouts = ComputeDiskTimeouts(**timeouts)
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
                disk_encryption_key: typing.Optional[typing.Union[ComputeDiskDiskEncryptionKey, typing.Dict[str, typing.Any]]] = None,
                id: typing.Optional[builtins.str] = None,
                image: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                physical_block_size_bytes: typing.Optional[jsii.Number] = None,
                project: typing.Optional[builtins.str] = None,
                provisioned_iops: typing.Optional[jsii.Number] = None,
                size: typing.Optional[jsii.Number] = None,
                snapshot: typing.Optional[builtins.str] = None,
                source_disk: typing.Optional[builtins.str] = None,
                source_image_encryption_key: typing.Optional[typing.Union[ComputeDiskSourceImageEncryptionKey, typing.Dict[str, typing.Any]]] = None,
                source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeDiskSourceSnapshotEncryptionKey, typing.Dict[str, typing.Any]]] = None,
                timeouts: typing.Optional[typing.Union[ComputeDiskTimeouts, typing.Dict[str, typing.Any]]] = None,
                type: typing.Optional[builtins.str] = None,
                zone: typing.Optional[builtins.str] = None,
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
            check_type(argname="argument disk_encryption_key", value=disk_encryption_key, expected_type=type_hints["disk_encryption_key"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument physical_block_size_bytes", value=physical_block_size_bytes, expected_type=type_hints["physical_block_size_bytes"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument provisioned_iops", value=provisioned_iops, expected_type=type_hints["provisioned_iops"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument snapshot", value=snapshot, expected_type=type_hints["snapshot"])
            check_type(argname="argument source_disk", value=source_disk, expected_type=type_hints["source_disk"])
            check_type(argname="argument source_image_encryption_key", value=source_image_encryption_key, expected_type=type_hints["source_image_encryption_key"])
            check_type(argname="argument source_snapshot_encryption_key", value=source_snapshot_encryption_key, expected_type=type_hints["source_snapshot_encryption_key"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
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
        if disk_encryption_key is not None:
            self._values["disk_encryption_key"] = disk_encryption_key
        if id is not None:
            self._values["id"] = id
        if image is not None:
            self._values["image"] = image
        if labels is not None:
            self._values["labels"] = labels
        if physical_block_size_bytes is not None:
            self._values["physical_block_size_bytes"] = physical_block_size_bytes
        if project is not None:
            self._values["project"] = project
        if provisioned_iops is not None:
            self._values["provisioned_iops"] = provisioned_iops
        if size is not None:
            self._values["size"] = size
        if snapshot is not None:
            self._values["snapshot"] = snapshot
        if source_disk is not None:
            self._values["source_disk"] = source_disk
        if source_image_encryption_key is not None:
            self._values["source_image_encryption_key"] = source_image_encryption_key
        if source_snapshot_encryption_key is not None:
            self._values["source_snapshot_encryption_key"] = source_snapshot_encryption_key
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type
        if zone is not None:
            self._values["zone"] = zone

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
        '''Name of the resource.

        Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#name ComputeDisk#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#description ComputeDisk#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key(self) -> typing.Optional["ComputeDiskDiskEncryptionKey"]:
        '''disk_encryption_key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#disk_encryption_key ComputeDisk#disk_encryption_key}
        '''
        result = self._values.get("disk_encryption_key")
        return typing.cast(typing.Optional["ComputeDiskDiskEncryptionKey"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#id ComputeDisk#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''The image from which to initialize this disk.

        This can be
        one of: the image's 'self_link', 'projects/{project}/global/images/{image}',
        'projects/{project}/global/images/family/{family}', 'global/images/{image}',
        'global/images/family/{family}', 'family/{family}', '{project}/{family}',
        '{project}/{image}', '{family}', or '{image}'. If referred by family, the
        images names must include the family name. If they don't, use the
        `google_compute_image data source </docs/providers/google/d/compute_image.html>`_.
        For instance, the image 'centos-6-v20180104' includes its family name 'centos-6'.
        These images can be referred by family name here.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#image ComputeDisk#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this disk.  A list of key->value pairs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#labels ComputeDisk#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def physical_block_size_bytes(self) -> typing.Optional[jsii.Number]:
        '''Physical block size of the persistent disk, in bytes.

        If not present
        in a request, a default value is used. Currently supported sizes
        are 4096 and 16384, other sizes may be added in the future.
        If an unsupported value is requested, the error message will list
        the supported values for the caller's project.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#physical_block_size_bytes ComputeDisk#physical_block_size_bytes}
        '''
        result = self._values.get("physical_block_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#project ComputeDisk#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_iops(self) -> typing.Optional[jsii.Number]:
        '''Indicates how many IOPS must be provisioned for the disk.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#provisioned_iops ComputeDisk#provisioned_iops}
        '''
        result = self._values.get("provisioned_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Size of the persistent disk, specified in GB.

        You can specify this
        field when creating a persistent disk using the 'image' or
        'snapshot' parameter, or specify it alone to create an empty
        persistent disk.

        If you specify this field along with 'image' or 'snapshot',
        the value must not be less than the size of the image
        or the size of the snapshot.

        ~>**NOTE** If you change the size, Terraform updates the disk size
        if upsizing is detected but recreates the disk if downsizing is requested.
        You can add 'lifecycle.prevent_destroy' in the config to prevent destroying
        and recreating.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#size ComputeDisk#size}
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot(self) -> typing.Optional[builtins.str]:
        '''The source snapshot used to create this disk.

        You can provide this as
        a partial or full URL to the resource. If the snapshot is in another
        project than this disk, you must supply a full URL. For example, the
        following are valid values:

        'https://www.googleapis.com/compute/v1/projects/project/global/snapshots/snapshot'
        'projects/project/global/snapshots/snapshot'
        'global/snapshots/snapshot'
        'snapshot'

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#snapshot ComputeDisk#snapshot}
        '''
        result = self._values.get("snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_disk(self) -> typing.Optional[builtins.str]:
        '''The source disk used to create this disk.

        You can provide this as a partial or full URL to the resource.
        For example, the following are valid values:

        https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/disks/{disk}
        https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/disks/{disk}
        projects/{project}/zones/{zone}/disks/{disk}
        projects/{project}/regions/{region}/disks/{disk}
        zones/{zone}/disks/{disk}
        regions/{region}/disks/{disk}

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#source_disk ComputeDisk#source_disk}
        '''
        result = self._values.get("source_disk")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_encryption_key(
        self,
    ) -> typing.Optional["ComputeDiskSourceImageEncryptionKey"]:
        '''source_image_encryption_key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#source_image_encryption_key ComputeDisk#source_image_encryption_key}
        '''
        result = self._values.get("source_image_encryption_key")
        return typing.cast(typing.Optional["ComputeDiskSourceImageEncryptionKey"], result)

    @builtins.property
    def source_snapshot_encryption_key(
        self,
    ) -> typing.Optional["ComputeDiskSourceSnapshotEncryptionKey"]:
        '''source_snapshot_encryption_key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#source_snapshot_encryption_key ComputeDisk#source_snapshot_encryption_key}
        '''
        result = self._values.get("source_snapshot_encryption_key")
        return typing.cast(typing.Optional["ComputeDiskSourceSnapshotEncryptionKey"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeDiskTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#timeouts ComputeDisk#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeDiskTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''URL of the disk type resource describing which disk type to use to create the disk.

        Provide this when creating the disk.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#type ComputeDisk#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''A reference to the zone where the disk resides.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#zone ComputeDisk#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskDiskEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
    },
)
class ComputeDiskDiskEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        if __debug__:
            def stub(
                *,
                kms_key_self_link: typing.Optional[builtins.str] = None,
                kms_key_service_account: typing.Optional[builtins.str] = None,
                raw_key: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument kms_key_self_link", value=kms_key_self_link, expected_type=type_hints["kms_key_self_link"])
            check_type(argname="argument kms_key_service_account", value=kms_key_service_account, expected_type=type_hints["kms_key_service_account"])
            check_type(argname="argument raw_key", value=raw_key, expected_type=type_hints["raw_key"])
        self._values: typing.Dict[str, typing.Any] = {}
        if kms_key_self_link is not None:
            self._values["kms_key_self_link"] = kms_key_self_link
        if kms_key_service_account is not None:
            self._values["kms_key_service_account"] = kms_key_service_account
        if raw_key is not None:
            self._values["raw_key"] = raw_key

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self link of the encryption key used to encrypt the disk.

        Also called KmsKeyName
        in the cloud console. Your project's Compute Engine System service account
        ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have
        'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature.
        See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account used for the encryption request for the given KMS key.

        If absent, the Compute Engine Service Agent service account is used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskDiskEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeDiskDiskEncryptionKeyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskDiskEncryptionKeyOutputReference",
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

    @jsii.member(jsii_name="resetKmsKeySelfLink")
    def reset_kms_key_self_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeySelfLink", []))

    @jsii.member(jsii_name="resetKmsKeyServiceAccount")
    def reset_kms_key_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyServiceAccount", []))

    @jsii.member(jsii_name="resetRawKey")
    def reset_raw_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRawKey", []))

    @builtins.property
    @jsii.member(jsii_name="sha256")
    def sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLinkInput")
    def kms_key_self_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeySelfLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccountInput")
    def kms_key_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="rawKeyInput")
    def raw_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rawKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value)

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeDiskDiskEncryptionKey]:
        return typing.cast(typing.Optional[ComputeDiskDiskEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeDiskDiskEncryptionKey],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[ComputeDiskDiskEncryptionKey]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskSourceImageEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
    },
)
class ComputeDiskSourceImageEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        if __debug__:
            def stub(
                *,
                kms_key_self_link: typing.Optional[builtins.str] = None,
                kms_key_service_account: typing.Optional[builtins.str] = None,
                raw_key: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument kms_key_self_link", value=kms_key_self_link, expected_type=type_hints["kms_key_self_link"])
            check_type(argname="argument kms_key_service_account", value=kms_key_service_account, expected_type=type_hints["kms_key_service_account"])
            check_type(argname="argument raw_key", value=raw_key, expected_type=type_hints["raw_key"])
        self._values: typing.Dict[str, typing.Any] = {}
        if kms_key_self_link is not None:
            self._values["kms_key_self_link"] = kms_key_self_link
        if kms_key_service_account is not None:
            self._values["kms_key_service_account"] = kms_key_service_account
        if raw_key is not None:
            self._values["raw_key"] = raw_key

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self link of the encryption key used to encrypt the disk.

        Also called KmsKeyName
        in the cloud console. Your project's Compute Engine System service account
        ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have
        'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature.
        See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account used for the encryption request for the given KMS key.

        If absent, the Compute Engine Service Agent service account is used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskSourceImageEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeDiskSourceImageEncryptionKeyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskSourceImageEncryptionKeyOutputReference",
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

    @jsii.member(jsii_name="resetKmsKeySelfLink")
    def reset_kms_key_self_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeySelfLink", []))

    @jsii.member(jsii_name="resetKmsKeyServiceAccount")
    def reset_kms_key_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyServiceAccount", []))

    @jsii.member(jsii_name="resetRawKey")
    def reset_raw_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRawKey", []))

    @builtins.property
    @jsii.member(jsii_name="sha256")
    def sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLinkInput")
    def kms_key_self_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeySelfLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccountInput")
    def kms_key_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="rawKeyInput")
    def raw_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rawKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value)

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeDiskSourceImageEncryptionKey]:
        return typing.cast(typing.Optional[ComputeDiskSourceImageEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeDiskSourceImageEncryptionKey],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeDiskSourceImageEncryptionKey],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskSourceSnapshotEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
    },
)
class ComputeDiskSourceSnapshotEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        if __debug__:
            def stub(
                *,
                kms_key_self_link: typing.Optional[builtins.str] = None,
                kms_key_service_account: typing.Optional[builtins.str] = None,
                raw_key: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument kms_key_self_link", value=kms_key_self_link, expected_type=type_hints["kms_key_self_link"])
            check_type(argname="argument kms_key_service_account", value=kms_key_service_account, expected_type=type_hints["kms_key_service_account"])
            check_type(argname="argument raw_key", value=raw_key, expected_type=type_hints["raw_key"])
        self._values: typing.Dict[str, typing.Any] = {}
        if kms_key_self_link is not None:
            self._values["kms_key_self_link"] = kms_key_self_link
        if kms_key_service_account is not None:
            self._values["kms_key_service_account"] = kms_key_service_account
        if raw_key is not None:
            self._values["raw_key"] = raw_key

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self link of the encryption key used to encrypt the disk.

        Also called KmsKeyName
        in the cloud console. Your project's Compute Engine System service account
        ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have
        'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature.
        See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account used for the encryption request for the given KMS key.

        If absent, the Compute Engine Service Agent service account is used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskSourceSnapshotEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeDiskSourceSnapshotEncryptionKeyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskSourceSnapshotEncryptionKeyOutputReference",
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

    @jsii.member(jsii_name="resetKmsKeySelfLink")
    def reset_kms_key_self_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeySelfLink", []))

    @jsii.member(jsii_name="resetKmsKeyServiceAccount")
    def reset_kms_key_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyServiceAccount", []))

    @jsii.member(jsii_name="resetRawKey")
    def reset_raw_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRawKey", []))

    @builtins.property
    @jsii.member(jsii_name="sha256")
    def sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLinkInput")
    def kms_key_self_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeySelfLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccountInput")
    def kms_key_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="rawKeyInput")
    def raw_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rawKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value)

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeDiskSourceSnapshotEncryptionKey]:
        return typing.cast(typing.Optional[ComputeDiskSourceSnapshotEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeDiskSourceSnapshotEncryptionKey],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[ComputeDiskSourceSnapshotEncryptionKey],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeDiskTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#create ComputeDisk#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#delete ComputeDisk#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#update ComputeDisk#update}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#create ComputeDisk#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#delete ComputeDisk#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_disk#update ComputeDisk#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeDiskTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskTimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[ComputeDiskTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ComputeDiskTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ComputeDiskTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[ComputeDiskTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ComputeDisk",
    "ComputeDiskConfig",
    "ComputeDiskDiskEncryptionKey",
    "ComputeDiskDiskEncryptionKeyOutputReference",
    "ComputeDiskSourceImageEncryptionKey",
    "ComputeDiskSourceImageEncryptionKeyOutputReference",
    "ComputeDiskSourceSnapshotEncryptionKey",
    "ComputeDiskSourceSnapshotEncryptionKeyOutputReference",
    "ComputeDiskTimeouts",
    "ComputeDiskTimeoutsOutputReference",
]

publication.publish()
