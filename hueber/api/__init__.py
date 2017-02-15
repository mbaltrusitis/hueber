
from hueber.api import lights
from hueber.api import groups
from hueber.api import config


class Bridge(object):
    """Hue bridge on local network.
    """
    def __init__(self, ip_address: str, user: str, lazy=True) -> None:
        self.ip_address = ip_address
        self.user = user
        self.url = "http://{}/api/{}".format(self.ip_address, self.user)  # type: str
        self.config = config.Config("config", self.url, lazy)
        self.lights = lights.Lights(self.url)
        self.groups = groups.Groups(self.url)

    def __repr__(self) -> str:
        return "Bridge({}, xxxxx...{})".format(self.ip_address, self.user[-9:])

