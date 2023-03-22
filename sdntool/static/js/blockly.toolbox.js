const toolbox = {
  "kind": "categoryToolbox",
  "contents": [
    {
      "kind": "category",
      "name": "Entrypoint",
      "colour": 144,
      "contents": [
        {
          "kind": "block",
          "type": "main_entrypoint"
        },
        {
          "kind": "block",
          "type": "define_check"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Expect",
      "colour": 328,
      "contents": [
        {
          "kind": "block",
          "type": "expect_boolean"
        },
        {
          "kind": "block",
          "type": "expect_number"
        },
        {
          "kind": "block",
          "type": "expect_string"
        },
        {
          "kind": "block",
          "type": "expect_variable"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Elements",
      "colour": 63,
      "contents": [
        {
          "kind": "block",
          "type": "all_elements"
        },
      ]
    },
    {
      "kind": "category",
      "name": "Network Log",
      "colour": 241,
      "contents": [
        {
          "kind": "block",
          "type": "check_log_with_type_element_keyword"
        },
        {
          "kind": "block",
          "type": "check_log_with_type_keyword"
        },
        {
          "kind": "block",
          "type": "check_log_with_type"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Evidence Data",
      "colour": 26,
      "contents": [
        {
          "kind": "block",
          "type": "exists_evidence_type_element"
        },
        {
          "kind": "block",
          "type": "exists_evidence_type"
        },
        {
          "kind": "block",
          "type": "fetch_evidence_type_element"
        },
        {
          "kind": "block",
          "type": "fetch_evidence_type"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Utility",
      "colour": 63,
      "contents": [
        {
          "kind": "block",
          "type": "fetch_property"
        },
        {
          "kind": "block",
          "type": "search_text"
        },
        {
          "kind": "block",
          "type": "get_ip",
        },
        {
          "kind": "block",
          "type": "get_port",
        },
        {
          "kind": "block",
          "type": "get_data_json",
        },
        {
          "kind": "block",
          "type": "json_to_array"
        },
        {
          "kind": "block",
          "type": "controls_forEach"
        },
        {
          "kind": "block",
          "type": "controls_if"
        },
        {
          "kind": "block",
          "type": "map_function"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Data Types",
      "colour": 230,
      "contents": [
        {
          "kind": "block",
          "type": "string"
        },
        {
          "kind": "block",
          "type": "config_type"
        },
        {
          "kind": "block",
          "type": "evidence_type"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Variables",
      "categorystyle": "variable_category",
      "custom": "VARIABLE"
    },
    {
      "kind": "category",
      "name": "Other",
      "colour": 230,
      "contents": [
        {
          "kind": "category",
          "name": "Control",
          "categorystyle": "logic_category",
          "contents": [
            {
              "kind": "block",
              "type": "controls_if"
            },
            {
              "kind": "block",
              "type": "controls_if",
              "extraState": {
                "hasElse": "true"
              }
            },
            {
              "kind": "block",
              "type": "controls_if",
              "extraState": {
                "hasElse": "true",
                "elseIfCount": 1
              }
            }
          ]
        },


        {
          "kind": "category",
          "name": "Logic",
          "categorystyle": "logic_category",
          "contents": [
            {
              "kind": "block",
              "type": "logic_compare"
            },
            {
              "kind": "block",
              "type": "logic_operation"
            },
            {
              "kind": "block",
              "type": "logic_negate"
            },
            {
              "kind": "block",
              "type": "logic_boolean"
            },
            {
              "kind": "block",
              "type": "logic_null"
            },
            {
              "kind": "block",
              "type": "logic_ternary"
            }
          ]
        },


        {
          "kind": "category",
          "name": "Math",
          "categorystyle": "math_category",
          "contents": [
            {
              "kind": "block",
              "type": "math_number",
              "fields": {
                "NUM": 123
              }
            },
            {
              "kind": "block",
              "type": "math_arithmetic",
              "fields": {
                "OP": "ADD"
              }
            },
            {
              "kind": "block",
              "type": "math_single",
              "fields": {
                "OP": "ROOT"
              }
            },
            {
              "kind": "block",
              "type": "math_trig",
              "fields": {
                "OP": "SIN"
              }
            },
            {
              "kind": "block",
              "type": "math_constant",
              "fields": {
                "CONSTANT": "PI"
              }
            },
            {
              "kind": "block",
              "type": "math_number_property",
              "extraState": "<mutation divisor_input=\"false\"></mutation>",
              "fields": {
                "PROPERTY": "EVEN"
              }
            },
            {
              "kind": "block",
              "type": "math_round",
              "fields": {
                "OP": "ROUND"
              }
            },
            {
              "kind": "block",
              "type": "math_on_list",
              "extraState": "<mutation op=\"SUM\"></mutation>",
              "fields": {
                "OP": "SUM"
              }
            },
            {
              "kind": "block",
              "type": "math_modulo"
            },
            {
              "kind": "block",
              "type": "math_constrain",
              "inputs": {
                "LOW": {
                  "block": {
                    "type": "math_number",
                    "fields": {
                      "NUM": 1
                    }
                  }
                },
                "HIGH": {
                  "block": {
                    "type": "math_number",
                    "fields": {
                      "NUM": 100
                    }
                  }
                }
              }
            },
          ]
        },


        {
          "kind": "category",
          "name": "Loops",
          "categorystyle": "loop_category",
          "contents": [
            {
              "kind": "block",
              "type": "controls_repeat_ext",
              "inputs": {
                "TIMES": {
                  "block": {
                    "type": "math_number",
                    "fields": {
                      "NUM": 10
                    }
                  }
                }
              }
            },
            {
              "kind": "block",
              "type": "controls_whileUntil"
            },
            {
              "kind": "block",
              "type": "controls_for",
              "fields": {
                "VAR": "i"
              },
              "inputs": {
                "FROM": {
                  "block": {
                    "type": "math_number",
                    "fields": {
                      "NUM": 1
                    }
                  }
                },
                "TO": {
                  "block": {
                    "type": "math_number",
                    "fields": {
                      "NUM": 10
                    }
                  }
                },
                "BY": {
                  "block": {
                    "type": "math_number",
                    "fields": {
                      "NUM": 1
                    }
                  }
                }
              }
            },
            {
              "kind": "block",
              "type": "controls_forEach"
            },
            {
              "kind": "block",
              "type": "controls_flow_statements"
            }
          ]
        },


        {
          "kind": "category",
          "name": "Lists",
          "categorystyle": "list_category",
          "contents": [
            {
              "kind": "block",
              "type": "lists_create_empty"
            },
            {
              "kind": "block",
              "type": "lists_create_with",
              "extraState": {
                "itemCount": 3
              }
            },
            {
              "kind": "block",
              "type": "lists_repeat",
              "inputs": {
                "NUM": {
                  "block": {
                    "type": "math_number",
                    "fields": {
                      "NUM": 5
                    }
                  }
                }
              }
            },
            {
              "kind": "block",
              "type": "lists_length"
            },
            {
              "kind": "block",
              "type": "lists_isEmpty"
            },
            {
              "kind": "block",
              "type": "lists_indexOf",
              "fields": {
                "END": "FIRST"
              }
            },
            {
              "kind": "block",
              "type": "lists_getIndex",
              "fields": {
                "MODE": "GET",
                "WHERE": "FROM_START"
              }
            },
            {
              "kind": "block",
              "type": "lists_setIndex",
              "fields": {
                "MODE": "SET",
                "WHERE": "FROM_START"
              }
            }
          ]
        },
        {
          "kind": "category",
          "name": "Functions",
          "categorystyle": "procedure_category",
          "custom": "PROCEDURE"
        }
      ]
    },

  ]
}
