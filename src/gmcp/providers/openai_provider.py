import os
try:
    from openai import OpenAI
except Exception:
    OpenAI = None
MODEL = os.getenv("GMCP_OPENAI_MODEL", "gpt-4o-mini")
class OpenAIProvider:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if OpenAI is None:
            raise RuntimeError("openai package not installed")
        self.client = OpenAI(api_key=self.api_key)
    def generate_code(self, prompt: str) -> str:
        resp = self.client.responses.create(model=MODEL, input=[{"role": "user", "content": prompt}], temperature=0.2)
        for item in resp.output:
            if item.type == "message":
                for content in item.message.content:
                    if content.type == "text":
                        return content.text
        if hasattr(resp, "output_text"):
            return resp.output_text
        raise RuntimeError("OpenAI response did not contain text")