Blockly.defineBlocksWithJsonArray([
    {
        "type": "exists_evidence_type_element",
        "output": "Boolean",
        "colour": 26,
        "message0": "evidence exists ? ",
        "args0": [],
        "message1": "type %1",
        "args1": [
            {
                "type": "input_value",
                "name": "TYPE",
                "check": "String",
                "align": "RIGHT"
            }
        ],
        "message2": "element %1",
        "args2": [
            {
                "type": "input_value",
                "name": "ELEMENT",
                "check": "String",
                "align": "RIGHT"
            }
        ],
        "tooltip": "Check if evidence exists",
    },
    {
        "type": "exists_evidence_type",
        "output": "Boolean",
        "colour": 26,
        "message0": "evidence exists ? ",
        "args0": [],
        "message1": "type %1",
        "args1": [
            {
                "type": "input_value",
                "name": "TYPE",
                "check": "String",
                "align": "RIGHT"
            }
        ]
    },
    {
        "type": "fetch_evidence_type_element",
        "output": "String",
        "colour": 26,
        "message0": "fetch evidence",
        "args0": [],
        "message1": "type %1",
        "args1": [
            {
                "type": "input_value",
                "name": "TYPE",
                "check": "String",
                "align": "RIGHT"
            }
        ],
        "message2": "element %1",
        "args2": [
            {
                "type": "input_value",
                "name": "ELEMENT",
                "check": "String",
                "align": "RIGHT"
            }
        ],
        "tooltip": "Check if evidence fetch",
    },
    {
        "type": "fetch_evidence_type",
        "output": "String",
        "colour": 26,
        "message0": "fetch evidence",
        "args0": [],
        "message1": "type %1",
        "args1": [
            {
                "type": "input_value",
                "name": "TYPE",
                "check": "String",
                "align": "RIGHT"
            }
        ]
    }
])