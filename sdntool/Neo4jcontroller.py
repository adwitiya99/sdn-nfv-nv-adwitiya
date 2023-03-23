from neo4j import GraphDatabase
from sdntool.Neo4jmodels import Network, NetworkController, NetworkSwitch, NetworkHost, NetworkRouter, NetworkLink, \
    Vnivm, Vnivnf, Vnivn
from sdntool.utils import format_data_hierarchical_json, format_data_to_vis_js_format
import json


class Neo4JController:
    # some boilerplate functions
    session = None
    driver = None

    # Enums
    HierarchicalFormat = "HierarchicalFormat"
    VisJSFormat = "VisJSFormat"

    @staticmethod
    def setup(uri, username, password):
        Neo4JController.driver = GraphDatabase.driver(uri, auth=(username, password))
        Neo4JController.driver.verify_connectivity()

    @staticmethod
    def read_transaction(function_reference, *args, **kwargs):
        with Neo4JController.driver.session() as session:
            return session.execute_read(function_reference, *args, **kwargs)

    @staticmethod
    def write_transaction(function_reference, *args, **kwargs):
        with Neo4JController.driver.session() as session:
            return session.execute_write(function_reference, *args, **kwargs)

    @staticmethod
    def generate_query_for_properties(json_object_name: str, data: dict):
        parts = []
        if "name" in data:
            del data["name"]
        if len(data) > 0:
            parts.append("SET")
        for key, value in data.items():
            parts.append(f"{json_object_name}.{key} = ${key},")

        query = " ".join(parts)
        if query.endswith(","):
            query = query[:-1]
        return query

    # custom functions
    # Name  to id
    @staticmethod
    def get_element_id_from_name(element_name: str):
        def _get_element_id_from_name(tx, _element_name):
            result = tx.run("""
            MATCH (n)
            WHERE n.name=$element_name
            RETURN ID(n)
            """, element_name=_element_name)
            return result.single()

        record = Neo4JController.read_transaction(_get_element_id_from_name, element_name)
        try:
            return record[0]
        except:
            return None

    # delete node by id and delete all its relationships and nodes till leaf node
    @staticmethod
    def delete_node(id, delete_all_nodes_relationship=False):
        def _delete_all_nodes_relationships(tx, _id):
            tx.run("""
            MATCH (n)-[*0..]->(x)
            WHERE ID(n)=$id
            OPTIONAL MATCH (x)-[r]-() 
            DELETE r, x
            """, id=_id)

        def _delete_node(tx, _id):
            tx.run("""
            MATCH (n)
            WHERE ID(n)=$id
            DETACH DELETE n
            """, id=_id)

        if delete_all_nodes_relationship:
            Neo4JController.write_transaction(_delete_all_nodes_relationships, id)
        else:
            Neo4JController.write_transaction(_delete_node, id)

    # `LINK` relation related function
    @staticmethod
    def create_link(source_id, target_id, properties={}):
        def _create_link(tx, _source_id, _target_id):
            tx.run(f"""
            MATCH (a), (b)
            WHERE ID(a) = $source_id AND ID(b) = $target_id
            CREATE (a)-[r:LINK]->(b) 
            {Neo4JController.generate_query_for_properties('r', properties)}
            """, source_id=_source_id, target_id=_target_id, **properties)

        try:
            Neo4JController.write_transaction(_create_link, source_id, target_id)
            return True
        except Exception as e:
            print(e)
            return False

    # Network related functions
    @staticmethod
    def create_network(name, properties={}):
        def _create_network(tx, _name):
            result = tx.run(
                f"CREATE (n:Network {{name: $name}}) {Neo4JController.generate_query_for_properties('n', properties)} RETURN ID(n), n.name",
                name=_name, **properties)
            return result.single()

        return Network.from_neo4j_response(Neo4JController.write_transaction(_create_network, name))

    @staticmethod
    def get_networks():
        def _get_networks(tx):
            result = tx.run("MATCH (n:Network) RETURN ID(n), n.name")
            return result.values()

        return [Network.from_neo4j_response(response) for response in Neo4JController.read_transaction(_get_networks)]

    # Network Controller related functions
    @staticmethod
    def create_controller(parent_id, name, properties={}, link_properties={}):
        def _create_controller(tx, _parent_id, _name):
            result = tx.run(f"""
            MATCH (parent) WHERE ID(parent) = $parent_id
            CREATE(c:Controller{{name: $name}})
            {Neo4JController.generate_query_for_properties('c', properties)}
            MERGE (parent)-[r:LINK]->(c)
            {Neo4JController.generate_query_for_properties('r', link_properties)}
            RETURN ID(c), c.name
            """, parent_id=_parent_id, name=_name, **link_properties, **properties)
            return result.single()

        return NetworkController.from_neo4j_response(
            Neo4JController.write_transaction(_create_controller, parent_id, name))

    @staticmethod
    def get_controllers(parent_id):
        def _get_controllers(tx, _parent_id):
            result = tx.run("""
            MATCH (parent)-[:LINK]->(c:Controller)
            WHERE ID(parent) = $parent_id
            RETURN ID(c), c.name
            """, parent_id=_parent_id)
            return result.values()

        return [NetworkController.from_neo4j_response(response) for response in
                Neo4JController.read_transaction(_get_controllers, parent_id)]

    # Switch related functions
    @staticmethod
    def create_switch(parent_id, name, properties={}, link_properties={}):
        def _create_switch(tx, _parent_id, _name):
            result = tx.run(f"""
            MATCH (parent) WHERE ID(parent) = $parent_id
            CREATE(s:Switch{{name: $name}})
            {Neo4JController.generate_query_for_properties('s', properties)} 
            MERGE (parent)-[r:LINK]->(s)
            {Neo4JController.generate_query_for_properties('r', link_properties)}
            RETURN ID(s), s.name
            """, parent_id=_parent_id, name=_name, **link_properties, **properties)
            return result.single()

        return NetworkSwitch.from_neo4j_response(Neo4JController.write_transaction(_create_switch, parent_id, name))

    @staticmethod
    def create_switch_without_parent_node(name, properties={}):
        def _create_switch(tx, _name):
            result = tx.run(f"""
            CREATE(s:Switch{{name: $name}})
            {Neo4JController.generate_query_for_properties('s', properties)} 
            RETURN ID(s), s.name
            """, name=_name, **properties)
            return result.single()

        return NetworkSwitch.from_neo4j_response(Neo4JController.write_transaction(_create_switch, name))

    @staticmethod
    def get_switches(parent_id):
        def _get_switches(tx, _parent_id):
            result = tx.run("""
            MATCH (parent)-[:LINK]->(s:Switch)
            WHERE ID(parent) = $parent_id
            RETURN ID(s), s.name
            """, parent_id=_parent_id)
            return result.values()

        return [NetworkSwitch.from_neo4j_response(response) for response in
                Neo4JController.read_transaction(_get_switches, parent_id)]

    # Router related functions
    @staticmethod
    def create_router(parent_id, name, properties={}, link_properties={}):
        def _create_router(tx, _parent_id, _name):
            result = tx.run(f"""
            MATCH (parent) WHERE ID(parent) = $parent_id
            CREATE(r:Router{{name: $name}})
            {Neo4JController.generate_query_for_properties('r', properties)}
            MERGE (parent)-[l:LINK]->(r)
            {Neo4JController.generate_query_for_properties('l', link_properties)}
            RETURN ID(r), r.name
            """, parent_id=_parent_id, name=_name, **link_properties, **properties)
            return result.single()

        return NetworkRouter.from_neo4j_response(Neo4JController.write_transaction(_create_router, parent_id, name))

    @staticmethod
    def get_routers(parent_id):
        def _get_routers(tx, _parent_id):
            result = tx.run("""
            MATCH (parent)-[:LINK]->(h:Host)
            WHERE ID(parent) = $parent_id
            RETURN ID(h), h.name
            """, parent_id=_parent_id)
            return result.values()

        return [NetworkRouter.from_neo4j_response(response) for response in
                Neo4JController.read_transaction(_get_routers, parent_id)]

    # Network Host related functions
    @staticmethod
    def create_host(parent_id, name, properties={}, link_properties={}):
        def _create_host(tx, _parent_id, _name):
            result = tx.run(f"""
            MATCH (parent) WHERE ID(parent) = $parent_id
            CREATE(h:Host{{name: $name}})
            {Neo4JController.generate_query_for_properties('h', properties)} 
            MERGE (parent)-[l:LINK]->(h)
            {Neo4JController.generate_query_for_properties('l', link_properties)}
            RETURN ID(h), h.name
            """, parent_id=_parent_id, name=_name, **link_properties, **properties)
            return result.single()

        return NetworkHost.from_neo4j_response(Neo4JController.write_transaction(_create_host, parent_id, name))

    @staticmethod
    def get_hosts(parent_id):
        def _get_hosts(tx, _parent_id):
            result = tx.run("""
            MATCH (parent)-[:LINK]->(h:Host)
            WHERE ID(parent) = $parent_id
            RETURN ID(h), h.name
            """, parent_id=_parent_id)
            return result.values()

        return [NetworkHost.from_neo4j_response(response) for response in
                Neo4JController.read_transaction(_get_hosts, parent_id)]

    """
    This function will try to invert path between two switches, if the direction of switch from down to up is not possible
    """

    @staticmethod
    def fix_direction_between_switch(node_id):
        def _fix_direction_between_switch(tx, _node_id):
            result = tx.run("""
            MATCH (n:Switch)<-[rel:LINK]-(x:Switch)
            WHERE ID(n)=$node_id
            CALL apoc.refactor.invert(rel)
            yield input, output
            RETURN input, output
            """, node_id=_node_id)
            return result.values()

        try:
            Neo4JController.write_transaction(_fix_direction_between_switch, node_id)
        except Exception as e:
            print(e)

    @staticmethod
    def get_properties(node_id):
        def _get_properties(tx, _node_id):
            result = tx.run("""
            MATCH (n) WHERE ID(n) = $node_id
            RETURN properties(n)
            """, node_id=_node_id)
            return result.single()

        try:
            return list(Neo4JController.read_transaction(_get_properties, node_id))[0]
        except Exception as e:
            return {}

    @staticmethod
    def get_all_controllers_of_network(network_id):
        def _get_all_controllers_of_network(tx, _network_id):
            result = tx.run("""
            MATCH (n:Network)-[:LINK*]-(c:Controller)
            WHERE ID(n) = $network_id
            WITH collect(c) as controllers
            UNWIND controllers as c
            RETURN DISTINCT ID(c), c.name
            """, network_id=_network_id)
            return result.values()

        return [NetworkController.from_neo4j_response(response) for response in
                Neo4JController.read_transaction(_get_all_controllers_of_network, network_id)]

    @staticmethod
    def get_all_switches_of_network(network_id):
        def _get_all_switches_of_network(tx, _network_id):
            result = tx.run("""
            MATCH (n:Network)-[:LINK*]-(s:Switch)
            WHERE ID(n) = $network_id
            WITH collect(s) as switches
            UNWIND switches as s
            RETURN DISTINCT ID(s), s.name
            """, network_id=_network_id)
            return result.values()

        return [NetworkSwitch.from_neo4j_response(response) for response in
                Neo4JController.read_transaction(_get_all_switches_of_network, network_id)]

    @staticmethod
    def get_all_routers_of_network(network_id):
        def _get_all_routers_of_network(tx, _network_id):
            result = tx.run("""
            MATCH (n:Network)-[:LINK*]-(r:Router)
            WHERE ID(n) = $network_id
            WITH collect(r) as routers
            UNWIND routers as r
            RETURN DISTINCT ID(r), r.name
            """, network_id=_network_id)
            return result.values()

        return [NetworkRouter.from_neo4j_response(response) for response in
                Neo4JController.read_transaction(_get_all_routers_of_network, network_id)]

    @staticmethod
    def get_all_hosts_of_network(network_id):
        def _get_all_hosts_of_network(tx, _network_id):
            result = tx.run("""
            MATCH (n:Network)-[:LINK*]-(h:Host)
            WHERE ID(n) = $network_id
            WITH collect(h) as hosts
            UNWIND hosts as h
            RETURN DISTINCT ID(h), h.name
            """, network_id=_network_id)
            return result.values()

        return [NetworkHost.from_neo4j_response(response) for response in
                Neo4JController.read_transaction(_get_all_hosts_of_network, network_id)]

    @staticmethod
    def get_link(link_id):
        def _get_link(tx, _link_id):
            result = tx.run("""
            MATCH ()-[l:LINK]->()
            WHERE ID(l)=link_id
            RETURN ID(l), properties(l)
            """, link_id=_link_id)
            return result.single()

        return NetworkLink.from_neo4j_response(Neo4JController.read_transaction(_get_link, link_id))

    # Function to fetch whole network tree
    @staticmethod
    def get_graph(parent_id, format="HierarchicalFormat"):
        # NOTE : This function query depends on `apoc` plugin for neo4j, So enable it before using this function
        def _get_network_tree(tx, _parent_id):
            result = tx.run("""
            MATCH (parent) WHERE ID(parent)=$parent_id
            CALL apoc.path.subgraphAll(parent, {labelFilter:"*", relationshipFilter:"LINK"}) YIELD nodes, relationships
            WITH parent, nodes, relationships,
                ID(parent) as id, 
                labels(parent)[0] as label, 
                parent.name as name, 
                [
                    x IN nodes WHERE NOT x IN [parent] |
                    {
                        id: ID(x),
                        label: labels(x)[0],
                        name:x.name,
                        children: [
                            y IN nodes WHERE (x)<-[:LINK]-(y) |
                            {id: ID(y), label: labels(y)[0], name: y.name}
                        ]
                    }
                ] as children
            RETURN {
                id: id,
                label: label,
                name: name,
                children: children
            }
            """, parent_id=_parent_id)
            return result.values()

        response = Neo4JController.read_transaction(_get_network_tree, parent_id)
        if len(response) == 0 or len(response[0]) == 0:
            return {} if format == Neo4JController.HierarchicalFormat else (
                {}, {} if format == Neo4JController.VisJSFormat else None)
        else:
            response = response[0][0]
            if format == Neo4JController.HierarchicalFormat:
                return format_data_hierarchical_json({
                    "id": response["id"],
                    "name": response["name"],
                    "label": response["label"],

                }, response["children"])
            elif format == Neo4JController.VisJSFormat:
                return format_data_to_vis_js_format({
                    "id": response["id"],
                    "name": response["name"],
                    "label": response["label"],
                }, response["children"])

            else:
                return None

    # Functions required by policy checking and evidence generation
    # We will provide network_name inspite of id as network_name is unqiuue
    @staticmethod
    def get_host_name_by_mac(network_name, mac):
        def _get_host_name_by_mac(tx, _network_name, _mac):
            result = tx.run("""
            MATCH (n:Network)-[:LINK*]-(h:Host)
            WHERE n.name = $network_name AND h.mac = $mac
            RETURN h.name
            """, network_name=_network_name, mac=_mac)
            return result.single()

        res = Neo4JController.read_transaction(_get_host_name_by_mac, network_name, mac)
        return res[0] if res is not None else None

    @staticmethod
    def get_property_of_node(node_id, property_name):
        def _get_property_of_node(tx, _node_id, _property_name):
            result = tx.run("""
            MATCH (n)
            WHERE ID(n) = $node_id
            RETURN n.$property_name
            """, node_id=_node_id, property_name=_property_name)
            return result.single()

        res = Neo4JController.read_transaction(_get_property_of_node, node_id, property_name)
        return res[0] if res is not None else None

    # if __name__ == "__main__":
    # Neo4JController.setup("bolt://localhost:7687", "neo4j", "cdcju")
    # z = Neo4JController.create_network("Network 2")
    # print(z.id)
    # print([network.to_json() for network in Neo4JController.get_networks()])
    # for i in range(5):
    #     y = Neo4JController.create_switch(z.id, "Switch {}".format(i))
    #     for j in range(5):
    #         m = Neo4JController.create_controller(y.id, "Controller {}".format(j))
    #         for k in range(5):
    #             n = Neo4JController.create_switch(m.id, "Switch {}".format(k))
    #             for l in range(5):
    #                 Neo4JController.create_host(n.id, "Host {}".format(l))
    # print([controller.to_json() for controller in Neo4JController.get_controllers(13)])
    # Neo4JController.delete_node(156, delete_all_nodes_relationship=True)
    # print(json.dumps(Neo4JController.get_graph(131)))
    @staticmethod
    def create_vni(name, properties={}):
        def _create_vni(tx, _name):
            result = tx.run(
                f"CREATE (n:VNI {{name: $name}}) {Neo4JController.generate_query_for_properties('n', properties)} RETURN ID(n), n.name",
                name=_name, **properties)
            return result.single()

        return Network.from_neo4j_response(Neo4JController.write_transaction(_create_vni, name))

    @staticmethod
    def get_vni():
        def _get_vni(tx):
            result = tx.run("MATCH (n:VNI) RETURN ID(n), n.name")
            return result.values()

        return [Network.from_neo4j_response(response) for response in Neo4JController.read_transaction(_get_vni)]

    # Virtual Machine related functions
    @staticmethod
    def create_virtualmachine(parent_name, name, properties={}):
        def _create_virtualmachine(tx, _name, _parent_name):
            result = tx.run(f"""
            CREATE(h:{parent_name}:Virtualmachine{{name: $name}})
            {Neo4JController.generate_query_for_properties('h', properties)} 
            RETURN ID(h), h.name
            """, parent_name=_parent_name, name=_name, **properties)
            return result.single()

        return Vnivm.from_neo4j_response(Neo4JController.write_transaction(_create_virtualmachine, name, parent_name))

    @staticmethod
    def get_virtualmachine(parent_id):
        def _get_virtualmachine(tx, _parent_id):
            result = tx.run("""
            MATCH (parent)-[:LINK]->(h:Virtualmachine)
            WHERE ID(parent) = $parent_id
            RETURN ID(h), h.name
            """, parent_id=_parent_id)
            return result.values()

        return [Vnivm.from_neo4j_response(response) for response in
                Neo4JController.read_transaction(_get_virtualmachine, parent_id)]

    # Virtual Network related functions
    @staticmethod
    def create_virtualnetwork(parent_name, name, properties={}):
        def _create_virtualnetwork(tx, _name, _parent_name):
            result = tx.run(f"""
                CREATE(h:{parent_name}:Virtualnetwork{{name: $name}})
                {Neo4JController.generate_query_for_properties('h', properties)} 
                RETURN ID(h), h.name
                """, parent_name=_parent_name, name=_name, **properties)
            return result.single()

        return Vnivn.from_neo4j_response(Neo4JController.write_transaction(_create_virtualnetwork, name, parent_name))

    @staticmethod
    def get_virtualnetwork(parent_id):
        def _get_virtualnetwork(tx, _parent_id):
            result = tx.run("""
                MATCH (parent)-[:LINK]->(h:Virtualnetwork)
                WHERE ID(parent) = $parent_id
                RETURN ID(h), h.name
                """, parent_id=_parent_id)
            return result.values()

        return [Vnivn.from_neo4j_response(response) for response in
                Neo4JController.read_transaction(_get_virtualnetwork, parent_id)]

    # Virtual Network Function related functions
    @staticmethod
    def create_virtualnetworkfunction(parent_name, name, properties={}, link_properties={}):
        def _create_virtualnetworkfunction(tx, _name, _parent_name):
            result = tx.run(f"""
            CREATE(h:{parent_name}:Virtualnetworkfunction{{name: $name}})
            {Neo4JController.generate_query_for_properties('h', properties)} 
            
            RETURN ID(h), h.name
            """, parent_name=_parent_name, name=_name, **properties)
            return result.single()

        return Vnivnf.from_neo4j_response(
            Neo4JController.write_transaction(_create_virtualnetworkfunction, name, parent_name))

    @staticmethod
    def get_virtualnetworkfunction(parent_id):
        def _get_virtualnetworkfunction(tx, _parent_id):
            result = tx.run("""
            MATCH (parent)-[:LINK]->(h:Virtualnetworkfunction)
            WHERE ID(parent) = $parent_id
            RETURN ID(h), h.name
            """, parent_id=_parent_id)
            return result.values()

        return [Vnivnf.from_neo4j_response(response) for response in
                Neo4JController.read_transaction(_get_virtualnetworkfunction, parent_id)]

    """
    This function will try to invert path between two switches, if the direction of switch from down to up is not possible
    """

    @staticmethod
    def get_graph_vni(parent_name, format="HierarchicalFormat"):
        # NOTE : This function query depends on `apoc` plugin for neo4j, So enable it before using this function
        def _get_network_tree(tx, _parent_name):
            result = tx.run(f"""
                    MATCH (n:{parent_name})<-[:LINK]-(parent)
                    RETURN n, parent
                   
                """, parent_name=_parent_name).data()
            nodes = []
            return {"nodes": result}

        response = Neo4JController.read_transaction(_get_network_tree, parent_name)
        return json.dumps(response)

    @staticmethod
    def createvnilink_vm_to_vn(vni, vm, vn, properties={}):
        def _createvnilink_vm_to_vn(tx, _vni, _vm, _vn):
            result = tx.run(f"""
            
            MATCH (a:{vni}), (b:{vni})
WHERE a.id = $vm AND b.vn_id = $vn
MERGE (a)-[r:LINK]->(b)
            
             {Neo4JController.generate_query_for_properties('r', properties)}
                            """, vni=_vni, vm=_vm, vn=_vn, **properties).data()
            return {"nodes": result}

        try:
            response = Neo4JController.write_transaction(_createvnilink_vm_to_vn, vni, vm, vn)
            return True
        except Exception as e:
            print(e)
            return False


    @staticmethod
    def createvnilink_vn_to_vnf(vni, vn, vnf, properties={}):


        def _createvnilink_vn_to_vnf(tx, _vni, _vn, _vnf):
            result = tx.run(f"""
    
                MATCH (a:{vni}), (b:{vni})
                WHERE a.vn_id = $vn AND b.vnfID = $vnf
                MERGE (a)-[r:LINK]->(b)
    
                 {Neo4JController.generate_query_for_properties('r', properties)}
                                """, vni=_vni, vn=_vn, vnf=_vnf, **properties).data()
            return {"nodes": result}

        try:
            for x in vnf:
                response = Neo4JController.write_transaction(_createvnilink_vn_to_vnf, vni, vn, x)
            return True
        except Exception as e:
            print(e)
            return False


