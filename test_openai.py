from openai import OpenAI

client = OpenAI()

try:
    response = client.responses.create(
        model="gpt-5.6-luna",
        input="Hello. Give me one short sentence."
    )

    print("API TEST SUCCESS")
    print("Response:")
    print(response.output_text)

except Exception as e:

    print("\nAPI TEST FAILED")
    print("Error Type:", type(e).__name__)
    print("Error:", str(e))

    if hasattr(e, "body"):
        print("Error Body:", e.body)
