import anthropic

# Resposta ok

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)
if response.stop_reason == "end_turn":
    # Processa a resposta completa
    for block in response.content:
        if block.type == "text":
            print(block.text)