from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils import invoke, normalize_url


class GeekflareBrandTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        params = tool_parameters
        yield from invoke(self, "brand", {"url": normalize_url(params.get("url")), "mode": params.get("mode") or "standard"})
