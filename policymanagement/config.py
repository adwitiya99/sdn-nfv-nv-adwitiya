"""
Evidence data type configurations
"""

evidence_data_types = [
    {
        "is_log": True,
        "type": "karaf.log",
        "description": "Karaf log",
        "element": "network",
        "multiple_file_upload_allowed": False
    },
    {
        "is_log": True,
        "type": "karaf_ssl.log",
        "description": "Karaf SSL log",
        "element": "controller",
        "multiple_file_upload_allowed": False
    },
    {
        "is_log": True,
        "type": "ping.log",
        "description": "Ping log",
        "element": "host",
        "multiple_file_upload_allowed": False
    },
    {
        "is_log": True,
        "type": "atomix.log",
        "description": "Atomix log",
        "element": "controller",
        "multiple_file_upload_allowed": False
    },
    {
        "is_log": True,
        "type": "devices.log",
        "description": "Devices log",
        "element": "controller",
        "multiple_file_upload_allowed": False
    },
    {
        "is_log": False,
        "type": "flow-rule",
        "description": "Flow rule",
        "element": "network",
        "multiple_file_upload_allowed": True
    },
    {
        "is_log": False,
        "type": "onos-service",
        "description": "Onos service",
        "element": "controller",
        "multiple_file_upload_allowed": False
    },
    {
        "is_log": False,
        "type": "atomix-conf",
        "description": "Atomix configuration",
        "element": "controller",
        "multiple_file_upload_allowed": False
    },
    {
        "is_log": False,
        "type": "onos-backup",
        "description": "Onos Backup File",
        "element": "network",
        "multiple_file_upload_allowed": False
    },
    {
        "is_log": False,
        "type": "onos-restore",
        "description": "Onos Restore File",
        "element": "network",
        "multiple_file_upload_allowed": False
    },
]

"""
Policy data type configurations
NOTE :
> Before creating a new policy, first need to select the network
"""

prefixed_policy_data_types = [
    {
        "label": "Network Segregation Property [Connected]",
        "type": "network-segregation-property-connected",
        "description": "There should be communication between Host {first_host} and Host {second_host} in the network",
        "fields": [
            {
                "label": "Select First Host ",
                "key": "first_host",
                "element_type": "host",
                "placeholder": "Select a host",
                "input_type": "load_from_db"
            },
            {
                "label": "Select Second Host",
                "key": "second_host",
                "element_type": "host",
                "placeholder": "Select a host",
                "input_type": "load_from_db"
            }
        ]
    },
    {
        "label": "Network Segregation Property [Not Connected]",
        "type": "network-segregation-property-not-connected",
        "description": "There should be NO communication between Host {first_host} and Host {second_host} in the network",
        "fields": [
            {
                "label": "Select First Host ",
                "key": "first_host",
                "element_type": "host",
                "placeholder": "Select a host",
                "input_type": "load_from_db"
            },
            {
                "label": "Select Second Host",
                "key": "second_host",
                "element_type": "host",
                "placeholder": "Select a host",
                "input_type": "load_from_db"
            }
        ]
    },
    {
        "label": "Mutual Authentication Property",
        "type": "mutual-authentication-property",
        "description": "Mutual authentication property for {controller}",
        "fields": [
            {
                "label": "Select Controller",
                "key": "controller",
                "element_type": "controller",
                "placeholder": "Select Controller",
                "input_type": "load_from_db"
            }
        ]
    },
    {
        "label": "Redundancy Property",
        "type": "redundancy-property",
        "description": "Redundancy Property",
        "fields": []
    },
    {
        "label": "Backup Property",
        "type": "backup-property",
        "description": "Backup Property",
        "fields": []
    },
]
