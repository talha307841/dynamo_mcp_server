from __future__ import annotations
import os
from datetime import datetime, time as dtime
from typing import List
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import pytz
from .registry import ToolRegistry
from .codegen import ensure_tool as codegen_ensure_tool
load_dotenv()
mcp = FastMCP("GMCP — Generalized Self-Extending Server")
def _parse_business_hours(s: str) -> tuple[dtime, dtime]:
    start_s, end_s = s.split("-")
    hs = list(map(int, start_s.split(":")))
    he = list(map(int, end_s.split(":")))
    return dtime(hs[0], hs[1]), dtime(he[0], he[1])
@mcp.tool(schema={
    "name": "time.get_time",
    "description": "Get current local time for a given IANA timezone (e.g., Asia/Karachi)",
    "inputSchema": {"type": "object", "properties": {"timezone": {"type": "string"}}, "required": ["timezone"]}
})
def get_time(timezone: str) -> dict:
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    return {"timezone": timezone, "current_time": now.isoformat()}
@mcp.tool(schema={
    "name": "time.convert_time",
    "description": "Convert a time between timezones (format: YYYY-MM-DD HH:MM:SS)",
    "inputSchema": {"type": "object", "properties": {
        "time": {"type": "string"},
        "from_tz": {"type": "string"},
        "to_tz": {"type": "string"}
    }, "required": ["time", "from_tz", "to_tz"]}
})
def convert_time(time: str, from_tz: str, to_tz: str) -> dict:
    src = pytz.timezone(from_tz)
    tgt = pytz.timezone(to_tz)
    naive = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    local_dt = src.localize(naive)
    target = local_dt.astimezone(tgt)
    return {
        "original_time": time,
        "from_timezone": from_tz,
        "to_timezone": to_tz,
        "converted_time": target.strftime("%Y-%m-%d %H:%M:%S")
    }
@mcp.tool(schema={
    "name": "time.suggest_call_window",
    "description": "Suggest overlap windows for business hours across locations.",
    "inputSchema": {"type": "object", "properties": {
        "locations": {"type": "array", "items": {"type": "string"}},
        "business_hours": {"type": "string", "default": "09:00-18:00"}
    }, "required": ["locations"]}
})
def suggest_call_window(locations: List[str], business_hours: str = "09:00-18:00") -> dict:
    start, end = _parse_business_hours(business_hours)
    tz_objs = [pytz.timezone(l) for l in locations]
    base = datetime.now(tz_objs[0]).replace(minute=0, second=0, microsecond=0)
    candidates = []
    for h in range(0, 24):
        t0 = base.replace(hour=h)
        ok = True
        local_times = []
        for tz in tz_objs:
            lt = t0.astimezone(tz)
            if not (start <= lt.time() <= end):
                ok = False
                break
            local_times.append({"tz": tz.zone, "time": lt.strftime("%Y-%m-%d %H:%M")})
        if ok:
            candidates.append(local_times)
    return {"windows": candidates[:5], "note": "Top 5 hourly windows that are within local business hours for all participants."}
registry = ToolRegistry()
@mcp.tool(schema={
    "name": "meta.ensure_tool",
    "description": "Ensure a tool exists by name; if missing, generate it via LLM to the given spec and load it.",
    "inputSchema": {"type": "object", "properties": {
        "name": {"type": "string"},
        "spec": {"type": "object", "description": "High-level description incl. inputSchema, outputSchema, and requirements."}
    }, "required": ["name", "spec"]}
})
def ensure_tool(name: str, spec: dict) -> dict:
    if registry.has(name):
        return {"status": "exists", "name": name}
    path = codegen_ensure_tool(name, spec)
    loaded = registry.load_tool_module(path)
    return {"status": "created", "name": name, "module": loaded.__name__}
if __name__ == "__main__":
    import sys
    mode = (sys.argv[1] if len(sys.argv) > 1 else "stdio").lower()
    if mode == "http":
        from starlette.applications import Starlette
        from starlette.routing import Mount
        import uvicorn
        mcp.settings.streamable_http_path = "/mcp"
        app = Starlette(routes=[
            Mount("/", app=mcp.streamable_http_app()),
        ])
        host = os.getenv("GMCP_HTTP_HOST", "0.0.0.0")
        port = int(os.getenv("GMCP_HTTP_PORT", "8288"))
        uvicorn.run(app, host=host, port=port)
    else:
        import mcp.server.stdio
        mcp.run(transport="stdio")