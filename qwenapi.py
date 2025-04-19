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
                {
                    "type": "text",
                    "text": """你是一个专业的图像数据处理助手，负责从提供的发票图片中提取信息，并将其转换为标准化的CSV表格格式。

请分析以下图片，并执行以下任务：

1.  **识别关键信息**：从图片中找出以下发票信息：
    *   发票日期
    *   金额
    *   发票号码

2.  **规范化输出**：将提取的信息整理成CSV格式，字段顺序和格式要求如下：
    *   发票日期 (格式: YYYY-MM-DD)
    *   金额 (单位: 元，保留两位小数)
    *   发票号码

3.  **处理缺失值**：
    *   如果图片中找不到发票日期，请在CSV对应位置填写 "未知"。
    *   如果图片中找不到金额，请在CSV对应位置填写 "0.00"。
    *   如果图片中找不到发票号码，请在CSV对应位置填写 "未知"。

4.  **输出格式示例**：
    ```csv
    发票日期,金额,发票号码
    YYYY-MM-DD,XX.XX,XXXXXXXX
    ```
    请只输出CSV内容，包括表头。

请根据以上规则处理图片中的发票信息。""",
                },
            ],
        },
    ],
)

print(completion.choices[0].message.content)
