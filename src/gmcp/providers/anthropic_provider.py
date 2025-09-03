import os
try:
    import anthropic
except Exception:
    anthropic = None
MODEL = os.getenv("GMCP_ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
class AnthropicProvider:
    def __init__(self, api_key: str = None):
        if anthropic is None:
            raise RuntimeError("anthropic package not installed")
        self.client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    def generate_code(self, prompt: str) -> str:
        msg = self.client.messages.create(model=MODEL, max_tokens=2000, temperature=0.2, messages=[{"role": "user", "content": prompt}])
        parts = []
        for block in msg.content:
            if block.type == "text":
                parts.append(block.text)
        return "\n".join(parts)