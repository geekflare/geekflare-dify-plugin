from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils import invoke, normalize_url

# check -> (endpoint path, accepts followRedirect)
CHECKS: dict[str, str] = {
    "site_status": "up",
    "dns_records": "dnsrecord",
    "tls_scan": "tlsscan",
    "redirect_check": "redirectcheck",
    "broken_links": "brokenlink",
    "load_time": "loadtime",
    "lighthouse": "lighthouse",
}


class GeekflareSiteCheckTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        check = tool_parameters.get("check") or "site_status"
        if check not in CHECKS:
            yield self.create_text_message(f"Unknown check '{check}'. Use one of: {', '.join(CHECKS)}.")
            return
        yield from invoke(self, CHECKS[check], {"url": normalize_url(tool_parameters.get("url", ""))})
