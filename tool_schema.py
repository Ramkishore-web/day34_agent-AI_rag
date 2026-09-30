calculator_tool_schema = {
    "name": "calculator",
    "description": "Perform basic arithmetic calculations.",
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "description": "The arithmetic operation to perform.",
                "enum": [
                    "add",
                    "subtract",
                    "multiply",
                    "divide"
                ]
            },
            "a": {
                "type": "number",
                "description": "The first number."
            },
            "b": {
                "type": "number",
                "description": "The second number."
            }
        },
        "required": [
            "operation",
            "a",
            "b"
        ]
    }
}


if __name__ == "__main__":

    print("Tool Name:", calculator_tool_schema["name"])
    print("Description:", calculator_tool_schema["description"])
    print("Parameters:")
    print(calculator_tool_schema["parameters"])
