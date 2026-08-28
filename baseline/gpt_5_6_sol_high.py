import os

from dotenv import load_dotenv
from openai import OpenAI

from common import DEFAULT_TEXT_PROMPT, encode_image_as_data_url, get_image_path_arg, timed_request

load_dotenv()

endpoint = "https://ikeda-openai-foundry.services.ai.azure.com/openai/v1"
deployment_name = "gpt-5.6-sol"
api_key = os.environ["gpt_5_6_sol_api_key"]

client = OpenAI(
    base_url=endpoint,
    api_key=api_key,
)

image_path = get_image_path_arg()

if image_path:
    input_content = [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Read the text in this image in vertical columns from right to left, in the correct reading order. Do not output any unnecessary characters."},
                {"type": "input_image", "image_url": encode_image_as_data_url(image_path)},
            ],
        }
    ]
else:
    input_content = DEFAULT_TEXT_PROMPT

with timed_request():
    response = client.responses.create(
        model=deployment_name,
        input=input_content,
        reasoning={"effort": "high"},
    )

print(response.output_text)
