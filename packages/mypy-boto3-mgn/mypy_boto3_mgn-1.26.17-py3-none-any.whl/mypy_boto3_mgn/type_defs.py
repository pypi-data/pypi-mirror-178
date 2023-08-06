"""
Type annotations for mgn service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/type_defs/)

Usage::

    ```python
    from mypy_boto3_mgn.type_defs import ApplicationAggregatedStatusTypeDef

    data: ApplicationAggregatedStatusTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ApplicationHealthStatusType,
    ApplicationProgressStatusType,
    BootModeType,
    ChangeServerLifeCycleStateSourceServerLifecycleStateType,
    DataReplicationErrorStringType,
    DataReplicationInitiationStepNameType,
    DataReplicationInitiationStepStatusType,
    DataReplicationStateType,
    FirstBootType,
    InitiatedByType,
    JobLogEventType,
    JobStatusType,
    JobTypeType,
    LaunchDispositionType,
    LaunchStatusType,
    LifeCycleStateType,
    PostLaunchActionExecutionStatusType,
    PostLaunchActionsDeploymentTypeType,
    ReplicationConfigurationDataPlaneRoutingType,
    ReplicationConfigurationDefaultLargeStagingDiskTypeType,
    ReplicationConfigurationEbsEncryptionType,
    ReplicationConfigurationReplicatedDiskStagingDiskTypeType,
    ReplicationTypeType,
    SsmDocumentTypeType,
    TargetInstanceTypeRightSizingMethodType,
    VolumeTypeType,
    WaveHealthStatusType,
    WaveProgressStatusType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ApplicationAggregatedStatusTypeDef",
    "ResponseMetadataTypeDef",
    "ArchiveApplicationRequestRequestTypeDef",
    "ArchiveWaveRequestRequestTypeDef",
    "AssociateApplicationsRequestRequestTypeDef",
    "AssociateSourceServersRequestRequestTypeDef",
    "CPUTypeDef",
    "ChangeServerLifeCycleStateSourceServerLifecycleTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "LaunchTemplateDiskConfTypeDef",
    "LicensingTypeDef",
    "CreateReplicationConfigurationTemplateRequestRequestTypeDef",
    "CreateWaveRequestRequestTypeDef",
    "DataReplicationErrorTypeDef",
    "DataReplicationInfoReplicatedDiskTypeDef",
    "DataReplicationInitiationStepTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "DeleteLaunchConfigurationTemplateRequestRequestTypeDef",
    "DeleteReplicationConfigurationTemplateRequestRequestTypeDef",
    "DeleteSourceServerRequestRequestTypeDef",
    "DeleteVcenterClientRequestRequestTypeDef",
    "DeleteWaveRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeJobLogItemsRequestRequestTypeDef",
    "DescribeJobsRequestFiltersTypeDef",
    "DescribeLaunchConfigurationTemplatesRequestRequestTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestRequestTypeDef",
    "ReplicationConfigurationTemplateTypeDef",
    "DescribeSourceServersRequestFiltersTypeDef",
    "DescribeVcenterClientsRequestRequestTypeDef",
    "VcenterClientTypeDef",
    "DisassociateApplicationsRequestRequestTypeDef",
    "DisassociateSourceServersRequestRequestTypeDef",
    "DisconnectFromServiceRequestRequestTypeDef",
    "DiskTypeDef",
    "FinalizeCutoverRequestRequestTypeDef",
    "GetLaunchConfigurationRequestRequestTypeDef",
    "GetReplicationConfigurationRequestRequestTypeDef",
    "IdentificationHintsTypeDef",
    "JobLogEventDataTypeDef",
    "LaunchedInstanceTypeDef",
    "LifeCycleLastCutoverFinalizedTypeDef",
    "LifeCycleLastCutoverInitiatedTypeDef",
    "LifeCycleLastCutoverRevertedTypeDef",
    "LifeCycleLastTestFinalizedTypeDef",
    "LifeCycleLastTestInitiatedTypeDef",
    "LifeCycleLastTestRevertedTypeDef",
    "ListApplicationsRequestFiltersTypeDef",
    "SourceServerActionsRequestFiltersTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TemplateActionsRequestFiltersTypeDef",
    "ListWavesRequestFiltersTypeDef",
    "MarkAsArchivedRequestRequestTypeDef",
    "NetworkInterfaceTypeDef",
    "OSTypeDef",
    "SsmParameterStoreParameterTypeDef",
    "RemoveSourceServerActionRequestRequestTypeDef",
    "RemoveTemplateActionRequestRequestTypeDef",
    "ReplicationConfigurationReplicatedDiskTypeDef",
    "RetryDataReplicationRequestRequestTypeDef",
    "StartCutoverRequestRequestTypeDef",
    "StartReplicationRequestRequestTypeDef",
    "StartTestRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TerminateTargetInstancesRequestRequestTypeDef",
    "UnarchiveApplicationRequestRequestTypeDef",
    "UnarchiveWaveRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    "UpdateSourceServerReplicationTypeRequestRequestTypeDef",
    "UpdateWaveRequestRequestTypeDef",
    "WaveAggregatedStatusTypeDef",
    "ApplicationTypeDef",
    "ApplicationResponseMetadataTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ReplicationConfigurationTemplateResponseMetadataTypeDef",
    "ChangeServerLifeCycleStateRequestRequestTypeDef",
    "DataReplicationInitiationTypeDef",
    "DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    "DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef",
    "DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef",
    "DescribeJobsRequestDescribeJobsPaginateTypeDef",
    "DescribeJobsRequestRequestTypeDef",
    "DescribeReplicationConfigurationTemplatesResponseTypeDef",
    "DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef",
    "DescribeSourceServersRequestRequestTypeDef",
    "DescribeVcenterClientsResponseTypeDef",
    "JobLogTypeDef",
    "LifeCycleLastCutoverTypeDef",
    "LifeCycleLastTestTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef",
    "ListSourceServerActionsRequestRequestTypeDef",
    "ListTemplateActionsRequestListTemplateActionsPaginateTypeDef",
    "ListTemplateActionsRequestRequestTypeDef",
    "ListWavesRequestListWavesPaginateTypeDef",
    "ListWavesRequestRequestTypeDef",
    "SourcePropertiesTypeDef",
    "PutSourceServerActionRequestRequestTypeDef",
    "PutTemplateActionRequestRequestTypeDef",
    "SourceServerActionDocumentResponseMetadataTypeDef",
    "SourceServerActionDocumentTypeDef",
    "SsmDocumentTypeDef",
    "TemplateActionDocumentResponseMetadataTypeDef",
    "TemplateActionDocumentTypeDef",
    "ReplicationConfigurationTypeDef",
    "UpdateReplicationConfigurationRequestRequestTypeDef",
    "WaveResponseMetadataTypeDef",
    "WaveTypeDef",
    "ListApplicationsResponseTypeDef",
    "DataReplicationInfoTypeDef",
    "DescribeJobLogItemsResponseTypeDef",
    "LifeCycleTypeDef",
    "ListSourceServerActionsResponseTypeDef",
    "JobPostLaunchActionsLaunchStatusTypeDef",
    "PostLaunchActionsTypeDef",
    "ListTemplateActionsResponseTypeDef",
    "ListWavesResponseTypeDef",
    "SourceServerResponseMetadataTypeDef",
    "SourceServerTypeDef",
    "PostLaunchActionsStatusTypeDef",
    "CreateLaunchConfigurationTemplateRequestRequestTypeDef",
    "LaunchConfigurationTemplateResponseMetadataTypeDef",
    "LaunchConfigurationTemplateTypeDef",
    "LaunchConfigurationTypeDef",
    "UpdateLaunchConfigurationRequestRequestTypeDef",
    "UpdateLaunchConfigurationTemplateRequestRequestTypeDef",
    "DescribeSourceServersResponseTypeDef",
    "ParticipatingServerTypeDef",
    "DescribeLaunchConfigurationTemplatesResponseTypeDef",
    "JobTypeDef",
    "DescribeJobsResponseTypeDef",
    "StartCutoverResponseTypeDef",
    "StartTestResponseTypeDef",
    "TerminateTargetInstancesResponseTypeDef",
)

ApplicationAggregatedStatusTypeDef = TypedDict(
    "ApplicationAggregatedStatusTypeDef",
    {
        "healthStatus": ApplicationHealthStatusType,
        "lastUpdateDateTime": str,
        "progressStatus": ApplicationProgressStatusType,
        "totalSourceServers": int,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

ArchiveApplicationRequestRequestTypeDef = TypedDict(
    "ArchiveApplicationRequestRequestTypeDef",
    {
        "applicationID": str,
    },
)

ArchiveWaveRequestRequestTypeDef = TypedDict(
    "ArchiveWaveRequestRequestTypeDef",
    {
        "waveID": str,
    },
)

AssociateApplicationsRequestRequestTypeDef = TypedDict(
    "AssociateApplicationsRequestRequestTypeDef",
    {
        "applicationIDs": Sequence[str],
        "waveID": str,
    },
)

AssociateSourceServersRequestRequestTypeDef = TypedDict(
    "AssociateSourceServersRequestRequestTypeDef",
    {
        "applicationID": str,
        "sourceServerIDs": Sequence[str],
    },
)

CPUTypeDef = TypedDict(
    "CPUTypeDef",
    {
        "cores": int,
        "modelName": str,
    },
    total=False,
)

ChangeServerLifeCycleStateSourceServerLifecycleTypeDef = TypedDict(
    "ChangeServerLifeCycleStateSourceServerLifecycleTypeDef",
    {
        "state": ChangeServerLifeCycleStateSourceServerLifecycleStateType,
    },
)

_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
):
    pass


LaunchTemplateDiskConfTypeDef = TypedDict(
    "LaunchTemplateDiskConfTypeDef",
    {
        "iops": int,
        "throughput": int,
        "volumeType": VolumeTypeType,
    },
    total=False,
)

LicensingTypeDef = TypedDict(
    "LicensingTypeDef",
    {
        "osByol": bool,
    },
    total=False,
)

_RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
    },
)
_OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "ebsEncryptionKeyArn": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateReplicationConfigurationTemplateRequestRequestTypeDef(
    _RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef,
    _OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef,
):
    pass


_RequiredCreateWaveRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWaveRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateWaveRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWaveRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateWaveRequestRequestTypeDef(
    _RequiredCreateWaveRequestRequestTypeDef, _OptionalCreateWaveRequestRequestTypeDef
):
    pass


DataReplicationErrorTypeDef = TypedDict(
    "DataReplicationErrorTypeDef",
    {
        "error": DataReplicationErrorStringType,
        "rawError": str,
    },
    total=False,
)

DataReplicationInfoReplicatedDiskTypeDef = TypedDict(
    "DataReplicationInfoReplicatedDiskTypeDef",
    {
        "backloggedStorageBytes": int,
        "deviceName": str,
        "replicatedStorageBytes": int,
        "rescannedStorageBytes": int,
        "totalStorageBytes": int,
    },
    total=False,
)

DataReplicationInitiationStepTypeDef = TypedDict(
    "DataReplicationInitiationStepTypeDef",
    {
        "name": DataReplicationInitiationStepNameType,
        "status": DataReplicationInitiationStepStatusType,
    },
    total=False,
)

DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "applicationID": str,
    },
)

DeleteJobRequestRequestTypeDef = TypedDict(
    "DeleteJobRequestRequestTypeDef",
    {
        "jobID": str,
    },
)

DeleteLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "DeleteLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)

DeleteReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "DeleteReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)

DeleteSourceServerRequestRequestTypeDef = TypedDict(
    "DeleteSourceServerRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

DeleteVcenterClientRequestRequestTypeDef = TypedDict(
    "DeleteVcenterClientRequestRequestTypeDef",
    {
        "vcenterClientID": str,
    },
)

DeleteWaveRequestRequestTypeDef = TypedDict(
    "DeleteWaveRequestRequestTypeDef",
    {
        "waveID": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredDescribeJobLogItemsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeJobLogItemsRequestRequestTypeDef",
    {
        "jobID": str,
    },
)
_OptionalDescribeJobLogItemsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeJobLogItemsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class DescribeJobLogItemsRequestRequestTypeDef(
    _RequiredDescribeJobLogItemsRequestRequestTypeDef,
    _OptionalDescribeJobLogItemsRequestRequestTypeDef,
):
    pass


DescribeJobsRequestFiltersTypeDef = TypedDict(
    "DescribeJobsRequestFiltersTypeDef",
    {
        "fromDate": str,
        "jobIDs": Sequence[str],
        "toDate": str,
    },
    total=False,
)

DescribeLaunchConfigurationTemplatesRequestRequestTypeDef = TypedDict(
    "DescribeLaunchConfigurationTemplatesRequestRequestTypeDef",
    {
        "launchConfigurationTemplateIDs": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeReplicationConfigurationTemplatesRequestRequestTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "replicationConfigurationTemplateIDs": Sequence[str],
    },
    total=False,
)

_RequiredReplicationConfigurationTemplateTypeDef = TypedDict(
    "_RequiredReplicationConfigurationTemplateTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)
_OptionalReplicationConfigurationTemplateTypeDef = TypedDict(
    "_OptionalReplicationConfigurationTemplateTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "tags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
    },
    total=False,
)


class ReplicationConfigurationTemplateTypeDef(
    _RequiredReplicationConfigurationTemplateTypeDef,
    _OptionalReplicationConfigurationTemplateTypeDef,
):
    pass


DescribeSourceServersRequestFiltersTypeDef = TypedDict(
    "DescribeSourceServersRequestFiltersTypeDef",
    {
        "applicationIDs": Sequence[str],
        "isArchived": bool,
        "lifeCycleStates": Sequence[LifeCycleStateType],
        "replicationTypes": Sequence[ReplicationTypeType],
        "sourceServerIDs": Sequence[str],
    },
    total=False,
)

DescribeVcenterClientsRequestRequestTypeDef = TypedDict(
    "DescribeVcenterClientsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

VcenterClientTypeDef = TypedDict(
    "VcenterClientTypeDef",
    {
        "arn": str,
        "datacenterName": str,
        "hostname": str,
        "lastSeenDatetime": str,
        "sourceServerTags": Dict[str, str],
        "tags": Dict[str, str],
        "vcenterClientID": str,
        "vcenterUUID": str,
    },
    total=False,
)

DisassociateApplicationsRequestRequestTypeDef = TypedDict(
    "DisassociateApplicationsRequestRequestTypeDef",
    {
        "applicationIDs": Sequence[str],
        "waveID": str,
    },
)

DisassociateSourceServersRequestRequestTypeDef = TypedDict(
    "DisassociateSourceServersRequestRequestTypeDef",
    {
        "applicationID": str,
        "sourceServerIDs": Sequence[str],
    },
)

DisconnectFromServiceRequestRequestTypeDef = TypedDict(
    "DisconnectFromServiceRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

DiskTypeDef = TypedDict(
    "DiskTypeDef",
    {
        "bytes": int,
        "deviceName": str,
    },
    total=False,
)

FinalizeCutoverRequestRequestTypeDef = TypedDict(
    "FinalizeCutoverRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

GetLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "GetLaunchConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

GetReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "GetReplicationConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

IdentificationHintsTypeDef = TypedDict(
    "IdentificationHintsTypeDef",
    {
        "awsInstanceID": str,
        "fqdn": str,
        "hostname": str,
        "vmPath": str,
        "vmWareUuid": str,
    },
    total=False,
)

JobLogEventDataTypeDef = TypedDict(
    "JobLogEventDataTypeDef",
    {
        "conversionServerID": str,
        "rawError": str,
        "sourceServerID": str,
        "targetInstanceID": str,
    },
    total=False,
)

LaunchedInstanceTypeDef = TypedDict(
    "LaunchedInstanceTypeDef",
    {
        "ec2InstanceID": str,
        "firstBoot": FirstBootType,
        "jobID": str,
    },
    total=False,
)

LifeCycleLastCutoverFinalizedTypeDef = TypedDict(
    "LifeCycleLastCutoverFinalizedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

LifeCycleLastCutoverInitiatedTypeDef = TypedDict(
    "LifeCycleLastCutoverInitiatedTypeDef",
    {
        "apiCallDateTime": str,
        "jobID": str,
    },
    total=False,
)

LifeCycleLastCutoverRevertedTypeDef = TypedDict(
    "LifeCycleLastCutoverRevertedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

LifeCycleLastTestFinalizedTypeDef = TypedDict(
    "LifeCycleLastTestFinalizedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

LifeCycleLastTestInitiatedTypeDef = TypedDict(
    "LifeCycleLastTestInitiatedTypeDef",
    {
        "apiCallDateTime": str,
        "jobID": str,
    },
    total=False,
)

LifeCycleLastTestRevertedTypeDef = TypedDict(
    "LifeCycleLastTestRevertedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

ListApplicationsRequestFiltersTypeDef = TypedDict(
    "ListApplicationsRequestFiltersTypeDef",
    {
        "applicationIDs": Sequence[str],
        "isArchived": bool,
        "waveIDs": Sequence[str],
    },
    total=False,
)

SourceServerActionsRequestFiltersTypeDef = TypedDict(
    "SourceServerActionsRequestFiltersTypeDef",
    {
        "actionIDs": Sequence[str],
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

TemplateActionsRequestFiltersTypeDef = TypedDict(
    "TemplateActionsRequestFiltersTypeDef",
    {
        "actionIDs": Sequence[str],
    },
    total=False,
)

ListWavesRequestFiltersTypeDef = TypedDict(
    "ListWavesRequestFiltersTypeDef",
    {
        "isArchived": bool,
        "waveIDs": Sequence[str],
    },
    total=False,
)

MarkAsArchivedRequestRequestTypeDef = TypedDict(
    "MarkAsArchivedRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "ips": List[str],
        "isPrimary": bool,
        "macAddress": str,
    },
    total=False,
)

OSTypeDef = TypedDict(
    "OSTypeDef",
    {
        "fullString": str,
    },
    total=False,
)

SsmParameterStoreParameterTypeDef = TypedDict(
    "SsmParameterStoreParameterTypeDef",
    {
        "parameterName": str,
        "parameterType": Literal["STRING"],
    },
)

RemoveSourceServerActionRequestRequestTypeDef = TypedDict(
    "RemoveSourceServerActionRequestRequestTypeDef",
    {
        "actionID": str,
        "sourceServerID": str,
    },
)

RemoveTemplateActionRequestRequestTypeDef = TypedDict(
    "RemoveTemplateActionRequestRequestTypeDef",
    {
        "actionID": str,
        "launchConfigurationTemplateID": str,
    },
)

ReplicationConfigurationReplicatedDiskTypeDef = TypedDict(
    "ReplicationConfigurationReplicatedDiskTypeDef",
    {
        "deviceName": str,
        "iops": int,
        "isBootDisk": bool,
        "stagingDiskType": ReplicationConfigurationReplicatedDiskStagingDiskTypeType,
        "throughput": int,
    },
    total=False,
)

RetryDataReplicationRequestRequestTypeDef = TypedDict(
    "RetryDataReplicationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

_RequiredStartCutoverRequestRequestTypeDef = TypedDict(
    "_RequiredStartCutoverRequestRequestTypeDef",
    {
        "sourceServerIDs": Sequence[str],
    },
)
_OptionalStartCutoverRequestRequestTypeDef = TypedDict(
    "_OptionalStartCutoverRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class StartCutoverRequestRequestTypeDef(
    _RequiredStartCutoverRequestRequestTypeDef, _OptionalStartCutoverRequestRequestTypeDef
):
    pass


StartReplicationRequestRequestTypeDef = TypedDict(
    "StartReplicationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

_RequiredStartTestRequestRequestTypeDef = TypedDict(
    "_RequiredStartTestRequestRequestTypeDef",
    {
        "sourceServerIDs": Sequence[str],
    },
)
_OptionalStartTestRequestRequestTypeDef = TypedDict(
    "_OptionalStartTestRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class StartTestRequestRequestTypeDef(
    _RequiredStartTestRequestRequestTypeDef, _OptionalStartTestRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

_RequiredTerminateTargetInstancesRequestRequestTypeDef = TypedDict(
    "_RequiredTerminateTargetInstancesRequestRequestTypeDef",
    {
        "sourceServerIDs": Sequence[str],
    },
)
_OptionalTerminateTargetInstancesRequestRequestTypeDef = TypedDict(
    "_OptionalTerminateTargetInstancesRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class TerminateTargetInstancesRequestRequestTypeDef(
    _RequiredTerminateTargetInstancesRequestRequestTypeDef,
    _OptionalTerminateTargetInstancesRequestRequestTypeDef,
):
    pass


UnarchiveApplicationRequestRequestTypeDef = TypedDict(
    "UnarchiveApplicationRequestRequestTypeDef",
    {
        "applicationID": str,
    },
)

UnarchiveWaveRequestRequestTypeDef = TypedDict(
    "UnarchiveWaveRequestRequestTypeDef",
    {
        "waveID": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "applicationID": str,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "description": str,
        "name": str,
    },
    total=False,
)


class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass


_RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)
_OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
    },
    total=False,
)


class UpdateReplicationConfigurationTemplateRequestRequestTypeDef(
    _RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef,
    _OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef,
):
    pass


UpdateSourceServerReplicationTypeRequestRequestTypeDef = TypedDict(
    "UpdateSourceServerReplicationTypeRequestRequestTypeDef",
    {
        "replicationType": ReplicationTypeType,
        "sourceServerID": str,
    },
)

_RequiredUpdateWaveRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWaveRequestRequestTypeDef",
    {
        "waveID": str,
    },
)
_OptionalUpdateWaveRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWaveRequestRequestTypeDef",
    {
        "description": str,
        "name": str,
    },
    total=False,
)


class UpdateWaveRequestRequestTypeDef(
    _RequiredUpdateWaveRequestRequestTypeDef, _OptionalUpdateWaveRequestRequestTypeDef
):
    pass


WaveAggregatedStatusTypeDef = TypedDict(
    "WaveAggregatedStatusTypeDef",
    {
        "healthStatus": WaveHealthStatusType,
        "lastUpdateDateTime": str,
        "progressStatus": WaveProgressStatusType,
        "replicationStartedDateTime": str,
        "totalApplications": int,
    },
    total=False,
)

ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "applicationAggregatedStatus": ApplicationAggregatedStatusTypeDef,
        "applicationID": str,
        "arn": str,
        "creationDateTime": str,
        "description": str,
        "isArchived": bool,
        "lastModifiedDateTime": str,
        "name": str,
        "tags": Dict[str, str],
        "waveID": str,
    },
    total=False,
)

ApplicationResponseMetadataTypeDef = TypedDict(
    "ApplicationResponseMetadataTypeDef",
    {
        "applicationAggregatedStatus": ApplicationAggregatedStatusTypeDef,
        "applicationID": str,
        "arn": str,
        "creationDateTime": str,
        "description": str,
        "isArchived": bool,
        "lastModifiedDateTime": str,
        "name": str,
        "tags": Dict[str, str],
        "waveID": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReplicationConfigurationTemplateResponseMetadataTypeDef = TypedDict(
    "ReplicationConfigurationTemplateResponseMetadataTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "replicationConfigurationTemplateID": str,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "tags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ChangeServerLifeCycleStateRequestRequestTypeDef = TypedDict(
    "ChangeServerLifeCycleStateRequestRequestTypeDef",
    {
        "lifeCycle": ChangeServerLifeCycleStateSourceServerLifecycleTypeDef,
        "sourceServerID": str,
    },
)

DataReplicationInitiationTypeDef = TypedDict(
    "DataReplicationInitiationTypeDef",
    {
        "nextAttemptDateTime": str,
        "startDateTime": str,
        "steps": List[DataReplicationInitiationStepTypeDef],
    },
    total=False,
)

_RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef = TypedDict(
    "_RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    {
        "jobID": str,
    },
)
_OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef = TypedDict(
    "_OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef(
    _RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef,
    _OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef,
):
    pass


DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef = TypedDict(
    "DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef",
    {
        "launchConfigurationTemplateIDs": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef",
    {
        "replicationConfigurationTemplateIDs": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef = TypedDict(
    "DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeJobsRequestDescribeJobsPaginateTypeDef = TypedDict(
    "DescribeJobsRequestDescribeJobsPaginateTypeDef",
    {
        "filters": DescribeJobsRequestFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeJobsRequestRequestTypeDef = TypedDict(
    "DescribeJobsRequestRequestTypeDef",
    {
        "filters": DescribeJobsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeReplicationConfigurationTemplatesResponseTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesResponseTypeDef",
    {
        "items": List[ReplicationConfigurationTemplateTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef = TypedDict(
    "DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef",
    {
        "filters": DescribeSourceServersRequestFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeSourceServersRequestRequestTypeDef = TypedDict(
    "DescribeSourceServersRequestRequestTypeDef",
    {
        "filters": DescribeSourceServersRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeVcenterClientsResponseTypeDef = TypedDict(
    "DescribeVcenterClientsResponseTypeDef",
    {
        "items": List[VcenterClientTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobLogTypeDef = TypedDict(
    "JobLogTypeDef",
    {
        "event": JobLogEventType,
        "eventData": JobLogEventDataTypeDef,
        "logDateTime": str,
    },
    total=False,
)

LifeCycleLastCutoverTypeDef = TypedDict(
    "LifeCycleLastCutoverTypeDef",
    {
        "finalized": LifeCycleLastCutoverFinalizedTypeDef,
        "initiated": LifeCycleLastCutoverInitiatedTypeDef,
        "reverted": LifeCycleLastCutoverRevertedTypeDef,
    },
    total=False,
)

LifeCycleLastTestTypeDef = TypedDict(
    "LifeCycleLastTestTypeDef",
    {
        "finalized": LifeCycleLastTestFinalizedTypeDef,
        "initiated": LifeCycleLastTestInitiatedTypeDef,
        "reverted": LifeCycleLastTestRevertedTypeDef,
    },
    total=False,
)

ListApplicationsRequestListApplicationsPaginateTypeDef = TypedDict(
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    {
        "filters": ListApplicationsRequestFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
        "filters": ListApplicationsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef = TypedDict(
    "_RequiredListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef = TypedDict(
    "_OptionalListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef",
    {
        "filters": SourceServerActionsRequestFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef(
    _RequiredListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef,
    _OptionalListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef,
):
    pass


_RequiredListSourceServerActionsRequestRequestTypeDef = TypedDict(
    "_RequiredListSourceServerActionsRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalListSourceServerActionsRequestRequestTypeDef = TypedDict(
    "_OptionalListSourceServerActionsRequestRequestTypeDef",
    {
        "filters": SourceServerActionsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListSourceServerActionsRequestRequestTypeDef(
    _RequiredListSourceServerActionsRequestRequestTypeDef,
    _OptionalListSourceServerActionsRequestRequestTypeDef,
):
    pass


_RequiredListTemplateActionsRequestListTemplateActionsPaginateTypeDef = TypedDict(
    "_RequiredListTemplateActionsRequestListTemplateActionsPaginateTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)
_OptionalListTemplateActionsRequestListTemplateActionsPaginateTypeDef = TypedDict(
    "_OptionalListTemplateActionsRequestListTemplateActionsPaginateTypeDef",
    {
        "filters": TemplateActionsRequestFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTemplateActionsRequestListTemplateActionsPaginateTypeDef(
    _RequiredListTemplateActionsRequestListTemplateActionsPaginateTypeDef,
    _OptionalListTemplateActionsRequestListTemplateActionsPaginateTypeDef,
):
    pass


_RequiredListTemplateActionsRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplateActionsRequestRequestTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)
_OptionalListTemplateActionsRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplateActionsRequestRequestTypeDef",
    {
        "filters": TemplateActionsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListTemplateActionsRequestRequestTypeDef(
    _RequiredListTemplateActionsRequestRequestTypeDef,
    _OptionalListTemplateActionsRequestRequestTypeDef,
):
    pass


ListWavesRequestListWavesPaginateTypeDef = TypedDict(
    "ListWavesRequestListWavesPaginateTypeDef",
    {
        "filters": ListWavesRequestFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListWavesRequestRequestTypeDef = TypedDict(
    "ListWavesRequestRequestTypeDef",
    {
        "filters": ListWavesRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

SourcePropertiesTypeDef = TypedDict(
    "SourcePropertiesTypeDef",
    {
        "cpus": List[CPUTypeDef],
        "disks": List[DiskTypeDef],
        "identificationHints": IdentificationHintsTypeDef,
        "lastUpdatedDateTime": str,
        "networkInterfaces": List[NetworkInterfaceTypeDef],
        "os": OSTypeDef,
        "ramBytes": int,
        "recommendedInstanceType": str,
    },
    total=False,
)

_RequiredPutSourceServerActionRequestRequestTypeDef = TypedDict(
    "_RequiredPutSourceServerActionRequestRequestTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "documentIdentifier": str,
        "order": int,
        "sourceServerID": str,
    },
)
_OptionalPutSourceServerActionRequestRequestTypeDef = TypedDict(
    "_OptionalPutSourceServerActionRequestRequestTypeDef",
    {
        "active": bool,
        "documentVersion": str,
        "mustSucceedForCutover": bool,
        "parameters": Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
    },
    total=False,
)


class PutSourceServerActionRequestRequestTypeDef(
    _RequiredPutSourceServerActionRequestRequestTypeDef,
    _OptionalPutSourceServerActionRequestRequestTypeDef,
):
    pass


_RequiredPutTemplateActionRequestRequestTypeDef = TypedDict(
    "_RequiredPutTemplateActionRequestRequestTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "documentIdentifier": str,
        "launchConfigurationTemplateID": str,
        "order": int,
    },
)
_OptionalPutTemplateActionRequestRequestTypeDef = TypedDict(
    "_OptionalPutTemplateActionRequestRequestTypeDef",
    {
        "active": bool,
        "documentVersion": str,
        "mustSucceedForCutover": bool,
        "operatingSystem": str,
        "parameters": Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
    },
    total=False,
)


class PutTemplateActionRequestRequestTypeDef(
    _RequiredPutTemplateActionRequestRequestTypeDef, _OptionalPutTemplateActionRequestRequestTypeDef
):
    pass


SourceServerActionDocumentResponseMetadataTypeDef = TypedDict(
    "SourceServerActionDocumentResponseMetadataTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "active": bool,
        "documentIdentifier": str,
        "documentVersion": str,
        "mustSucceedForCutover": bool,
        "order": int,
        "parameters": Dict[str, List[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SourceServerActionDocumentTypeDef = TypedDict(
    "SourceServerActionDocumentTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "active": bool,
        "documentIdentifier": str,
        "documentVersion": str,
        "mustSucceedForCutover": bool,
        "order": int,
        "parameters": Dict[str, List[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
    },
    total=False,
)

_RequiredSsmDocumentTypeDef = TypedDict(
    "_RequiredSsmDocumentTypeDef",
    {
        "actionName": str,
        "ssmDocumentName": str,
    },
)
_OptionalSsmDocumentTypeDef = TypedDict(
    "_OptionalSsmDocumentTypeDef",
    {
        "mustSucceedForCutover": bool,
        "parameters": Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
    },
    total=False,
)


class SsmDocumentTypeDef(_RequiredSsmDocumentTypeDef, _OptionalSsmDocumentTypeDef):
    pass


TemplateActionDocumentResponseMetadataTypeDef = TypedDict(
    "TemplateActionDocumentResponseMetadataTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "active": bool,
        "documentIdentifier": str,
        "documentVersion": str,
        "mustSucceedForCutover": bool,
        "operatingSystem": str,
        "order": int,
        "parameters": Dict[str, List[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TemplateActionDocumentTypeDef = TypedDict(
    "TemplateActionDocumentTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "active": bool,
        "documentIdentifier": str,
        "documentVersion": str,
        "mustSucceedForCutover": bool,
        "operatingSystem": str,
        "order": int,
        "parameters": Dict[str, List[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
    },
    total=False,
)

ReplicationConfigurationTypeDef = TypedDict(
    "ReplicationConfigurationTypeDef",
    {
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "name": str,
        "replicatedDisks": List[ReplicationConfigurationReplicatedDiskTypeDef],
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "sourceServerID": str,
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateReplicationConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalUpdateReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateReplicationConfigurationRequestRequestTypeDef",
    {
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "name": str,
        "replicatedDisks": Sequence[ReplicationConfigurationReplicatedDiskTypeDef],
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
    },
    total=False,
)


class UpdateReplicationConfigurationRequestRequestTypeDef(
    _RequiredUpdateReplicationConfigurationRequestRequestTypeDef,
    _OptionalUpdateReplicationConfigurationRequestRequestTypeDef,
):
    pass


WaveResponseMetadataTypeDef = TypedDict(
    "WaveResponseMetadataTypeDef",
    {
        "arn": str,
        "creationDateTime": str,
        "description": str,
        "isArchived": bool,
        "lastModifiedDateTime": str,
        "name": str,
        "tags": Dict[str, str],
        "waveAggregatedStatus": WaveAggregatedStatusTypeDef,
        "waveID": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WaveTypeDef = TypedDict(
    "WaveTypeDef",
    {
        "arn": str,
        "creationDateTime": str,
        "description": str,
        "isArchived": bool,
        "lastModifiedDateTime": str,
        "name": str,
        "tags": Dict[str, str],
        "waveAggregatedStatus": WaveAggregatedStatusTypeDef,
        "waveID": str,
    },
    total=False,
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "items": List[ApplicationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataReplicationInfoTypeDef = TypedDict(
    "DataReplicationInfoTypeDef",
    {
        "dataReplicationError": DataReplicationErrorTypeDef,
        "dataReplicationInitiation": DataReplicationInitiationTypeDef,
        "dataReplicationState": DataReplicationStateType,
        "etaDateTime": str,
        "lagDuration": str,
        "lastSnapshotDateTime": str,
        "replicatedDisks": List[DataReplicationInfoReplicatedDiskTypeDef],
    },
    total=False,
)

DescribeJobLogItemsResponseTypeDef = TypedDict(
    "DescribeJobLogItemsResponseTypeDef",
    {
        "items": List[JobLogTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LifeCycleTypeDef = TypedDict(
    "LifeCycleTypeDef",
    {
        "addedToServiceDateTime": str,
        "elapsedReplicationDuration": str,
        "firstByteDateTime": str,
        "lastCutover": LifeCycleLastCutoverTypeDef,
        "lastSeenByServiceDateTime": str,
        "lastTest": LifeCycleLastTestTypeDef,
        "state": LifeCycleStateType,
    },
    total=False,
)

ListSourceServerActionsResponseTypeDef = TypedDict(
    "ListSourceServerActionsResponseTypeDef",
    {
        "items": List[SourceServerActionDocumentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobPostLaunchActionsLaunchStatusTypeDef = TypedDict(
    "JobPostLaunchActionsLaunchStatusTypeDef",
    {
        "executionID": str,
        "executionStatus": PostLaunchActionExecutionStatusType,
        "failureReason": str,
        "ssmDocument": SsmDocumentTypeDef,
        "ssmDocumentType": SsmDocumentTypeType,
    },
    total=False,
)

PostLaunchActionsTypeDef = TypedDict(
    "PostLaunchActionsTypeDef",
    {
        "cloudWatchLogGroupName": str,
        "deployment": PostLaunchActionsDeploymentTypeType,
        "s3LogBucket": str,
        "s3OutputKeyPrefix": str,
        "ssmDocuments": Sequence[SsmDocumentTypeDef],
    },
    total=False,
)

ListTemplateActionsResponseTypeDef = TypedDict(
    "ListTemplateActionsResponseTypeDef",
    {
        "items": List[TemplateActionDocumentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWavesResponseTypeDef = TypedDict(
    "ListWavesResponseTypeDef",
    {
        "items": List[WaveTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SourceServerResponseMetadataTypeDef = TypedDict(
    "SourceServerResponseMetadataTypeDef",
    {
        "applicationID": str,
        "arn": str,
        "dataReplicationInfo": DataReplicationInfoTypeDef,
        "isArchived": bool,
        "launchedInstance": LaunchedInstanceTypeDef,
        "lifeCycle": LifeCycleTypeDef,
        "replicationType": ReplicationTypeType,
        "sourceProperties": SourcePropertiesTypeDef,
        "sourceServerID": str,
        "tags": Dict[str, str],
        "vcenterClientID": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SourceServerTypeDef = TypedDict(
    "SourceServerTypeDef",
    {
        "applicationID": str,
        "arn": str,
        "dataReplicationInfo": DataReplicationInfoTypeDef,
        "isArchived": bool,
        "launchedInstance": LaunchedInstanceTypeDef,
        "lifeCycle": LifeCycleTypeDef,
        "replicationType": ReplicationTypeType,
        "sourceProperties": SourcePropertiesTypeDef,
        "sourceServerID": str,
        "tags": Dict[str, str],
        "vcenterClientID": str,
    },
    total=False,
)

PostLaunchActionsStatusTypeDef = TypedDict(
    "PostLaunchActionsStatusTypeDef",
    {
        "postLaunchActionsLaunchStatusList": List[JobPostLaunchActionsLaunchStatusTypeDef],
        "ssmAgentDiscoveryDatetime": str,
    },
    total=False,
)

CreateLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "CreateLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "associatePublicIpAddress": bool,
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "enableMapAutoTagging": bool,
        "largeVolumeConf": LaunchTemplateDiskConfTypeDef,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "smallVolumeConf": LaunchTemplateDiskConfTypeDef,
        "smallVolumeMaxSize": int,
        "tags": Mapping[str, str],
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
    },
    total=False,
)

LaunchConfigurationTemplateResponseMetadataTypeDef = TypedDict(
    "LaunchConfigurationTemplateResponseMetadataTypeDef",
    {
        "arn": str,
        "associatePublicIpAddress": bool,
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "ec2LaunchTemplateID": str,
        "enableMapAutoTagging": bool,
        "largeVolumeConf": LaunchTemplateDiskConfTypeDef,
        "launchConfigurationTemplateID": str,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "smallVolumeConf": LaunchTemplateDiskConfTypeDef,
        "smallVolumeMaxSize": int,
        "tags": Dict[str, str],
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredLaunchConfigurationTemplateTypeDef = TypedDict(
    "_RequiredLaunchConfigurationTemplateTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)
_OptionalLaunchConfigurationTemplateTypeDef = TypedDict(
    "_OptionalLaunchConfigurationTemplateTypeDef",
    {
        "arn": str,
        "associatePublicIpAddress": bool,
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "ec2LaunchTemplateID": str,
        "enableMapAutoTagging": bool,
        "largeVolumeConf": LaunchTemplateDiskConfTypeDef,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "smallVolumeConf": LaunchTemplateDiskConfTypeDef,
        "smallVolumeMaxSize": int,
        "tags": Dict[str, str],
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
    },
    total=False,
)


class LaunchConfigurationTemplateTypeDef(
    _RequiredLaunchConfigurationTemplateTypeDef, _OptionalLaunchConfigurationTemplateTypeDef
):
    pass


LaunchConfigurationTypeDef = TypedDict(
    "LaunchConfigurationTypeDef",
    {
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "ec2LaunchTemplateID": str,
        "enableMapAutoTagging": bool,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "name": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "sourceServerID": str,
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLaunchConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalUpdateLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLaunchConfigurationRequestRequestTypeDef",
    {
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "enableMapAutoTagging": bool,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "name": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
    },
    total=False,
)


class UpdateLaunchConfigurationRequestRequestTypeDef(
    _RequiredUpdateLaunchConfigurationRequestRequestTypeDef,
    _OptionalUpdateLaunchConfigurationRequestRequestTypeDef,
):
    pass


_RequiredUpdateLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)
_OptionalUpdateLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "associatePublicIpAddress": bool,
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "enableMapAutoTagging": bool,
        "largeVolumeConf": LaunchTemplateDiskConfTypeDef,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "smallVolumeConf": LaunchTemplateDiskConfTypeDef,
        "smallVolumeMaxSize": int,
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
    },
    total=False,
)


class UpdateLaunchConfigurationTemplateRequestRequestTypeDef(
    _RequiredUpdateLaunchConfigurationTemplateRequestRequestTypeDef,
    _OptionalUpdateLaunchConfigurationTemplateRequestRequestTypeDef,
):
    pass


DescribeSourceServersResponseTypeDef = TypedDict(
    "DescribeSourceServersResponseTypeDef",
    {
        "items": List[SourceServerTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredParticipatingServerTypeDef = TypedDict(
    "_RequiredParticipatingServerTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalParticipatingServerTypeDef = TypedDict(
    "_OptionalParticipatingServerTypeDef",
    {
        "launchStatus": LaunchStatusType,
        "launchedEc2InstanceID": str,
        "postLaunchActionsStatus": PostLaunchActionsStatusTypeDef,
    },
    total=False,
)


class ParticipatingServerTypeDef(
    _RequiredParticipatingServerTypeDef, _OptionalParticipatingServerTypeDef
):
    pass


DescribeLaunchConfigurationTemplatesResponseTypeDef = TypedDict(
    "DescribeLaunchConfigurationTemplatesResponseTypeDef",
    {
        "items": List[LaunchConfigurationTemplateTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredJobTypeDef = TypedDict(
    "_RequiredJobTypeDef",
    {
        "jobID": str,
    },
)
_OptionalJobTypeDef = TypedDict(
    "_OptionalJobTypeDef",
    {
        "arn": str,
        "creationDateTime": str,
        "endDateTime": str,
        "initiatedBy": InitiatedByType,
        "participatingServers": List[ParticipatingServerTypeDef],
        "status": JobStatusType,
        "tags": Dict[str, str],
        "type": JobTypeType,
    },
    total=False,
)


class JobTypeDef(_RequiredJobTypeDef, _OptionalJobTypeDef):
    pass


DescribeJobsResponseTypeDef = TypedDict(
    "DescribeJobsResponseTypeDef",
    {
        "items": List[JobTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartCutoverResponseTypeDef = TypedDict(
    "StartCutoverResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartTestResponseTypeDef = TypedDict(
    "StartTestResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TerminateTargetInstancesResponseTypeDef = TypedDict(
    "TerminateTargetInstancesResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
