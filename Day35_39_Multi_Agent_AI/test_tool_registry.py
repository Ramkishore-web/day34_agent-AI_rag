from src.tools.registry import tool_registry


print("=" * 60)
print("REGISTERED TOOLS")
print("=" * 60)

for tool in tool_registry.list_tools():
    print("-", tool)


print("\n" + "=" * 60)
print("CALCULATOR TEST")
print("=" * 60)

result = tool_registry.execute(
    "calculator",
    expression="10000 * 0.18"
)

print(result)


print("\n" + "=" * 60)
print("RAG SEARCH TEST")
print("=" * 60)

result = tool_registry.execute(
    "rag_search",
    query="What is the leave policy?"
)

print(result)


print("\n" + "=" * 60)
print("VALIDATION TEST")
print("=" * 60)

result = tool_registry.execute(
    "validation_tool",
    data={"answer": "Leave policy information"}
)

print(result)