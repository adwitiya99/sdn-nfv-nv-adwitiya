Blockly.defineBlocksWithJsonArray([
    {
        "type": "main_entrypoint",
        "colour": 72,
        "message0": "Start",
        "args0": [],
        "message1": "%1",
        "args1": [
            {
                "type": "input_statement",
                "name": "MAIN",
                "check": "define_check"
            }
        ]
    },
    {
        "type": "define_check",
        "colour": 144,
        "message0": "Define check",
        "args0": [],
        "message1": "description %1",
        "args1": [
            {
                "type": "field_input",
                "name": "DESCRIPTION",
                "check": "String",
                "align": "RIGHT",
                "text": "provide a description"
            }
        ],
        "message2": "%1",
        "args2": [
            {
                "type": "input_statement",
                "name": "CHECK"
            }
        ],
        "previousStatement": "define_check",
        "nextStatement": "define_check"
    }
])