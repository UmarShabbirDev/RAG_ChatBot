
from openai import OpenAI
client = OpenAI()
def GetChatgptResponse(prompt):
    response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    )
    bot_response = response.choices[0].message.content
    print(bot_response)
    return bot_response