# NOTE : All the functions mentioned below is required by Neo4JController class

# Preferred hierarchical format
"""
{
    "id": 0,
    "name": "Root",
    "label": "Network",
    "children": [
        {
            "id": 1,
            "name": "Switch 0",
            "label": "Switch",
            "children": [....]
        },
        ....
    ]
}
"""
import random
import string

from sdntool.Neo4jmodels import NetworkLink, NetworkController, NetworkSwitch, NetworkHost

# Preferred VisJS format
"""
"nodes": [
    {"id": 1, "label": "Node 1", "name": "I am node 1!"},
    {"id": 2, "label": "Node 2", "name": "I am node 2!"},
]

"edges": [
    {"from": 1, "to": 2},
]
"""


# This function will convert the raw neo4j data to hierarchical format
def format_data_hierarchical_json(parent_data, nodes):
    data = parent_data
    data["children"] = []
    parent_ids = [parent_data["id"]]

    for parent_id in parent_ids:
        for node in nodes:
            if len(node["children"]) == 0:
                continue
            for i in range(len(node["children"])):
                if node["children"][i]["id"] == parent_id:
                    data["children"].append(format_data_hierarchical_json(
                        {
                            "id": node["id"],
                            "name": node["name"],
                            "label": node["label"],
                        }, nodes
                    ))
    return data


# This function accepts parent nodes data and list of nodes and
# in return list of nodes and edges that are compatable with VisJS
def format_data_to_vis_js_format(parent_data, raw_nodes):
    nodes = list()
    edges = list()

    nodes.append({
        "id": parent_data["id"],
        "label": parent_data["name"],
        "group": parent_data["label"]
    })

    for node in raw_nodes:
        # Add node
        nodes.append({
            "id": node["id"],
            "label": node["name"],
            "group": node["label"],
        })
        # Add edge
        if len(node["children"]) > 0:
            for i in range(len(node["children"])):
                edges.append({
                    "from": node["id"],
                    "to": node["children"][i]["id"]
                })
    return list(nodes), list(edges)


# From ONOS data to network import
def import_network(no4j_controller, name_generator, controllers_data, switches_data, hosts_data, links_data):
    controllers = [NetworkController.from_raw_json(x) for x in controllers_data["controller"]]
    switches_map = {}
    links = links_data["links"]

    for switch in switches_data["devices"]:
        ob = NetworkSwitch.from_raw_json(switch)
        switches_map[switch["id"]] = ob

    for host in hosts_data["hosts"]:
        ob = NetworkHost.from_raw_json(host)
        for location in host["locations"]:
            switch = switches_map[location["elementId"]]
            switch.add_host(ob)

    #  1. Create network
    network = no4j_controller.create_network(name_generator.get_next_network_name())

    # 2.  Create all controllers using the network id
    for controller in controllers:
        created_controller = no4j_controller.create_controller(network.id, name_generator.get_next_controller_name(),
                                                               controller.props)
        controller.id = created_controller.id
        controller.name = created_controller.name

    # 3. Create all switches without network id
    for switch in switches_map:
        created_switch = no4j_controller.create_switch_without_parent_node(name_generator.get_next_switch_name(),
                                                                           switches_map[switch].props)
        switches_map[switch].id = created_switch.id
        switches_map[switch].name = created_switch.name

    # 4.  Connect all switches to all controllers
    for controller in controllers:
        no4j_controller.create_link(controller.id, switches_map[controller.connectedSwitchId].id)

    # 5. Connect switches by using links.json
    link_connections = {}
    for link in links:
        # no4j_controller.create_link(switches_map[link["src"]["device"]].id, switches_map[link["dst"]["device"]].id)
        srcid = switches_map[link["src"]["device"]].id
        dstid = switches_map[link["dst"]["device"]].id
        if srcid in link_connections:
            if dstid in link_connections[srcid]:
                continue

        if dstid in link_connections:
            if srcid in link_connections[dstid]:
                continue

        if srcid not in link_connections:
            link_connections[srcid] = []
        link_connections[srcid].append(dstid)

    for srcid in link_connections:
        for dstid in link_connections[srcid]:
            no4j_controller.create_link(srcid, dstid)

    # Try to fix direction of first node
    for controller in controllers:
        no4j_controller.fix_direction_between_switch(switches_map[controller.connectedSwitchId].id)

    # 6. Create all hosts using the switch id
    for switch in switches_map:
        for host in switches_map[switch].children:
            host.link_props = NetworkLink(-1, {
                "ip1": switches_map[switch].props["ip"],
                "ip2": host.props["ip"]
            }).props
            created_host = no4j_controller.create_host(switches_map[switch].id, name_generator.get_next_host_name(),
                                                       host.props, host.link_props)
            host.id = created_host.id
            host.name = created_host.name

    return network




def extract_required_properties_based_on_requirement(request_dict, required_properties: list):
    data = {}
    for prop in required_properties:
        data[prop] = request_dict.get(prop, "")
    return data


def generate_random_id_for_node():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=24))


def import_vni(neo4j_controller, name_generator, virtualmachine_data, virtualnetwork_data, virtualnetworkfunction_data, links_data):
    print(virtualnetwork_data["vns"])
    new_vni_name = name_generator.get_next_vni_name();
    new_vni = neo4j_controller.create_vni(new_vni_name)

    for vm in virtualmachine_data["vms"]:
        new_virtualmachine = name_generator.get_next_virtualmachine_name()
        cvm= neo4j_controller.create_virtualmachine(new_vni_name, new_virtualmachine, vm)
        # previous work must be done successfully.
        neo4j_controller.create_link(new_vni.id, cvm.id)

    for vn in virtualnetwork_data["vns"]:
        new_virtualnetwork = name_generator.get_next_virtualnetwork_name()
        cvn= neo4j_controller.create_virtualnetwork(new_vni_name, new_virtualnetwork, vn)
        neo4j_controller.create_link(new_vni.id, cvn.id)

    for vnf in virtualnetworkfunction_data["vnfs"]:
        new_virtualnetworkfunction = name_generator.get_next_virtualnetworkfunction_name()
        cvnf= neo4j_controller.create_virtualnetworkfunction(new_vni_name, new_virtualnetworkfunction , vnf)
        neo4j_controller.create_link(new_vni.id, cvnf.id )

    # unique id should be checked
    for lnk in links_data["links"]:
        neo4j_controller.create_link(lnk["source_id"], lnk["dest_id"],)

    return new_vni