import openai, json

with open("./json/openai.json") as f:
    openaikey = json.load(f)["key"]

openai.api_key = openaikey

# question = "What is 1+1?"

def ask(question):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=question,
        temperature=0.30,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return str(response.choices[0]["text"])
