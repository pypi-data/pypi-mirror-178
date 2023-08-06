# Copyright (c) 2012-2021, Mark Peek <mark@peek.org>
# All rights reserved.
#
# See LICENSE file for full license.

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Resource Explorer"
prefix = "resource-explorer-2"


class Action(BaseAction):
    def __init__(self, action: str = None) -> None:
        super().__init__(prefix, action)


class ARN(BaseARN):
    def __init__(self, resource: str = "", region: str = "", account: str = "") -> None:
        super().__init__(
            service=prefix, resource=resource, region=region, account=account
        )


AssociateDefaultView = Action("AssociateDefaultView")
BatchGetView = Action("BatchGetView")
CreateIndex = Action("CreateIndex")
CreateView = Action("CreateView")
DeleteIndex = Action("DeleteIndex")
DeleteView = Action("DeleteView")
DisassociateDefaultView = Action("DisassociateDefaultView")
GetDefaultView = Action("GetDefaultView")
GetIndex = Action("GetIndex")
GetView = Action("GetView")
ListIndexes = Action("ListIndexes")
ListSupportedResourceTypes = Action("ListSupportedResourceTypes")
ListTagsForResource = Action("ListTagsForResource")
ListViews = Action("ListViews")
Search = Action("Search")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateIndexType = Action("UpdateIndexType")
UpdateView = Action("UpdateView")
