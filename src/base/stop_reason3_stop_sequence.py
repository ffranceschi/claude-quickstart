import anthropic

# stop_sequence
# Claude encontrou uma de suas sequências de parada personalizadas.

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    stop_sequences=["END", "STOP"],
    messages=[{"role": "user", "content": "Generate text until you say END"}],
)

if response.stop_reason == "stop_sequence":
    print(f"Stopped at sequence: {response.stop_sequence}")