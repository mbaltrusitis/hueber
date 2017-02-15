
from collections import UserDict
import datetime as dt
import json
from typing import Any
from typing import Dict
from typing import List
import urllib.request

# from hueber.lib.http import Request

class Request(object):
    """A simple request type to send to a Bridge.

    A Request is a one-time use container to make a request to the Hue bridge. The
    Request's response will be stored as a UTF-8 string and can/should not be updated.

    Note:
        As for now this is only allowing GET, PUT AND POST requests as to not idiotically
        delete something off of the Hub.

    Attrs:
        method (str): can only be one of the values included int ``PERMITTED_METHODS``.
        host (str): IP or hostname of Hue Bridge
        route (str): the path (including a leading slash) to send the request
        body (str): The payload in JSON format to send to the bridge. Defaults to an
                    empty string.
        _data (str) : The serialized JSON resonse from the Hue Bridge

    """
    PERMITTED_METHODS = ("GET", "PUT", "POST")

    def __init__(self, method: str, host: str, route: str, body: str="") -> None:
        if method not in Request.PERMITTED_METHODS:
            raise Exception("Not an accepted HTTP method")
        self.method = method
        self.url = host + route  # type: str
        self.body = body.encode("UTF-8") if body is not "" else None  # type: bytes
        self._data = self._request(self.url, self.body, self.method)  # type: str

    def _request(self, url: str, data: bytes, method: str) -> str:
        """Send a request, read and return the response data as a UTF-8 str.
        """
        try:
            req = urllib.request.Request(url=url, data=data, method=method)
            with urllib.request.urlopen(req) as f:
                return f.read().decode("UTF-8")
        except Exception as err:
            raise err

    @property
    def data(self) -> str:
        return self._data


class Resource(UserDict):
    """Base class for Hue resouces on the Bridge.

    This provides a basic abstraction for sending HTTP requests to Bridge RESTful API
    and its approriate routes.
    """
    def __init__(self, id_: str, name: str, url: str, **kwds) -> None:
        self.id_ = id_
        self.name = name
        self.url = url
        self._last_updated = dt.datetime.utcnow()  # type: dt.datetime

    def _get(self, route) -> Dict[str, Any]:
        req = Request("GET", self.url, route)
        return json.loads(req.data)

    def _put(self, route: str, body: str) -> List[Dict[str, str]]:
        req = Request("PUT", self.url, route, body)
        self._update_time()
        return json.loads(req.data)

    def _post(self, host: str, route: str, body: str) -> List[Dict[str, str]]:
        req = Request("POST", self.url, route, body)
        self._update_time()
        return json.loads(req.data)

    @property
    def last_updated(self) -> dt.datetime:
        return self._last_updated

    @last_updated.setter
    def last_updated(self) -> dt.datetime:
        return self._last_updated

    def _update_time(self) -> None:
        self._last_update = dt.datetime.utcnow()

    def __len__(self):
        raise NotImplementedError

class ResourceComposite(Resource):
    """A collection of Hue resources.

    When fetching the attributes of a category of resources (i.e. /groups, /lights,
    /sensors, etc.) all available attributes are not returned. If you do need these
    then call the ResourceComposite's sync() method which will fetch each resources
    metadata individually. This may put a lot of load on the Bridge.
    """
    def __init__(self, name: str, url: str, node) -> None:
        id_ = None  # type: str
        super().__init__(id_=id_, name=name, url=url)
        self.node = node
        self.data = self._get_all()  # type: Dict[int, Any]

    def _get_all(self) -> Dict[int, Any]:
        request = self._get("/" + self.name)
        return {int(k): self.node(k, self.url, **v) for k, v in request.items()}  # unstring the keys

    def sync(self):
        """Fetch the full set of attributes for every resource in the composite.
        """
        for k, v in self.keys():
            v.sync()

    def push_attrs(self, update: str) -> List[List[Dict[str, str]]]:
        """Push the passed update string to all resources in the composite.
        """
        updates = []
        for k, v in self.keys():
            updates.append(v.push(update))
        return updates

