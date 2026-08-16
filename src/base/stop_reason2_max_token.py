import anthropic

# Resposta cortada com max_token

client = anthropic.Anthropic()
# Requisição com tokens limitados
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=10,
    messages=[{"role": "user", "content": "Explain quantum physics"}],
)

if response.stop_reason == "max_tokens":
    # A resposta foi truncada
    print("Response was cut off at token limit")
    # Considere fazer outra requisição para continuar