import os
import base64
from openai import OpenAI


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your local image
image_path = "Test1.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

client = OpenAI(
    api_key="sk-fb39b18cdd054cd19f38295a47520d6a",  # Directly pass the API key string
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-vl-max-latest",
    messages=[
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."}],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"  # Use base64 encoded image
                    },
                },
                {"type": "text", "text": "图中描绘的是什么景象?"},
            ],
        },
    ],
)

print(completion.choices[0].message.content)
