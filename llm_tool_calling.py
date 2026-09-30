import json
from openai import OpenAI


client = OpenAI()


def calculate(operation, a, b):

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":

        if b == 0:
            return "Error: Cannot divide by zero."

        return a / b

    return "Unsupported operation."


tools = [
    {
        "type": "function",
        "name": "calculate",
        "description": "Perform basic arithmetic calculations.",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": [
                        "add",
                        "subtract",
                        "multiply",
                        "divide"
                    ]
                },
                "a": {
                    "type": "number"
                },
                "b": {
                    "type": "number"
                }
            },
            "required": [
                "operation",
                "a",
                "b"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
]


question = "What is 80000 multiplied by 2?"


response = client.responses.create(
    model="gpt-5.6-luna",
    tools=tools,
    input=question
)


for item in response.output:

    if item.type == "function_call":

        print("\nModel selected tool:")
        print(item.name)

        print("\nArguments:")
        print(item.arguments)

        arguments = json.loads(item.arguments)

        result = calculate(
            arguments["operation"],
            arguments["a"],
            arguments["b"]
        )

        print("\nTool result:")
        print(result)

        tool_output = {
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": str(result)
        }

        final_response = client.responses.create(
            model="gpt-5.6-luna",
            tools=tools,
            input=[
                {
                    "role": "user",
                    "content": question
                },
                *response.output,
                tool_output
            ]
        )

        print("\nFinal Answer:")
        print(final_response.output_text)
