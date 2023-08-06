# Copyright (c) 2012-2021, Mark Peek <mark@peek.org>
# All rights reserved.
#
# See LICENSE file for full license.

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Backup Gateway"
prefix = "backup-gateway"


class Action(BaseAction):
    def __init__(self, action: str = None) -> None:
        super().__init__(prefix, action)


class ARN(BaseARN):
    def __init__(self, resource: str = "", region: str = "", account: str = "") -> None:
        super().__init__(
            service=prefix, resource=resource, region=region, account=account
        )


AssociateGatewayToServer = Action("AssociateGatewayToServer")
Backup = Action("Backup")
CreateGateway = Action("CreateGateway")
DeleteGateway = Action("DeleteGateway")
DeleteHypervisor = Action("DeleteHypervisor")
DisassociateGatewayFromServer = Action("DisassociateGatewayFromServer")
GetGateway = Action("GetGateway")
GetVirtualMachine = Action("GetVirtualMachine")
ImportHypervisorConfiguration = Action("ImportHypervisorConfiguration")
ListGateways = Action("ListGateways")
ListHypervisors = Action("ListHypervisors")
ListTagsForResource = Action("ListTagsForResource")
ListVirtualMachines = Action("ListVirtualMachines")
PutMaintenanceStartTime = Action("PutMaintenanceStartTime")
Restore = Action("Restore")
TagResource = Action("TagResource")
TestHypervisorConfiguration = Action("TestHypervisorConfiguration")
UntagResource = Action("UntagResource")
UpdateGatewayInformation = Action("UpdateGatewayInformation")
UpdateGatewaySoftwareNow = Action("UpdateGatewaySoftwareNow")
UpdateHypervisor = Action("UpdateHypervisor")
