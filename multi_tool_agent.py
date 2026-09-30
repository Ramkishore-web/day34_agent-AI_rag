import json
from openai import OpenAI


client = OpenAI()

MODEL = "gpt-5.6-luna"


# -------------------------------
# TOOL 1: CALCULATOR
# -------------------------------

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


# -------------------------------
# TOOL 2: RAG
# -------------------------------

def search_rag(query):

    # For this first LLM tool-calling test,
    # we use your Day 33 invoice knowledge.

    documents = [
        "ABC TRADERS. Invoice Number: INV-1025",
        "Customer: Ram Kishore",
        "Product: Laptop. Quantity: 2. Price: 80000",
        "Total Amount: 160000"
    ]

    query_lower = query.lower()

    matches = []

    for document in documents:

        document_lower = document.lower()

        if "customer" in query_lower and "customer" in document_lower:
            matches.append(document)

        elif "invoice" in query_lower and "invoice" in document_lower:
            matches.append(document)

        elif "product" in query_lower and "product" in document_lower:
            matches.append(document)

        elif "quantity" in query_lower and "quantity" in document_lower:
            matches.append(document)

        elif "price" in query_lower and "price" in document_lower:
            matches.append(document)

        elif "total amount" in query_lower and "total amount" in document_lower:
            matches.append(document)

    if not matches:
        return "No relevant document found."

    return "\n".join(matches)


# -------------------------------
# TOOL SCHEMAS
# -------------------------------

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
    },

    {
        "type": "function",
        "name": "search_rag",
        "description": "Search company and invoice documents for relevant information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The information to search for."
                }
            },
            "required": [
                "query"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
]


# -------------------------------
# TEST QUESTION
# -------------------------------

question = "Who is the customer in invoice INV-1025?"


# -------------------------------
# FIRST LLM CALL
# -------------------------------

response = client.responses.create(
    model=MODEL,
    tools=tools,
    input=question
)


print("\nUser:")
print(question)


# -------------------------------
# PROCESS TOOL CALL
# -------------------------------

tool_outputs = []

for item in response.output:

    if item.type != "function_call":
        continue

    print("\nLLM Selected Tool:")
    print(item.name)

    print("\nArguments:")
    print(item.arguments)

    arguments = json.loads(item.arguments)

    if item.name == "calculate":

        result = calculate(
            arguments["operation"],
            arguments["a"],
            arguments["b"]
        )

    elif item.name == "search_rag":

        result = search_rag(
            arguments["query"]
        )

    else:

        result = "Unknown tool."

    print("\nTool Result:")
    print(result)

    tool_outputs.append(
        {
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": str(result)
        }
    )


# -------------------------------
# SECOND LLM CALL
# -------------------------------

if tool_outputs:

    final_response = client.responses.create(
        model=MODEL,
        tools=tools,
        input=[
            {
                "role": "user",
                "content": question
            },
            *response.output,
            *tool_outputs
        ]
    )

    print("\nFinal Answer:")
    print(final_response.output_text)

else:

    print("\nFinal Answer:")
    print(response.output_text)
