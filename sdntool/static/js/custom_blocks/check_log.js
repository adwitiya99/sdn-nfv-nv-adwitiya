Blockly.defineBlocksWithJsonArray([
    {
        "type": "check_log_with_type_element_keyword",
        "message0": 'search network log',
        "output": "String",
        "args0": [],
        "message1": "type %1",
        "args1": [
            {
                "type": "input_value",
                "name": "VALUE",
                "check": "String",
                "align": "RIGHT",
                
            }
        ],
        "message2": "element %1",
        "args2": [
            {
                "type": "input_value",
                "name": "VALUE",
                "check": "String",
                "align": "RIGHT"
            }
        ],
        "message3": 'keyword %1',
        "args3": [
            {
                "type": "input_value",
                "name": "VALUE",
                "check": "String",
                "align": "RIGHT"
            }
        ],
        "colour": 241,
    },
    {
        "type": "check_log_with_type_keyword",
        "message0": 'search network log',
        "output": "String",
        "args0": [],
        "message1": "element %1",
        "args1": [
            {
                "type": "input_value",
                "name": "VALUE",
                "check": "String",
                "align": "RIGHT"
            }
        ],
        "message2": 'keyword %1',
        "args2": [
            {
                "type": "input_value",
                "name": "VALUE",
                "check": "String",
                "align": "RIGHT"
            }
        ],
        "colour": 241,
    },
    {
        "type": "check_log_with_type",
        "message0": 'search network log',
        "output": "String",
        "args0": [],
        "message1": "type %1",
        "args1": [
            {
                "type": "input_value",
                "name": "VALUE",
                "check": "String",
                "align": "RIGHT"
            }
        ],
        "colour": 241,
    }
])