import anthropic

message = anthropic.Anthropic().messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)

print(message)

for block in message.content:
    if block.type == "text":
        print(block.text)