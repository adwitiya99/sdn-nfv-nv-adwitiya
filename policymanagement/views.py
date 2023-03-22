import json
import re

from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.utils.datetime_safe import datetime

from policymanagement.config import evidence_data_types
from policymanagement.tasks import startPolicyVerification
from policymanagement.utils import snakecase_to_sentence
from policymanagement.models import EvidenceData, EvidenceDataStore, RegisteredPolicyDetails, PolicyVerificationReport
from policymanagement.config import prefixed_policy_data_types
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from sdntool.Neo4jcontroller import Neo4JController
from sdntool.login_validator import login_check

from logmanager.manager import LogManager
from logmanager.models import LogType, ParserType


# ================ ADD EVIDENCE DATA====================================
@require_http_methods(["GET", "POST"])
@login_check
def addata(request):
    if request.method == 'POST':
        network = request.POST.get('network')
        data_type = request.POST.get('data_type')
        evidence_type = request.POST.get('evidence_type')
        evidence_file = request.FILES.get('evidence_file')
        controller = request.POST.get('controller')
        switch = request.POST.get('switch')
        host = request.POST.get('host')

        # If the evidence type is `log`
        if data_type == 'log':
            log_entry_done = False
            if evidence_type == 'karaf.log':
                file_lines = evidence_file.read().decode('utf-8').split("\n")
                status = LogManager.insertLog(file_lines, LogType.NETWORK, ParserType.KARAF, network_name=network,
                                              element_name=network, config_type=evidence_type)
                log_entry_done = status
            elif evidence_type == 'karaf_ssl.log':
                file_lines = evidence_file.read().decode('utf-8').split("\n")
                status = LogManager.insertLog(file_lines, LogType.NETWORK, ParserType.KARAF, network_name=network,
                                              element_name=controller, config_type=evidence_type)
                log_entry_done = status
            elif evidence_type == 'ping.log':
                file_lines = evidence_file.read().decode('utf-8').split("\n")
                status = LogManager.insertLog(file_lines, LogType.NETWORK, ParserType.PING, network_name=network,
                                              element_name=host, config_type=evidence_type)
                log_entry_done = status
            elif evidence_type == 'atomix.log':
                file_lines = evidence_file.read().decode('utf-8').split("\n")
                status = LogManager.insertLog(file_lines, LogType.NETWORK, ParserType.ATOMIX, network_name=network,
                                              element_name=controller, config_type=evidence_type)
                log_entry_done = status
            elif evidence_type == 'devices.log':
                file_lines = evidence_file.read().decode('utf-8').split("\n")
                status = LogManager.insertLog(file_lines, LogType.NETWORK, ParserType.DEVICES, network_name=network,
                                              element_name=controller, config_type=evidence_type)
                log_entry_done = status
            if log_entry_done:
                try:
                    # Search object
                    elements_involved = network
                    if evidence_type == "karaf_ssl.log" or evidence_type == "devices.log" or evidence_type == "atomix.log":
                        elements_involved = controller
                    evidence_data = EvidenceData.objects.get(
                        network_name=network,
                        is_log=True,
                        evidence_type=evidence_type,
                        elements_involved=elements_involved,
                        selected_switch_name=switch,
                        selected_host_name=host,
                        selected_controller_name=controller
                    )
                    evidence_data.last_updated = datetime.now()
                    evidence_data.save()
                    messages.success(request, "Evidence data already exists ! Updated successfully")
                except EvidenceData.DoesNotExist:
                    # Create object
                    EvidenceData.objects.create(
                        network_name=network,
                        is_log=True,
                        evidence_type=evidence_type,
                        elements_involved=network,
                        selected_switch_name=switch,
                        selected_host_name=host,
                        selected_controller_name=controller
                    )
                    messages.success(request, "Evidence data added successfully")


        # If the evidence type is `config`
        elif data_type == 'config':
            if evidence_type == 'flow-rule':
                """
                Special Note For Flow Rule 
                We dont taking for any host name
                But, we will put  `ETH_DST` in `selected_host_name` field
                As, we cant distinguish multiple flow record of same hosts
                """
                for file in request.FILES.getlist("evidence_file"):
                    ETH_DST_HOST_NAME = None
                    ETH_DST_HOST_MAC = None
                    file_content = file.read().decode('utf-8')
                    file_content_json = json.loads(file_content)
                    # Resolve the dst host name
                    for record in file_content_json['selector']['criteria']:
                        if record['type'] == 'ETH_DST':
                            ETH_DST_HOST_MAC = record['mac']
                            break
                    # Find macs
                    macs = list(re.findall(r'"mac": "(.*?)"', file_content))
                    hosts_name = []
                    for mac in macs:
                        r = Neo4JController.get_host_name_by_mac(network, mac)
                        if r is not None:
                            hosts_name.append(r)
                            if mac == ETH_DST_HOST_MAC:
                                ETH_DST_HOST_NAME = r
                    if len(hosts_name) < 2:
                        continue
                    if ETH_DST_HOST_NAME is None:
                        continue
                    sorted(hosts_name)
                    hosts_name = " ".join(hosts_name)

                    # Create entry in EvidenceDataStore
                    evidence_data_store = EvidenceDataStore.objects.create(content=file_content)
                    # Create entry in EvidenceData
                    isExists = EvidenceData.objects.filter(network_name=network, is_log=False,
                                                           evidence_type=evidence_type,
                                                           elements_involved=hosts_name,
                                                           selected_host_name=ETH_DST_HOST_NAME
                                                           ).exists()
                    if isExists:
                        evidence_data = EvidenceData.objects.get(network_name=network, is_log=False,
                                                                 evidence_type=evidence_type,
                                                                 elements_involved=hosts_name,
                                                                 selected_host_name=ETH_DST_HOST_NAME
                                                                 )
                        evidence_data.evidence_data = evidence_data_store
                        evidence_data.last_updated = datetime.now()
                        evidence_data.save()
                        messages.success(request, "Evidence data already exists ! Updated successfully")
                    else:
                        EvidenceData.objects.create(network_name=network, is_log=False, evidence_type=evidence_type,
                                                    elements_involved=hosts_name, evidence_data=evidence_data_store,
                                                    selected_host_name=ETH_DST_HOST_NAME
                                                    )
                        messages.success(request, "Evidence data added successfully")
            elif evidence_type == "onos-backup" or evidence_type == "onos-restore":
                # Store in EvidenceDataStore
                evidence_data_store = EvidenceDataStore.objects.create(content=evidence_file.read().decode('utf-8'))
                isExists = EvidenceData.objects.filter(network_name=network, is_log=False, evidence_type=evidence_type).exists()
                if not isExists:
                    # Create EvidenceData
                    EvidenceData.objects.create(
                        network_name=network,
                        is_log=False,
                        evidence_type=evidence_type,
                        evidence_data=evidence_data_store
                    )
                    messages.success(request, "Evidence data added successfully")
                else:
                    EvidenceData.objects.filter(network_name=network, is_log=False, evidence_type=evidence_type)\
                        .update(
                        evidence_data=evidence_data_store
                    )
                    messages.success(request, "Evidence data already exists ! Updated successfully")
            elif evidence_type == 'onos-service' or evidence_type == 'atomix-conf':
                # Store in EvidenceDataStore
                evidence_data_store = EvidenceDataStore.objects.create(content=evidence_file.read().decode('utf-8'))
                isExists = EvidenceData.objects.filter(network_name=network, is_log=False, evidence_type=evidence_type,
                                                       elements_involved=controller, selected_controller_name=controller).exists()
                if not isExists:
                    # Create EvidenceData
                    EvidenceData.objects.create(
                        network_name=network,
                        is_log=False,
                        evidence_type=evidence_type,
                        elements_involved=controller,
                        evidence_data=evidence_data_store,
                        selected_controller_name=controller
                    )
                    messages.success(request, "Evidence data added successfully")
                else:
                    EvidenceData.objects.filter(network_name=network, is_log=False, evidence_type=evidence_type,
                                                elements_involved=controller, selected_controller_name=controller).update(
                        evidence_data=evidence_data_store
                    )
                    messages.success(request, "Evidence data already exists ! Updated successfully")

    networks = [x.to_json(minified=True) for x in Neo4JController.get_networks()]
    return render(request, 'policymanagement/addevidence.html', {
        'all_networks': networks,
        'all_networks_safe': json.dumps(networks),
        'evidence_data_types': json.dumps(evidence_data_types)
    })


# ========================================================================

# ================ MODIFY EVIDENCE DATA====================================
@require_GET
@login_check
def managedata(request):
    data = {
        'all_networks': [x.to_json(minified=True) for x in Neo4JController.get_networks()]
    }
    selected_network = request.GET.get('selected_network', "")
    action = request.GET.get("action", "")
    if selected_network != "":
        data['selected_network'] = selected_network

    if action == "delete":
        try:
            record_id = int(request.GET.get("record_id", ""))
            if record_id != "":
                EvidenceData.objects.filter(id=record_id, is_log=False).delete()
            messages.success(request, "Evidence data deleted successfully")
        except:
            messages.error(request, "Error deleting evidence record")

        return redirect(reverse("managedata") + '?selected_network=' + selected_network)

    if selected_network != "":
        data['evidence_data'] = EvidenceData.objects.filter(network_name=selected_network).order_by('-last_updated')
    return render(request, 'policymanagement/manageevidence.html', data)


# ========================================================================

# ================ POLICY DETAILS====================================
@require_http_methods(["GET", "POST"])
@login_check
def managepolicy(request):
    action = request.GET.get('action', "")
    data = {}
    networks = [x.to_json(minified=True) for x in Neo4JController.get_networks()]
    data['all_networks'] = networks
    data['all_networks_safe'] = json.dumps(networks)
    data['policy_types'] = prefixed_policy_data_types
    data['policy_data_types'] = json.dumps(prefixed_policy_data_types)
    selected_network = request.GET.get('selected_network', "")
    if selected_network != "":
        data['selected_network'] = selected_network

    if request.method == "POST":
        selected_policy = request.POST.get("selected_policy", "")
        policy_details = None
        for policy in prefixed_policy_data_types:
            if policy['type'] == selected_policy:
                policy_details = policy
                break
        if policy_details is None:
            raise Exception("400 bad request")
        keys = [x["key"] for x in policy_details["fields"]]
        config = {}
        for key in keys:
            config[key] = request.POST.get(key, "")
        RegisteredPolicyDetails.objects.create(
            network_name=selected_network,
            core_policy_label=policy_details["label"],
            core_policy_type=policy_details["type"],
            policy_description=policy_details["description"].format(**config, network_name=selected_network),
            policy_config=json.dumps(config)
        )
        messages.success(request, "Policy added successfully for network {}".format(selected_network))
        return redirect(reverse('managepolicy') + "?selected_network={}".format(selected_network))

    if action == "delete":
        try:
            record_no = int(request.GET.get('record_no', ""))
            RegisteredPolicyDetails.objects.filter(id=record_no).delete()
            messages.success(request, "Policy deleted successfully for network {}".format(selected_network))
        except:
            messages.error(request, "Policy deletion failed for network {}".format(selected_network))
        return redirect(reverse('managepolicy') + '?selected_network={}'.format(selected_network))

    if selected_network != "":
        data['registered_policies'] = RegisteredPolicyDetails.objects.filter(network_name=selected_network)

    return render(request, 'policymanagement/managepolicy.html', data)


# ========================================================================


# ================ VERIFY POLICY ====================================
@require_GET
@login_check
def verifypolicy(request):
    data = {}
    networks = [x.to_json(minified=True) for x in Neo4JController.get_networks()]
    data['all_networks'] = networks
    data['all_networks_safe'] = json.dumps(networks)
    selected_network = request.GET.get('selected_network', "")
    if selected_network != "":
        data['selected_network'] = selected_network

    action = request.GET.get("action", "")
    if action == "verify":
        try:
            record_id = request.GET.get("record_id", "")
            from_date = request.GET.get("from_date", "")
            if from_date == "":
                raise Exception("Invalid date provided")
            log_from_date_timestamp = datetime.strptime(from_date, '%Y-%m-%d')
            policies = []
            if record_id == "all":
                policies = RegisteredPolicyDetails.objects.filter(network_name=selected_network)
            else:
                record_id = int(record_id)
                policies.append(RegisteredPolicyDetails.objects.get(network_name=selected_network, id=record_id))

            submitted_policy_details = []
            for policy in policies:
                tmp = {"id": policy.id, "description": policy.policy_description}
                submitted_policy_details.append(tmp)

            if len(policies) == 0:
                raise Exception("Failed to parse policy")

            record = PolicyVerificationReport.objects.create(
                network_name=selected_network,
                submitted_policy_details=json.dumps(submitted_policy_details),
                verification_result=json.dumps({}),
                status="submitted",
                passed=False,
                log_from_timestamp=log_from_date_timestamp
            )
            startPolicyVerification.delay(record.id)
            messages.success(request, "Policy verification submitted successfully ! You can find update in Report Management Section")
        except Exception as e:
            print(e)
            messages.error(request, "Policy verification failed")
        return redirect(reverse('verifypolicy') + '?selected_network={}'.format(selected_network))

    if selected_network != "":
        data['registered_policies'] = RegisteredPolicyDetails.objects.filter(network_name=selected_network)
    return render(request, 'policymanagement/verifypolicy.html', data)


# ================ REPORT MANAGEMENT====================================
@require_GET
@login_check
def reportmanagement(request):
    data = {}
    networks = [x.to_json(minified=True) for x in Neo4JController.get_networks()]
    data['all_networks'] = networks
    data['all_networks_safe'] = json.dumps(networks)
    selected_network = request.GET.get('selected_network', "")
    if selected_network != "":
        data['selected_network'] = selected_network
    if selected_network != "":
        data['policy_verification_reports'] = PolicyVerificationReport.objects.filter(network_name=selected_network).order_by('-id')

    return render(request, 'policymanagement/reportmanagement.html', data)

# ================= VIEW REPORT ========================================

@require_GET
@login_check
def verificationreportdetails(request, report_id):
    try:
        report = PolicyVerificationReport.objects.get(id=report_id)
        requested_policies = json.loads(report.submitted_policy_details)
        data = {
            "report_id": report.id,
            "network_name": report.network_name,
            "requested_checks": [policy["description"] for policy in requested_policies],
            "runtime_status": report.status,
            "compliance_passed": report.passed,
            "submitted_on": report.submitted_on,
            "completed_on": report.completed_on,
        }

        result = json.loads(report.verification_result)
        formatted_result = []
        """
        [
            {
                "id": 452,
                "description" : "All nodes should have a label",
                "overall_pass": true,
                "details": [
                    {
                        "pass" :  true,
                        "description" : "fdfdfd"
                    }
                ]
            }
        ]
        """
        for policy in requested_policies:
            data_policy = {}
            data_policy["id"] = policy["id"]
            data_policy["description"] = policy["description"]
            if str(data_policy["id"]) in result:
                detailed_policy_report = result[str(data_policy["id"])]
                data_policy["overall_pass"] = detailed_policy_report["pass"]
                data_policy["details"] = []
                for detail in detailed_policy_report["checks"]:
                    data_policy["details"].append({
                        "pass": detailed_policy_report["checks"][detail],
                        "description": snakecase_to_sentence(detail)
                    })
            else:
                data_policy["overall_pass"] = False
                data_policy["details"] = []
            formatted_result.append(data_policy)
        data["formatted_result"] = formatted_result
        return render(request, "policymanagement/verificationReport.html", data)
    except PolicyVerificationReport.DoesNotExist:
        return HttpResponse("Requested report details not found", status=404)
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong ! Contact admin", status=500)