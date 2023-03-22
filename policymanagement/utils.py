import json

from policymanagement.models import EvidenceData

def compare_json(json1, json2):
    def sorting(item):
        if isinstance(item, dict):
            return sorted((key, sorting(values)) for key, values in item.items())
        if isinstance(item, list):
            return sorted(sorting(x) for x in item)
        else:
            return item
    return sorting(json1) == sorting(json2)


def fetch_atomix_config_controller(network_name, controller_name):
    try:
        file = EvidenceData.objects.get(network_name=network_name, evidence_type="atomix-conf", selected_controller_name=controller_name).evidence_data.content
        return {
            "found": True,
            "content": json.loads(file)
        }
    except EvidenceData.DoesNotExist:
        return {
            "found": False,
            "content": {}
        }


def snakecase_to_sentence(input_str):
    return input_str.replace("_", " ").title()
