import anthropic

# tool_use

client = anthropic.Anthropic()
weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City and state"},
        },
        "required": ["location"],
    },
}


def execute_tool(name, tool_input):
    """Execute a tool and return the result."""
    print("Executing tool", name)
    print("Input:", tool_input)

    return f"Weather in {tool_input.get('location', 'unknown')}: 71°F"


response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "What is the weather in Sao Paulos - SP?"}],
)

if response.stop_reason == "tool_use":
    print("Tool used")
    # Extraia e execute a ferramenta
    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)
            # Retorne o resultado ao Claude para a resposta final
            print(result)