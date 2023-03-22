Blockly.defineBlocksWithJsonArray([
    {
        "type": "all_elements",
        "output": "Array",
        "colour": 63,
        "message0": "all %1",
        "args0": [
            {
                "type": "field_dropdown",
                "name": "ELEMENT",
                "options": [
                    ["Controller", "controller"],
                    ["Switch", "switch"],
                    ["Router", "router"],
                    ["Host", "host"]
                ]
            }
        ]

    }
])