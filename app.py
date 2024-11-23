import openai

openai.api_key = 'anything'
openai.base_url = "https://api.pawan.krd/cosmosrp/v1/chat/completions"

completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "How do I list all files in a directory using Python?"},
    ],
)

print(completion.choices[0].message.content)