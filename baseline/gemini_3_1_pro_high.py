import os

from dotenv import load_dotenv
from google import genai

from common import DEFAULT_TEXT_PROMPT, encode_image, get_image_path_arg, timed_request

load_dotenv()

client = genai.Client(
    api_key=os.environ["gemini_3_1_pro_api_key"],
)

generation_config = {
    'max_output_tokens': 65536,
    'top_p': 0.95,
    'thinking_level': 'high',
}

image_path = get_image_path_arg()

if image_path:
    image_data, mime_type = encode_image(image_path)
    input_content = [
        {"type": "text", "text": "Read the text in this image in vertical columns from right to left, in the correct reading order. Do not output any unnecessary characters."},
        {"type": "image", "data": image_data, "mime_type": mime_type},
    ]
else:
    input_content = DEFAULT_TEXT_PROMPT

with timed_request():
    interaction = client.interactions.create(
        model='models/gemini-3.1-pro-preview',
        input=input_content,
        generation_config=generation_config,
    )

print(interaction.output_text)
