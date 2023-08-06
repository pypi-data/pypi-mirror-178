# Copyright (c) 2012-2021, Mark Peek <mark@peek.org>
# All rights reserved.
#
# See LICENSE file for full license.

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon Managed Streaming for Apache Kafka"
prefix = "kafka"


class Action(BaseAction):
    def __init__(self, action: str = None) -> None:
        super().__init__(prefix, action)


class ARN(BaseARN):
    def __init__(self, resource: str = "", region: str = "", account: str = "") -> None:
        super().__init__(
            service=prefix, resource=resource, region=region, account=account
        )


BatchAssociateScramSecret = Action("BatchAssociateScramSecret")
BatchDisassociateScramSecret = Action("BatchDisassociateScramSecret")
CreateCluster = Action("CreateCluster")
CreateClusterV2 = Action("CreateClusterV2")
CreateConfiguration = Action("CreateConfiguration")
DeleteCluster = Action("DeleteCluster")
DeleteConfiguration = Action("DeleteConfiguration")
DescribeCluster = Action("DescribeCluster")
DescribeClusterOperation = Action("DescribeClusterOperation")
DescribeClusterV2 = Action("DescribeClusterV2")
DescribeConfiguration = Action("DescribeConfiguration")
DescribeConfigurationRevision = Action("DescribeConfigurationRevision")
GetBootstrapBrokers = Action("GetBootstrapBrokers")
GetCompatibleKafkaVersions = Action("GetCompatibleKafkaVersions")
ListClusterOperations = Action("ListClusterOperations")
ListClusters = Action("ListClusters")
ListClustersV2 = Action("ListClustersV2")
ListConfigurationRevisions = Action("ListConfigurationRevisions")
ListConfigurations = Action("ListConfigurations")
ListKafkaVersions = Action("ListKafkaVersions")
ListNodes = Action("ListNodes")
ListScramSecrets = Action("ListScramSecrets")
ListTagsForResource = Action("ListTagsForResource")
RebootBroker = Action("RebootBroker")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateBrokerCount = Action("UpdateBrokerCount")
UpdateBrokerStorage = Action("UpdateBrokerStorage")
UpdateBrokerType = Action("UpdateBrokerType")
UpdateClusterConfiguration = Action("UpdateClusterConfiguration")
UpdateClusterKafkaVersion = Action("UpdateClusterKafkaVersion")
UpdateConfiguration = Action("UpdateConfiguration")
UpdateConnectivity = Action("UpdateConnectivity")
UpdateMonitoring = Action("UpdateMonitoring")
UpdateSecurity = Action("UpdateSecurity")
UpdateStorage = Action("UpdateStorage")
