from pydantic import BaseModel
import anthropic
# ...
class ContactInfo(BaseModel):
    name: str
    email: str
    plan_interest: str
# ...

client = anthropic.Anthropic()
response = client.messages.parse(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Extract contact info: John Smith, john@example.com, interested in the Pro plan",
        }
    ],
    output_format=ContactInfo,
)

# Acesse a saída analisada diretamente
contact = response.parsed_output
print(contact.name, contact.email)