from openai import OpenAI
import config

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= config.TOKEN,
)

def get_answer(Message):
    completion = client.chat.completions.create(
    extra_headers={},
    extra_body={},
    model="deepseek/deepseek-r1-0528:free",
    messages=[
        {
        "role": "user",
        "content": str(Message) + ". Пожалуйста, пиши кратко и понятно, не превышая 200 символов, пиши без лишних символов: без эмодзи, здвездочек и прочего. Будь лаконичен"
        }
    ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

