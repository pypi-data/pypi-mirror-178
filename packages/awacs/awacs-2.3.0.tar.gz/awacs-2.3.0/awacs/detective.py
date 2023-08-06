# Copyright (c) 2012-2021, Mark Peek <mark@peek.org>
# All rights reserved.
#
# See LICENSE file for full license.

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon Detective"
prefix = "detective"


class Action(BaseAction):
    def __init__(self, action: str = None) -> None:
        super().__init__(prefix, action)


class ARN(BaseARN):
    def __init__(self, resource: str = "", region: str = "", account: str = "") -> None:
        super().__init__(
            service=prefix, resource=resource, region=region, account=account
        )


AcceptInvitation = Action("AcceptInvitation")
BatchGetGraphMemberDatasources = Action("BatchGetGraphMemberDatasources")
BatchGetMembershipDatasources = Action("BatchGetMembershipDatasources")
CreateGraph = Action("CreateGraph")
CreateMembers = Action("CreateMembers")
DeleteGraph = Action("DeleteGraph")
DeleteMembers = Action("DeleteMembers")
DescribeOrganizationConfiguration = Action("DescribeOrganizationConfiguration")
DisableOrganizationAdminAccount = Action("DisableOrganizationAdminAccount")
DisassociateMembership = Action("DisassociateMembership")
EnableOrganizationAdminAccount = Action("EnableOrganizationAdminAccount")
GetFreeTrialEligibility = Action("GetFreeTrialEligibility")
GetGraphIngestState = Action("GetGraphIngestState")
GetMembers = Action("GetMembers")
GetPricingInformation = Action("GetPricingInformation")
GetUsageInformation = Action("GetUsageInformation")
ListDatasourcePackages = Action("ListDatasourcePackages")
ListGraphs = Action("ListGraphs")
ListHighDegreeEntities = Action("ListHighDegreeEntities")
ListInvitations = Action("ListInvitations")
ListMembers = Action("ListMembers")
ListOrganizationAdminAccount = Action("ListOrganizationAdminAccount")
ListOrganizationAdminAccounts = Action("ListOrganizationAdminAccounts")
ListTagsForResource = Action("ListTagsForResource")
RejectInvitation = Action("RejectInvitation")
SearchGraph = Action("SearchGraph")
StartMonitoringMember = Action("StartMonitoringMember")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateDatasourcePackages = Action("UpdateDatasourcePackages")
UpdateOrganizationConfiguration = Action("UpdateOrganizationConfiguration")
