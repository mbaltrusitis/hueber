
from typing import Any
from typing import Dict
from hueber.api._common import Resource
from hueber.api._common import ResourceComposite


class Config(Resource):
    """Metadata about the Bridge and all devices known to it.

    The state call is by far the heaviest which is the reason for a lazy switch. If for
    some reason you need the huge blob of all devices, set the default lazy arg to False
    upon instantiation or just call the get_state() method after the fact.

    As for now the Bridge and its /config route are entirely read-only in regards to
    which routes/methods have been implemented.
    """
    def __init__(self, name: str, ip: str, lazy: bool) -> None:
        id_ = None  # type: str
        super(Config, self).__init__(id_, name, ip)
        self.data = self.get_data()
        self.state = self.get_state() if not lazy else None

    def get_data(self) -> Dict[str, Any]:
        request = self._get("/config")
        return request

    def get_state(self) -> Dict[str, Any]:
        request = self._get("")
        return request

