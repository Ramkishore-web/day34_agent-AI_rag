from openai import OpenAI

client = OpenAI()

try:
    models = client.models.list()

    print("API connection: SUCCESS")
    print("\nGPT models available to this API key:")

    found = False

    for model in models.data:
        if "gpt-5.6" in model.id or "gpt-6" in model.id:
            print("-", model.id)
            found = True

    if not found:
        print("No GPT-5.6/GPT-6 model was returned.")

except Exception as e:

    print("API TEST FAILED")
    print("Error Type:", type(e).__name__)
    print("Error:", str(e))
