from .Service import Service
from .domain import Domain
from .errors import *
from requests import post, get, delete
from .config import base


class StacketClient:
    def __init__(self, token: str = None):
        if not token:
            raise MissingArgument("Token wasn't entered")
        self.__token__ = token

    def verify(self):
        result = post(f"{base}/auth/verify", {"token": self.__token__})
        if "state" in result.json() and result.json()["state"] == "verified":
            return True
        return False

    def get_services(self):
        result = get(f"{base}/services/", headers={"Authorization": self.__token__})
        Json = result.json()
        if not 200 <= result.status_code < 300:
            raise ClientException("Error: " + Json["error"])
        services = []
        for service in Json:
            services.append(Service(service, self.__token__, ))
        return services

    def get_service(self, id):
        result = get(f"{base}/services/{id}", headers={"Authorization": self.__token__})
        Json = result.json()
        if not 200 <= result.status_code < 300:
            raise ClientException("Error: " + Json["error"])
        return Service(Json["service"], self.__token__, Json["access"])

    def create_service(self, settings):
        result = post(f"{base}/services/", settings, headers={"Authorization": self.__token__})
        Json = result.json()
        if not 200 <= result.status_code < 300:
            raise ClientException("Error: " + Json["error"])
        return Service(Json, self.__token__)

    """
        :returns -> dict
        :node -> str
        :type -> str
        
        Possible types:
        -> 'minecraft'
        -> 'mysql'
        -> 'terraria'
        -> 'factorio'
        -> 'csgo'
        -> 'rust'
        -> 'nodejs'
        -> 'deno'
        -> 'python'
        -> 'mongodb'
        -> 'nginx'
        -> 'nginx-php'
        -> 'vps'
        
        Possible errors:
            {"error":"Service type supported on this node."}
    """

    def get_versions(self, node: str = None, type: str = None):
        result = get(f"{base}/node/{node if node else 'fn10'}/{type if type else 'Minecraft'}/versions",
                     headers={"Authorization": self.__token__})
        Json = result.json()
        return Json

    def get_package(self, node: str = None, type: str = None):
        result = get(f"{base}/node/{node if node else 'fn10'}/{type if type else 'Minecraft'}/packages",
                     headers={"Authorization": self.__token__})
        Json = result.json()
        return Json

    def get_node_info(self):
        result = get(f"https://services_devapi.stacket.net/nodeInfo", headers={"Authorization": self.__token__})
        Json = result.json()
        return Json

    def get_nodes(self):
        return self.get_node_info()

    def get_domains(self):
        result = get(f"https://domains_devapi.stacket.net/", headers={"Authorization": self.__token__})
        Json = result.json()
        if not 200 <= result.status_code < 300:
            raise ClientException("Error: " + Json["error"])
        domains = []
        for domain in Json:
            domains.append(Domain(domain["_id"], self.__token__, domain))
        return domains

    def get_domain(self, id):
        result = get(f"https://domains_devapi.stacket.net/{id}", headers={"Authorization": self.__token__})
        Json = result.json()
        if not 200 <= result.status_code < 300:
            raise ClientException("Error: " + Json["error"])
        return Domain(Json["_id"], self.__token__, Json)
