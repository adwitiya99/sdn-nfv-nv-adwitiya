Blockly.defineBlocksWithJsonArray([
    {
        "type": "fetch_property",
        "output": "String",
        "colour": 63,
        "message0": "fetch property %1",
        "args0": [
            {
                "type": "field_input",
                "name": "PROPERTY",
                "check": "String"
            }
        ],
        "message1": "element %1",
        "args1": [
            {
                "type": "input_value",
                "name": "OBJECT",
                "check": "String",
                "align": "RIGHT"
            }
        ]
    },
    {
        "type": "search_text",
        "output": "Boolean",
        "colour": 63,
        "message0": 'search text %1',
        "args0": [
            {
                "type": "input_value",
                "name": "TEXT",
                "check": "String",
                "align": "RIGHT"
            }
        ],
        "message1": "keyword %1",
        "args1": [
            {
                "type": "input_value",
                "name": "IN",
                "check": "String",
                "align": "RIGHT"
            }
        ]
    },
    {
        "type": "get_ip",
        "output": "String",
        "colour": 63,
        "message0": 'ip %1',
        "args0": [
            {
                "type": "input_value",
                "name": "IP",
                "check": "String"
            }
        ]
    },
    {
        "type": "get_port",
        "output": "String",
        "colour": 63,
        "message0": 'port %1',
        "args0": [
            {
                "type": "input_value",
                "name": "PORT",
                "check": "String"
            }
        ]
    },
    {
        "type": "get_data_json",
        "output": null,
        "colour": 63,
        "message0": 'json data %1',
        "args0": [
            {
                "type": "input_value",
                "name": "DATA",
            }
        ],
        "message1": "key %1",
        "args1": [
            {
                "type": "input_value",
                "name": "KEY"
            }
        ]
    },
    {
        "type": "json_to_array",
        "output": "Array",
        "colour": 63,
        "message0": 'json to array',
        "args0": [],
        "message1": "data %1",
        "args1": [
            {
                "type": "input_value",
                "name": "JSON",
                "check": "String"
            }
        ],
        "message2": "initial key %1",
        "args2": [
            {
                "type": "field_input",
                "name": "KEY",
                "check": "String",
            }
        ],
        "message3": "method %1",
        "args3": [
            {
                "type": "field_input",
                "name": "METHOD",
                "check": "String"
            }
        ],
        "inputsInline": false
    },
    {
        "type": "map_function",
        "output": "Array",
        "colour": 63,
        "message0": 'map %1',
        "args0": [
            {
                "type": "field_variable",
                "name": "ARRAY",
                "variable": "tmp",
                "check": null
            }
        ],
        "message1": "data %1",
        "args1": [
            {
                "type": "input_value",
                "name": "DATA",
                "check": "Array"
            }
        ],
        "message2": "output %1",
        "args2": [
            {
                "type": "input_value",
                "name": "FUNCTION",
                "check": null
            }
        ]
    }
])