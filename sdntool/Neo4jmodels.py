"""
Some mandatory elements that every model should have
- Every class should have name and id field
- Every class should have an staticmethod called from_neo4j_response() > which will be used to convert the neo4j response to the model
- Every class should have a class method called to_json() > which will be used to convert the model to json serializable object
"""

required_properties = {
    "network": [],
    "controller": ["ip", "cluster", "no_of_hosts", "no_of_devices_connected", "no_of_switches"],
    "switch": ["ip", "manufacturer", "hardware_id", "software_id", "serial", "driver", "protocol"],
    "router": [],
    "host": ["ip", "mac", "vlan", "no_of_cpu_cores", "ram", "hard_disk", "os"],
    "vni": [],
    "virtualmachine": ["id", "status", "name", "ip", "sec_group", "vCPU", "RAM", "size", "image_name"],
    "virtualnetwork": ["name", "vn_id", "Status", "MTU", "network_address", "attached_devices"],
    "virtualnetworkfunction": ["num_cpus", "mem_size", "disk_size", "image", "cps", "vnfID", "vimID"]
}


class Network:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.props = {}
        self.link_props = {}
        self.children = []

    @staticmethod
    def from_neo4j_response(response):
        return Network(response[0], response[1])

    def to_json(self, minified=True):
        if minified:
            return {
                "id": self.id,
                "name": self.name
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
                "type": "network",
                "props:": self.props,
                "link_props": self.link_props,
                "children": [child.to_json(minified=False) for child in self.children]
            }

    @staticmethod
    def from_raw_json(raw_json: dict):
        formatted_json = Network(-1, "")


class NetworkController:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.props = {}
        self.link_props = {}
        self.children = []
        self.connectedSwitchId = ""

    @staticmethod
    def from_neo4j_response(response):
        return NetworkController(response[0], response[1])

    def to_json(self, minified=True):
        if minified:
            return {
                "id": self.id,
                "name": self.name
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
                "type": "controller",
                "props:": self.props,
                "link_props": self.link_props,
                "children": [child.to_json(minified=False) for child in self.children]
            }

    @staticmethod
    def from_raw_json(raw_json: dict):
        created_object = NetworkController(-1, "")
        created_object.props = {
            "ip": raw_json["IP"],
            "cluster": raw_json["IPListincluster"] != "0",
            "controller_type": raw_json["controllerType"],
            "no_of_hosts": raw_json["noofhosts"],
            "no_of_devices_connected": raw_json["noofdevicescon"],
            "no_of_links": raw_json["nooflinks"]
        }

        created_object.connectedSwitchId = raw_json["connectedSwitchId"]

        created_object.link_props = {}
        return created_object


class NetworkSwitch:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.props = {}
        self.link_props = {}
        self.children = []

    @staticmethod
    def from_neo4j_response(response):
        return NetworkController(response[0], response[1])

    def to_json(self, minified=True):
        if minified:
            return {
                "id": self.id,
                "name": self.name
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
                "type": "switch",
                "props:": self.props,
                "link_props": self.link_props,
                "children": [child.to_json(minified=False) for child in self.children]
            }

    @staticmethod
    def from_raw_json(raw_json: dict):
        created_object = NetworkSwitch(-1, "")
        created_object.props = {
            "of_id": raw_json["id"],
            "manufacturer": raw_json["mfr"],
            "hardware_id": raw_json["hw"],
            "software_id": raw_json["sw"],
            "driver": raw_json["driver"],
            "protocol": raw_json["annotations"]["protocol"],
            "ip": raw_json["annotations"]["managementAddress"]
        }

        created_object.link_props = {}

        return created_object

    def add_host(self, host):
        self.children.append(host)


class NetworkHost:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.props = {}
        self.link_props = {}

    @staticmethod
    def from_neo4j_response(response):
        return NetworkController(response[0], response[1])

    def to_json(self, minified=True):
        if minified:
            return {
                "id": self.id,
                "name": self.name
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
                "type": "host",
                "props:": self.props,
                "link_props": self.link_props
            }

    @staticmethod
    def from_raw_json(raw_json: dict):
        created_object = NetworkHost(-1, "")
        created_object.props = {
            "mac": raw_json["mac"],
            "vlan": raw_json["vlan"],
            "no_of_cpu_cores": raw_json["noOfCpuCores"] if "noOfCpuCores" in raw_json else "",
            "ram": raw_json["ram"] if "ram" in raw_json else "",
            "hard_disk": raw_json["hardDisk"] if "hardDisk" in raw_json else "",
            "os": raw_json["os"] if "os" in raw_json else "",
            "ip": raw_json["ipAddresses"][-1]
        }

        created_object.link_props = {}

        return created_object


class NetworkRouter:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.props = {}
        self.link_props = {}
        self.children = []

    @staticmethod
    def from_neo4j_response(response):
        return NetworkRouter(response[0], response[1])

    def to_json(self, minified=True):
        if minified:
            return {
                "id": self.id,
                "name": self.name
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
                "type": "router",
                "props:": self.props,
                "link_props": self.link_props,
                "children": [child.to_json(minified=False) for child in self.children]
            }

    @staticmethod
    def from_raw_json(raw_json: dict):
        raise NotImplementedError("Not implemented yet")


class NetworkLink:
    def __init__(self, id, props):
        self.id = id
        self.props = props
        if "bandwidth" not in props:
            self.props["bandwidth"] = ""
        if "jitter" not in props:
            self.props["jitter"] = ""
        if "latency" not in props:
            self.props["latency"] = ""

    @staticmethod
    def from_neo4j_response(response):
        return NetworkLink(response[0], response[1])

    def to_json(self):
        return {
            "id": self.id,
            "type": "link",
            "props:": self.props,
        }


class Vnivm:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.props = {}
        self.link_props = {}

    @staticmethod
    def from_neo4j_response(response):
        return Vnivm(response[0], response[1])

    def to_json(self, minified=True):
        if minified:
            return {
                "id": self.id,
                "name": self.name
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
                "type": "virtualmachine",
                "props:": self.props,
                "link_props": self.link_props,

            }


    @staticmethod

    def from_raw_json(raw_json: dict):
        created_object = Vnivm(-1, "")
        created_object.props = {
            "id": raw_json["id"],
            "status": raw_json["status"],
            "name": raw_json["name"],
            "ip": raw_json["ip"],
            "sec_group": raw_json["sec_group"],
            "vCPU": raw_json["vCPU"],
            "RAM": raw_json["RAM"],
            "size": raw_json["size"],
            "image_name": raw_json["image_name"]
        }
        created_object.link_props = {}
        return created_object


class Vnivn:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.props = {}
        self.link_props = {}

    @staticmethod
    def from_neo4j_response(response):
        return Vnivn(response[0], response[1])

    def to_json(self, minified=True):
        if minified:
            return {
                "id": self.id,
                "name": self.name
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
                "type": "virtualnetwork",
                "props:": self.props,
                "link_props": self.link_props,

            }


    @staticmethod

    def from_raw_json(raw_json: dict):
        created_object = Vnivn(-1, "")
        created_object.props = {
            "name": raw_json["name"],
            "vn_id": raw_json["vn_id"],
            "Status": raw_json["Status"],
            "MTU": raw_json["MTU"],
            "network_address": raw_json["network_address"],
            "attached_devices": raw_json["attached_devices"]
        }
        created_object.link_props = {}
        return created_object

class Vnivnf:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.props = {}
        self.link_props = {}

    @staticmethod
    def from_neo4j_response(response):
        return Vnivnf(response[0], response[1])

    def to_json(self, minified=True):
        if minified:
            return {
                "id": self.id,
                "name": self.name
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
                "type": "virtualnetworkfunction",
                "props:": self.props,
                "link_props": self.link_props,

            }


    @staticmethod

    def from_raw_json(raw_json: dict):
        created_object = Vnivnf(-1, "")
        created_object.props = {
            "num_cpus": raw_json["num_cpus"],
            "mem_size": raw_json["mem_size"],
            "disk_size": raw_json["disk_size"],
            "image": raw_json["image"],
            "cps": raw_json["cps"],
            "vnfID": raw_json["vnfID"],
            "vimID": raw_json["vimID"]
        }

        created_object.link_props = {}
        return created_object

