from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils import invoke


class GeekflareSearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        params = tool_parameters
        yield from invoke(self, "search", {"query": params.get("query"), "limit": int(params["limit"]) if params.get("limit") else None, "source": params.get("source"), "location": params.get("location"), "city": params.get("city"), "time": params.get("time"), "serp": bool(params.get("serp", False))})
