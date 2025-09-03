from dataclasses import dataclass
from pathlib import Path
from jinja2 import Template
from .registry import ToolRegistry
from .providers.openai_provider import OpenAIProvider
try:
    from .providers.anthropic_provider import AnthropicProvider
except Exception:
    AnthropicProvider = None
PROMPT = """You are generating a single MCP tool in Python using the FastMCP API. Return ONLY valid Python code that defines exactly one @mcp.tool function with a JSON schema. The function SHOULD match the requested tool name: {{ name }} and satisfy this spec JSON: {{ spec | tojson }}"""
_registry = ToolRegistry()
def _llm_provider():
    provider_name = (os.getenv("GMCP_PROVIDER") or "openai")
    if provider_name == "openai":
        return OpenAIProvider()
    if provider_name == "anthropic" and AnthropicProvider:
        return AnthropicProvider()
    return OpenAIProvider()
def ensure_tool(name: str, spec: dict) -> Path:
    path = _registry.path_for(name)
    if path.exists():
        return path
    provider = _llm_provider()
    prompt = Template(PROMPT).render(name=name, spec=spec)
    code = provider.generate_code(prompt)
    if "@mcp.tool" not in code or name not in code:
        raise RuntimeError("Generated code missing mcp.tool decorator or tool name")
    path.write_text(code, encoding="utf-8")
    return path