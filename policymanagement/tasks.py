import json

from celery import shared_task
from policymanagement.models import PolicyVerificationReport, RegisteredPolicyDetails
from .verifier import verify_backup_property, verify_redundancy_property, mutual_authentication_property, network_segregation_property_for_communication, network_segregation_property_for_no_communication
from datetime import datetime


@shared_task
def startPolicyVerification(policy_verification_record_id):
    policy_verification_record = PolicyVerificationReport.objects.get(id=policy_verification_record_id)
    # Make status `RUNNING`
    policy_verification_record.status = "running"
    policy_verification_record.save()
    # Pick one policy
    doVerify(policy_verification_record)


def doVerify(policy_verification_record: PolicyVerificationReport):
    # check registered policies
    # for each policy call their respective checker functions
    # for any error set policy_verification_record to False
    try:
        checks_data = {}
        # for policy in policy_verification_record:
        policies = json.loads(policy_verification_record.submitted_policy_details)
        for policy in policies:
            temp = RegisteredPolicyDetails.objects.get(id=policy["id"])
            from_log_timestamp = int(policy_verification_record.log_from_timestamp.timestamp()*1000)
            policy_config = json.loads(temp.policy_config)
            if temp.core_policy_type == "backup-property":
                response = verify_backup_property(temp.network_name)
                checks_data[str(temp.id)] = response
            elif temp.core_policy_type == "redundancy-property":
                response = verify_redundancy_property(temp.network_name, from_log_timestamp)
                checks_data[str(temp.id)] = response
            elif temp.core_policy_type == "mutual-authentication-property":
                response = mutual_authentication_property(temp.network_name, policy_config["controller"], from_log_timestamp)
                checks_data[str(temp.id)] = response
            elif temp.core_policy_type == "network-segregation-property-connected":
                response = network_segregation_property_for_communication(policy_config["first_host"], policy_config["second_host"], temp.network_name, from_log_timestamp)
                checks_data[str(temp.id)] = response
            elif temp.core_policy_type == "network-segregation-property-not-connected":
                response = network_segregation_property_for_no_communication(policy_config["first_host"], policy_config["second_host"], temp.network_name, from_log_timestamp)
                checks_data[str(temp.id)] = response

        policy_verification_record.status = "completed"
        policy_verification_record.verification_result = json.dumps(checks_data)

        # Calculate overall passes
        compliance_passed = True
        for check in checks_data.values():
            compliance_passed = check["pass"] and compliance_passed
        policy_verification_record.passed = compliance_passed
        policy_verification_record.completed_on = datetime.now()
        policy_verification_record.save()
    except Exception as e:
        print(e)
        policy_verification_record.status = 'failed'
        policy_verification_record.save()
