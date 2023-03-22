"""
Assumptions that has been taken
- Every function will
    - take its input and arguments
    - if necessary also some arguments from the environment
    - return check status + message
    - Also return list of checks and reason why it succeed or failed

In the code, many variable has been mentioned as h1 or h2
h1 represents First Host
h2 represents Second Host
....
They are not related to any host name in database
"""
import json

from django.db.models import Q

from logmanager.models import NetworkLog
from policymanagement.utils import *
from sdntool.Neo4jcontroller import Neo4JController
from policymanagement.models import *
import re

"""
Network Segregation Property [No Communication]
> Goal - Host H1 and H2 should not communicate with each other
> Requirement - H1 mac and H2 mac and flow_rule.json
> Check -
    - Check if the flow rule has the H1 mac as src and H2 mac as dst
"""


def network_segregation_property_for_no_communication(first_host_name: str, second_host_name: str, network_name: str, from_log_timestamp: int):
    checks_data = {
        "EVIDENCE_FILE_FOUND_FOR_FIRST_HOST_TO_SECOND_HOST": False,
        "EVIDENCE_FILE_FOUND_FOR_SECOND_HOST_TO_FIRST_HOST": False,
        "RESOLVED_MAC_ADDRESS_FOR_FIRST_HOST": False,
        "RESOLVED_MAC_ADDRESS_FOR_SECOND_HOST": False,
        "RESOLVED_IP_ADDRESS_FOR_FIRST_HOST": False,
        "RESOLVED_IP_ADDRESS_FOR_SECOND_HOST": False,
        "NO_CONNECTION_EXISTS_FROM_FIRST_HOST_TO_SECOND_HOST": False,
        "NO_CONNECTION_EXISTS_FROM_SECOND_HOST_TO_FIRST_HOST": False,
        "NO_TRACES_OF_ICMP_PING_REQUEST_FROM_FIRST_HOST_TO_SECOND_HOST": False,
        "NO_TRACES_OF_ICMP_PING_REQUEST_FROM_SECOND_HOST_TO_FIRST_HOST": False
    }

    compliance_pass = False
    # Required Treatment Configuration
    required_treatment_config = {}

    try:
        # Fetch evidence file
        first_host_record = EvidenceData.objects.filter(selected_host_name=first_host_name).filter(
            evidence_type="flow-rule").first()
        first_host_evidence_data = json.loads(first_host_record.evidence_data.content)
        checks_data["EVIDENCE_FILE_FOUND_FOR_FIRST_HOST_TO_SECOND_HOST"] = True
        second_host_record = EvidenceData.objects.filter(selected_host_name=second_host_name).filter(
            evidence_type="flow-rule").first()
        second_host_evidence_data = json.loads(second_host_record.evidence_data.content)
        checks_data["EVIDENCE_FILE_FOUND_FOR_SECOND_HOST_TO_FIRST_HOST"] = True

        if checks_data["EVIDENCE_FILE_FOUND_FOR_FIRST_HOST_TO_SECOND_HOST"] and checks_data[
            "EVIDENCE_FILE_FOUND_FOR_SECOND_HOST_TO_FIRST_HOST"]:
            # Fetch mac address
            first_host_properties = Neo4JController.get_properties(
                Neo4JController.get_element_id_from_name(first_host_name))
            first_host_mac = first_host_properties["mac"]
            checks_data["RESOLVED_MAC_ADDRESS_FOR_FIRST_HOST"] = True
            first_host_ip = first_host_properties["ip"]
            checks_data["RESOLVED_IP_ADDRESS_FOR_FIRST_HOST"] = True
            second_host_properties = Neo4JController.get_properties(
                Neo4JController.get_element_id_from_name(second_host_name))
            second_host_mac = second_host_properties["mac"]
            checks_data["RESOLVED_MAC_ADDRESS_FOR_SECOND_HOST"] = True
            second_host_ip = second_host_properties["ip"]
            checks_data["RESOLVED_IP_ADDRESS_FOR_SECOND_HOST"] = True

            # Check if there is any flow rule for h1-h2
            criteria = first_host_evidence_data["selector"]["criteria"]
            if (criteria[1]["type"] == "ETH_SRC" and criteria[1]["mac"] == second_host_mac and criteria[2][
                "type"] == "ETH_DST" and criteria[2]["mac"] == first_host_mac) or (
                    criteria[2]["type"] == "ETH_SRC" and criteria[2]["mac"] == second_host_mac and criteria[1][
                "type"] == "ETH_DST" and criteria[1]["mac"] == first_host_mac):
                if compare_json(first_host_evidence_data["treatment"], required_treatment_config):
                    checks_data["NO_CONNECTION_EXISTS_FROM_FIRST_HOST_TO_SECOND_HOST"] = True

            # Check if there is any flow rule for h2-h1
            criteria = second_host_evidence_data["selector"]["criteria"]
            if (criteria[1]["type"] == "ETH_SRC" and criteria[1]["mac"] == first_host_mac and criteria[2][
                "type"] == "ETH_DST" and criteria[2]["mac"] == second_host_mac) or (
                    criteria[2]["type"] == "ETH_SRC" and criteria[2]["mac"] == first_host_mac and criteria[1][
                "type"] == "ETH_DST" and criteria[1]["mac"] == second_host_mac):
                if compare_json(second_host_evidence_data["treatment"], required_treatment_config):
                    checks_data["NO_CONNECTION_EXISTS_FROM_SECOND_HOST_TO_FIRST_HOST"] = True

            # Check of there is any ping request in log in h1 from h2's ip
            first_records_count = NetworkLog.objects(message__contains=second_host_ip, config_type="ping.log",
                                                     network_name=network_name, element_name=first_host_name,
                                                     uploaded_on__gte=from_log_timestamp).count()
            checks_data["NO_TRACES_OF_ICMP_PING_REQUEST_FROM_SECOND_HOST_TO_FIRST_HOST"] = first_records_count == 0

            # Check of there is any ping request in log in h1 from h2's ip
            second_records_count = NetworkLog.objects(message__contains=first_host_ip, config_type="ping.log",
                                                      network_name=network_name, element_name=second_host_name,
                                                      uploaded_on__gte=from_log_timestamp).count()
            checks_data["NO_TRACES_OF_ICMP_PING_REQUEST_FROM_FIRST_HOST_TO_SECOND_HOST"] = second_records_count == 0

    except Exception as e:
        print(e)

    # Compliance check based on previous checks
    compliance_pass = True
    for key in checks_data.keys():
        if not checks_data[key]:
            compliance_pass = False
            break

    return {
        "checks": checks_data,
        "pass": compliance_pass
    }


"""
Network Segregation Property [Communication]
> Goal - Host H1 and H2 should communicate with each other
> Requirement - H1 mac and H2 mac and flow_rule.json
> Check -
    - Check if the flow rule has the H1 mac as src and H2 mac as dst and treatment set
"""


def network_segregation_property_for_communication(first_host_name: str, second_host_name: str, network_name: str,
                                                   from_log_timestamp: int):
    checks_data = {
        "EVIDENCE_FILE_FOUND_FOR_FIRST_HOST_TO_SECOND_HOST": False,
        "EVIDENCE_FILE_FOUND_FOR_SECOND_HOST_TO_FIRST_HOST": False,
        "RESOLVED_MAC_ADDRESS_FOR_FIRST_HOST": False,
        "RESOLVED_MAC_ADDRESS_FOR_SECOND_HOST": False,
        "RESOLVED_IP_ADDRESS_FOR_FIRST_HOST": False,
        "RESOLVED_IP_ADDRESS_FOR_SECOND_HOST": False,
        "CONNECTION_EXISTS_FROM_FIRST_HOST_TO_SECOND_HOST": False,
        "CONNECTION_EXISTS_FROM_SECOND_HOST_TO_FIRST_HOST": False,
        "FOUND_TRACES_OF_ICMP_PING_REQUEST_FROM_FIRST_HOST_TO_SECOND_HOST": False,
        "FOUND_TRACES_OF_ICMP_PING_REQUEST_FROM_SECOND_HOST_TO_FIRST_HOST": False
    }

    compliance_pass = False
    # Required Treatment Configuration
    required_treatment_config = {
        "instructions": [
            {
                "type": "OUTPUT",
                "port": "CONTROLLER"
            }
        ]
    }

    try:
        # Fetch evidence file
        first_host_record = EvidenceData.objects.filter(selected_host_name=first_host_name).filter(
            evidence_type="flow-rule").first()
        first_host_evidence_data = json.loads(first_host_record.evidence_data.content)
        checks_data["EVIDENCE_FILE_FOUND_FOR_FIRST_HOST_TO_SECOND_HOST"] = True
        second_host_record = EvidenceData.objects.filter(selected_host_name=second_host_name).filter(
            evidence_type="flow-rule").first()
        second_host_evidence_data = json.loads(second_host_record.evidence_data.content)
        checks_data["EVIDENCE_FILE_FOUND_FOR_SECOND_HOST_TO_FIRST_HOST"] = True

        if checks_data["EVIDENCE_FILE_FOUND_FOR_FIRST_HOST_TO_SECOND_HOST"] and checks_data[
            "EVIDENCE_FILE_FOUND_FOR_SECOND_HOST_TO_FIRST_HOST"]:
            # Fetch mac address
            first_host_properties = Neo4JController.get_properties(
                Neo4JController.get_element_id_from_name(first_host_name))
            first_host_mac = first_host_properties["mac"]
            checks_data["RESOLVED_MAC_ADDRESS_FOR_FIRST_HOST"] = True
            first_host_ip = first_host_properties["ip"]
            checks_data["RESOLVED_IP_ADDRESS_FOR_FIRST_HOST"] = True
            second_host_properties = Neo4JController.get_properties(
                Neo4JController.get_element_id_from_name(second_host_name))
            second_host_mac = second_host_properties["mac"]
            checks_data["RESOLVED_MAC_ADDRESS_FOR_SECOND_HOST"] = True
            second_host_ip = second_host_properties["ip"]
            checks_data["RESOLVED_IP_ADDRESS_FOR_SECOND_HOST"] = True

            # Check if there is any flow rule for h1-h2
            criteria = first_host_evidence_data["selector"]["criteria"]
            if (criteria[1]["type"] == "ETH_SRC" and criteria[1]["mac"] == second_host_mac and criteria[2][
                "type"] == "ETH_DST" and criteria[2]["mac"] == first_host_mac) or (
                    criteria[2]["type"] == "ETH_SRC" and criteria[2]["mac"] == second_host_mac and criteria[1][
                "type"] == "ETH_DST" and criteria[1]["mac"] == first_host_mac):
                if compare_json(first_host_evidence_data["treatment"], required_treatment_config):
                    checks_data["CONNECTION_EXISTS_FROM_FIRST_HOST_TO_SECOND_HOST"] = True

            # Check if there is any flow rule for h2-h1
            criteria = second_host_evidence_data["selector"]["criteria"]
            if (criteria[1]["type"] == "ETH_SRC" and criteria[1]["mac"] == first_host_mac and criteria[2][
                "type"] == "ETH_DST" and criteria[2]["mac"] == second_host_mac) or (
                    criteria[2]["type"] == "ETH_SRC" and criteria[2]["mac"] == first_host_mac and criteria[1][
                "type"] == "ETH_DST" and criteria[1]["mac"] == second_host_mac):
                if compare_json(second_host_evidence_data["treatment"], required_treatment_config):
                    checks_data["CONNECTION_EXISTS_FROM_SECOND_HOST_TO_FIRST_HOST"] = True

            # Check of there is any ping request in log in h1 from h2's ip
            first_records_count = NetworkLog.objects(message__contains=second_host_ip, config_type="ping.log",
                                                     network_name=network_name, element_name=first_host_name,
                                                     uploaded_on__gte=from_log_timestamp).count()
            checks_data["FOUND_TRACES_OF_ICMP_PING_REQUEST_FROM_SECOND_HOST_TO_FIRST_HOST"] = first_records_count > 0

            # Check of there is any ping request in log in h1 from h2's ip
            second_records_count = NetworkLog.objects(message__contains=first_host_ip, config_type="ping.log",
                                                      network_name=network_name, element_name=second_host_name,
                                                      uploaded_on__gte=from_log_timestamp).count()
            checks_data["FOUND_TRACES_OF_ICMP_PING_REQUEST_FROM_FIRST_HOST_TO_SECOND_HOST"] = second_records_count > 0

    except Exception as e:
        print(e)

    # Compliance check based on previous checks
    compliance_pass = True
    for key in checks_data.keys():
        if not checks_data[key]:
            compliance_pass = False
            break

    return {
        "checks": checks_data,
        "pass": compliance_pass
    }


"""
Mutual Authentication Property 
> Goal - Controller and switch should be able to authenticate each other.
> Requirement - onos-service file 
"""


def mutual_authentication_property(network_name, controller_name, from_log_timestamp: int):
    checks_data = {
        "ONOS_SERVICE_FILE_FOUND": False,
    }

    # Fetch onos-service file
    filtered_records = EvidenceData.objects.filter(
        network_name=network_name,
        evidence_type='onos-service',
        selected_controller_name=controller_name
    )
    if len(filtered_records) == 0:
        checks_data["ONOS_SERVICE_FILE_FOUND"] = False
    else:
        checks_data["ONOS_SERVICE_FILE_FOUND"] = True
        onos_service_file = filtered_records[0].evidence_data.content
        # Check
        found_config_lines = re.findall('export\s+JAVA_OPTS=\"\s*\${JAVA_OPTS:-.*DenableOFTLS=true',
                                        onos_service_file)
        if len(found_config_lines) > 0:
            checks_data["TLS_ENABLED"] = True
            checks_data["CONFIG_LINE_UNCOMMENTED"] = True
            # Now check whether the line is commented
            if len(re.findall('#\s*export\s+JAVA_OPTS=\"\s*\${JAVA_OPTS:-.*DenableOFTLS=true',
                              onos_service_file)):
                checks_data["TLS_ENABLED"] = False
                checks_data["CONFIG_LINE_UNCOMMENTED"] = False

        # Check for keystore and trust store key and password
        if len(re.findall(
                'export\s+JAVA_OPTS\s*=\s*\"\s*\${\s*JAVA_OPTS:-.*DenableOFTLS=true\s*-Djavax.net.ssl.keyStore\s*=.*/onos.jks\s*-Djavax.net.ssl.keyStorePassword\s*=.*\s*-Djavax.net.ssl.trustStore\s*=.*\s*-Djavax.net.ssl.trustStorePassword\s*=.*}\"',
                onos_service_file)) > 0:
            checks_data["AUTH_CONFIG_FOUND"] = True
        else:
            checks_data["AUTH_CONFIG_FOUND"] = False

        # Fetch all controllers
        controllers = Neo4JController.get_controllers(Neo4JController.get_element_id_from_name(network_name))
        for controller in controllers:
            checks_data["OPEN_FLOW_SSL_ENABLED_FOR_CONTROLLER_" + controller.name] = False
            checks_data["TRACE_OF_ALL_SWITCHES_CONNECTION_FOUND_FOR_CONTROLLER_" + controller.name] = False

        # Checks
        for controller in controllers:
            count = NetworkLog.objects(message__contains="OpenFlow SSL enabled", config_type="karaf_ssl.log",
                                       network_name=network_name, element_name=controller.name,
                                       uploaded_on__gte=from_log_timestamp).count()
            if count > 0:
                checks_data["OPEN_FLOW_SSL_ENABLED_FOR_CONTROLLER_" + controller.name] = True

        # Fetch all switches
        switches = Neo4JController.get_all_switches_of_network(Neo4JController.get_element_id_from_name(network_name))
        for index, switch in enumerate(switches):
            switches[index].props = Neo4JController.get_properties(switch.id)

        # Check
        for controller in controllers:
            found_all = True
            for switch in switches:
                try:
                    count = NetworkLog.objects(message__contains=switch.props["of_id"], config_type="devices.log",
                                               network_name=network_name, element_name=controller.name,
                                               uploaded_on__gte=from_log_timestamp).count()
                    if count == 0:
                        found_all = False
                except:
                    pass
            checks_data["TRACE_OF_ALL_SWITCHES_CONNECTION_FOUND_FOR_CONTROLLER_" + controller.name] = found_all

    compliance_pass = True
    for key in checks_data:
        if not checks_data[key]:
            compliance_pass = False
            break
    return {
        "checks": checks_data,
        "pass": compliance_pass
    }


"""
Data Protection Property
> Goal - 
    - The communication between the switch and the controller should be encrypted.
    - The communication between the switch and the controller should be over TLS.
    - Isolation among different applications must be ensured.
> Requirement - onos-service file and Startup.properties file
"""

# TODO: no Startup.properties file currently available. So verification of that pending
# def data_protection_property(onos_service_file):
#     checks_data = {
#         "TLS_ENABLED": False,
#         "AUTH_CONFIG_FOUND": False,
#         "CONFIG_LINE_NOT_COMMENTED": False
#     }
#
#     complience_pass = False
#
#     # Check
#     found_config_lines = re.findall('export\s+JAVA_OPTS=\"\s*\${JAVA_OPTS:-.*Dio\.atomix\.enableNettyTLS=true',
#                                     onos_service_file)
#     if len(found_config_lines) > 0:
#         checks_data["TLS_ENABLED"] = True
#         # Now check wthether the line is commented
#         if len(re.findall('#\s*export\s+JAVA_OPTS=\"\s*\${JAVA_OPTS:-.*Dio\.atomix\.enableNettyTLS=true',
#                           onos_service_file)) == 0:
#             checks_data["CONFIG_LINE_NOT_COMMENTED"] = True
#
#     # Check for keystore and trust store key and password
#     if len(re.findall(
#             'export\s+JAVA_OPTS\s*=\s*\"\s*\${\s*JAVA_OPTS:-.*Dio\.atomix\.enableNettyTLS=true\s*-Djavax.net.ssl.keyStore\s*=.*/onos.jks\s*-Djavax.net.ssl.keyStorePassword\s*=.*\s*-Djavax.net.ssl.trustStore\s*=.*\s*-Djavax.net.ssl.trustStorePassword\s*=.*}\"',
#             onos_service_file)) > 0:
#         checks_data["AUTH_CONFIG_FOUND"] = True
#     else:
#         checks_data["AUTH_CONFIG_FOUND"] = False
#
#     complience_pass = checks_data["TLS_ENABLED"] and checks_data["AUTH_CONFIG_FOUND"] and checks_data[
#         "CONFIG_LINE_NOT_COMMENTED"]
#     return complience_pass, checks_data


"""
Redundancy Property
> Goal - If C1 fails then C2 and C3 should take over
> Checks -
    - atomix.conf exists for all controller in the network
    - Do verification
    - In atomix.conf file, 
        - the cluster.node.id should be own IP 
        - partitionGroups.raft.partitionSize should be 3
        - cluster.discovery.nodes should have all the IPs of the other + own controller
"""


def verify_redundancy_property(network_name,  from_log_timestamp: int):
    checks = {
        "PIPELINE_BROKEN": True
    }
    compliance_pass = True

    try:
        network_name = network_name.strip()
        # Fetch network id
        network_id = Neo4JController.get_element_id_from_name(network_name)
        # Fetch all controllers
        controllers = Neo4JController.get_all_controllers_of_network(network_id)

        # Fetch all config files
        config_files = {}
        """
        Expected format :
        {
            "controller_name" : {
                "found" : false, 
                "content": "<>"
            }
        }
        """
        found_all_config_files = True

        for controller in controllers:
            config_files[controller.name] = fetch_atomix_config_controller(network_name, controller.name)
            if config_files[controller.name]["found"]:
                checks[f"CONTROLLER_{controller.name}_ATOMIX_CONFIG_FILE_FOUND"] = True
            else:
                checks[f"CONTROLLER_{controller.name}_ATOMIX_CONFIG_FILE_FOUND"] = False
                found_all_config_files = False

        if found_all_config_files:
            controllers_ips = {}
            controller_ip_list = set()

            # Fetch IPS of controller
            for controller in controllers:
                controller_property = dict(Neo4JController.get_properties(controller.id))
                controllers_ips[controller.name] = controller_property["ip"].split(":")[
                    0] if controller_property is not None else ""
                if controllers_ips[controller.name] != "":
                    controller_ip_list.add(controllers_ips[controller.name])

            # Now verify the config files
            controllers_count = len(controllers)

            # Create checks for all controllers
            for controller in controllers:
                checks[f"CONTROLLER_{controller.name}_ATOMIX_CONFIG_FILE_PARTITION_SIZE_VALID"] = False
                checks[f"CONTROLLER_{controller.name}_ATOMIX_CONFIG_FILE_OWN_IP_VALID"] = False
                checks[f"CONTROLLER_{controller.name}_ATOMIX_CONFIG_FILE_CLUSTER_NODES_VALID"] = False
                checks[f"TRACE_OF_ALL_CONTROLLERS_FOUND_IN_CONTROLLER_{controller.name}_ATOMIX_LOG_FILE"] = False

            # Verify partition size
            for controller in controllers:
                try:
                    if config_files[controller.name]["found"]:
                        if config_files[controller.name]["content"]["partitionGroups"]["raft"][
                            "partitionSize"] == controllers_count:
                            checks[f"CONTROLLER_{controller.name}_ATOMIX_CONFIG_FILE_PARTITION_SIZE_VALID"] = True
                except:
                    pass

            # Verify own ip
            for controller in controllers:
                try:
                    if config_files[controller.name]["found"]:
                        if config_files[controller.name]["content"]["cluster"]["node"]["address"].split(":")[0] == \
                                controllers_ips[controller.name]:
                            checks[f"CONTROLLER_{controller.name}_ATOMIX_CONFIG_FILE_OWN_IP_VALID"] = True
                except:
                    pass

            # Verify cluster nodes
            for controller in controllers:
                try:
                    if config_files[controller.name]["found"]:
                        if set([x["address"].split(":")[0] for x in
                                config_files[controller.name]["content"]["cluster"]["discovery"][
                                    "nodes"]]) == controller_ip_list:
                            checks[f"CONTROLLER_{controller.name}_ATOMIX_CONFIG_FILE_CLUSTER_NODES_VALID"] = True
                except:
                    pass

            # Verify presence of IP of all controllers in log files
            for controller in controllers:
                found_all = True
                for ip in controller_ip_list:
                    count = NetworkLog.objects(message__contains=ip, config_type="atomix.log",
                                network_name=network_name, element_name=controller.name,
                                uploaded_on__gte=from_log_timestamp).count()
                    if count == 0:
                        found_all = False

                checks[f"TRACE_OF_ALL_CONTROLLERS_FOUND_IN_CONTROLLER_{controller.name}_ATOMIX_LOG_FILE"] = found_all
            

            del checks["PIPELINE_BROKEN"]
    except Exception as e:
        print(e)

    for key in checks:
        compliance_pass = compliance_pass and checks[key]

    return {
        "checks": checks,
        "pass": compliance_pass
    }


"""
check backup property
    - checks presence of onos-backup and onos-restore files
"""


def verify_backup_property(network_name):
    checks = {
        "ONOS_RESTORE_FOUND": EvidenceData.objects.filter(network_name=network_name,
                                                          evidence_type="onos-restore").exists(),
        "ONOS_BACKUP_FOUND": EvidenceData.objects.filter(network_name=network_name,
                                                         evidence_type="onos-backup").exists()
    }

    compliance_pass = checks["ONOS_BACKUP_FOUND"] and checks["ONOS_RESTORE_FOUND"]
    return {
        "checks": checks,
        "pass": compliance_pass
    }
