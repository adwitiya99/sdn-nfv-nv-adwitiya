Blockly.defineBlocksWithJsonArray([
    {
        "type": "string",
        "message0": '%1',
        "args0": [
            {
                "type": "field_input",
                "name": "VALUE",
                "text": "text"
            }
        ],
        "output": "String",
        "colour": 230
    },
    {
        "type": "config_type",
        "message0": '%1',
        "args0": [
            {
                "type": "field_dropdown",
                "name": "VALUE",
                "options": [
                    ["atomix.conf", "atomix.conf"],
                    ["onos-service", "onos-service"],
                    ["onos.properties", "onos.properties"],
                    ["onos-backup", "onos-backup"],
                    ["onos-restore", "onos-restore"],
                    ["cluster.json", "cluster.json"],
                    ["karaf-ssl.cfg", "karaf-ssl.cfg"],
                    ["flow-rule.json", "flow-rule.json"]
                ]
            }
        ],
        "output": "String",
        "colour": 230
    },
    {
        "type": "evidence_type",
        "message0": '%1',
        "args0": [
            {
                "type": "field_dropdown",
                "name": "VALUE",
                "options": [
                    ["atomix.log", "atomix.log"],
                    ["karaf-ssl.log", "karaf-ssl.log"],
                    ["ping.log", "ping.log"],
                    ["devices.log", "devices.log"],
                ]
            }
        ],
        "output": "String",
        "colour": 230
    }
])