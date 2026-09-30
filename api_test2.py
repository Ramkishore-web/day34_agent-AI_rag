from openai import OpenAI

client = OpenAI()

try:
    r = client.responses.create(
        model="gpt-5.6-luna",
        input="Say hello in one sentence."
    )
    print("SUCCESS")
    print(r.output_text)

except Exception as e:
    print("TYPE:", type(e).__name__)
    print("MESSAGE:", str(e))
