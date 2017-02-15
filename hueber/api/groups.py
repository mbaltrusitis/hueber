
from collections import UserDict
import json
from typing import Any
from typing import Dict
from typing import List

from hueber.api._common import Resource
from hueber.api._common import ResourceComposite
from hueber.api._common import Request


class Group(Resource):
    """A single Group from the Hue bridge.
    """
    def __init__(self, id, url, **kwds):
        super(Group, self).__init__(id, kwds["name"], url)
        self.data = kwds  # type: Dict[str, Any]

    def sync(self) -> None:
        """Fetch the Group's state from the Bridge.
        """
        request = self._get("/groups/{}".format(self.id_))
        self.data = request

    def push(self, data: str) -> List[Dict[str, str]]:
        """Update the state of the member lights of the group.

        This would be similar to calling ``.update()`` to each individual light belonging
        to this group, as seen in self.get("lights", [])
        """
        request = self._put("/groups/{}/action".format(self.id_), data)
        return request

    def push_attrs(self, data: str) -> List[Dict[str, str]]:
        """Update the name and lights membership of group.
        """
        request = self._put("/groups/{}".format(self.id_), data)
        return request

    def __repr__(self) -> str:
        return ("Group({}, {}, {})".format(self.id_, self["name"],
                self.get("class", self.get("type", None))))  # handle Group 0's lack of type


class Groups(ResourceComposite):
    """All Groups known from the Hue Bridge.
    """
    def __init__(self, url: str) -> None:
        super(Groups, self).__init__(name="groups", url=url, node=Group)
        self._add_hidden_group()

    def sync(self) -> None:
        self.data = self._get_all()
        self._add_hidden_group()

    def _add_hidden_group(self) -> None:
        """Add the hidden "all known lights" Group ID 0 since its not returned.

        Group #0 contains all known lights to the bridge. It can be pretty helpful to
        have for making "entire home" changes. I am leaving it here so it is explicitly
        known to exist.
        """
        self[0] = Group('0', self.url, **self._get("/groups/0"))

