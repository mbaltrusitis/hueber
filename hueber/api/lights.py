
from collections import UserDict
import json
from typing import Any
from typing import Dict
from typing import List

from hueber.api._common import Resource
from hueber.api._common import ResourceComposite
from hueber.api._common import Request


class Light(Resource):
    """An individual lightbulb connected to the hub.
    """
    def __init__(self, id, url, **kwds) -> None:
        super(Light, self).__init__(id, kwds["name"], url)
        self.data = kwds  # type: Dict[str, Any]

    def sync(self) -> None:
        request = self._get("/lights/{}".format(self.id_))
        self.data = request

    def push(self, data: str) -> List[Dict[str, str]]:
        request = self._put("/lights/{}/state".format(self.id_), data)
        return request

    def push_attrs(self, data: str) -> List[Dict[str, str]]:
        """Update the attributes of the Light.

        Note:
            Lights only have a name attribute.
        """
        request = self._put("/lights/{}".format(self.id_), data)
        return request

    # TO-DO:
    # Create LightAtributesBuilder in statebuilder.py

    def __repr__(self) -> str:
        return "Light({}, {}, {})".format(self.id_, self["name"], self["type"])


class Lights(ResourceComposite):
    """All of your lights are belong to this.
    """
    def __init__(self, url: str) -> None:
        super(Lights, self).__init__(name="lights", url=url, node=Light)

    def sync(self) -> None:
        self.data = self._get_all()

