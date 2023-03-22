from django.db import models
import  json

# Create your models here.

class EvidenceDataStore(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()


class EvidenceData(models.Model):
    id = models.BigAutoField(primary_key=True)
    network_name = models.CharField(max_length=255)
    is_log = models.BooleanField(default=False)
    evidence_type = models.CharField(max_length=100)
    elements_involved = models.TextField()  # Store list in space seperated  format with lexicographically sorted order
    evidence_data = models.ForeignKey(EvidenceDataStore, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    # These below fields sole purpose is to store the state of form submission to make modification easier for user
    selected_controller_name = models.CharField(max_length=255, null=True)
    selected_switch_name = models.CharField(max_length=255, null=True)
    selected_host_name = models.CharField(max_length=255, null=True)


"""
All the Policies , those are available in the system for configuration for specific network
"""


class CorePolicy(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    fields_info = models.TextField()
    """
    [
        {
            "variable": "H1",
            "type": "host",
            "description": "Host 1"
        },
        {
            "variable": "H2",
            "type": "host",
            "description": "Host 2"
        }
    ]
    """
    blockly_json = models.TextField()
    generated_code = models.TextField(default="")
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_fields_info(self):
        return json.loads(self.fields_info)

    def get_involved_elements(self):
        fields_info = self.get_fields_info()
        return " ".join([field["variable"] for field in fields_info])

    def get_involved_elements_list(self):
        fields_info = self.get_fields_info()
        return [field["variable"] for field in fields_info]

    def get_blockly_json(self):
        return json.loads(self.blockly_json)


"""
Policy details
"""


class RegisteredPolicyDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    network_name = models.CharField(max_length=255)
    core_policy_label = models.CharField(max_length=255)
    core_policy_type = models.CharField(max_length=255)
    policy_description = models.TextField()
    policy_config = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)


"""
Report of verification
"""

PolicyVerificationStatus = (
    ("submitted", "submitted"),
    ("running", "running"),
    ("completed", "completed"),
    ("failed", "failed")
)


class PolicyVerificationReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    network_name = models.CharField(max_length=255)
    submitted_policy_details = models.TextField()  # JSON
    """
    [
        {
            "id": <policy_id>,
            "description": <policy_description>,
        }
    ]
    """
    verification_result = models.TextField()  # JSON
    status = models.CharField(max_length=255, choices=PolicyVerificationStatus, default="submitted")
    passed = models.BooleanField(default=False)
    submitted_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True)
    log_from_timestamp = models.DateTimeField(null=True)
