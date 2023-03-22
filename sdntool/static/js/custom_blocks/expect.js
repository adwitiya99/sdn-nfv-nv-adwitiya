Blockly.defineBlocksWithJsonArray([
    {
        "type": "expect_boolean",
        "message0": 'expect %1 %2',
        "args0": [
            {
                "type": "field_dropdown",
                "name": "VALUE",
                "options": [
                    ["Yes", "true"],
                    ["No", "false"]
                ]
            },
            {
                "type": "input_value",
                "name": "VALUE",
                "check": "Boolean",
                "align": "RIGHT"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 328,
    },
    {
        "type": "expect_number",
        "message0": 'expect %1 %2',
        "args0": [
            {
                "type": "field_number",
                "name": "VALUE",
                "value": 0,
                "min": -Infinity,
                "max": Infinity
            },
            {
                "type": "input_value",
                "name": "VALUE",
                "check": "Number",
                "align": "RIGHT"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 328,
    },
    {
        "type": "expect_string",
        "message0": 'expect %1 %2',
        "args0": [
            {
                "type": "field_input",
                "name": "VALUE",
                "text": "text"
            },
            {
                "type": "input_value",
                "name": "VALUE",
                "check": "String",
                "align": "RIGHT"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 328,
    },
    {
        "type": "expect_variable",
        "message0": 'expect %1 %2 %3',
        "args0": [
            {
                "type": "input_value",
                "name": "VALUE",
                "check": null,
            },
            {
                "type": "field_dropdown",
                "name": "VALUE",
                "options": [
                    ["==", "equal"],
                    ["!=", "not equal"],
                    [">", "greater than"],
                    ["<", "less than"],
                    [">=", "greater than or equal"],
                    ["<=", "less than or equal"]
                ]
            },
            {
                "type": "input_value",
                "name": "VALUE",
                "check": null
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 328,
        "inputsInline": true,                
    }
])