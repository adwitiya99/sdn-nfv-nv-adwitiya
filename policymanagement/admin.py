from django.contrib import admin
from policymanagement.models import EvidenceData, EvidenceDataStore, PolicyVerificationReport, RegisteredPolicyDetails, CorePolicy

# Register your models here.
admin.site.register(EvidenceData)
admin.site.register(EvidenceDataStore)
admin.site.register(PolicyVerificationReport)
admin.site.register(RegisteredPolicyDetails)
admin.site.register(CorePolicy)