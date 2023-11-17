import openai
import os
openai.api_key = os.getenv('OPENAI')

content = """Classify the text into one of the classes.
Classes: [`positive`, `negative`, `neutral`]
Text: Sunny weather makes me happy.
Class: `positive`

Text: The food is terrible.
Class: `negative`

Text: I love popcorn.
Class: `positive`

Text: This book left me a wonderful impression.
Class: """

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  temperature=0.6,
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

{
  "id": "chatcmpl-7qdGDlPbJdnoUCwIer5B0UFhQsWF2",
  "object": "chat.completion",
  "created": 1692778329,
  "model": "gpt-3.5-turbo-0613",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "`positive`"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 80,
    "completion_tokens": 3,
    "total_tokens": 83
  }
}


print(response["choices"][0]["message"]["content"])