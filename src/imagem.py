import base64
import httpx
import anthropic

# Opção 1: Imagem codificada em Base64
image_url = "https://platform.claude.com/docs/images/vision-example.jpg"
image_media_type = "image/jpeg"
image_data = base64.standard_b64encode(httpx.get(image_url).content).decode("utf-8")

message = anthropic.Anthropic().messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data,
                    },
                },
                {"type": "text", "text": "What is in the above image?"},
            ],
        }
    ],
)
print(message)

# Opção 2: Imagem referenciada por URL
message_from_url = anthropic.Anthropic().messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://platform.claude.com/docs/images/vision-example.jpg",
                    },
                },
                {"type": "text", "text": "What is in the above image?"},
            ],
        }
    ],
)
print(message_from_url)