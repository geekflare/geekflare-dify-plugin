from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.utils import GeekflareAPIError, call_api


class GeekflareProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = credentials.get("geekflare_api_key")
        if not api_key:
            raise ToolProviderCredentialValidationError("Geekflare API key is missing.")
        try:
            # A single A-record lookup is the cheapest authenticated call.
            call_api(api_key, "dnsrecord", {"url": "https://example.com", "types": ["A"]})
        except GeekflareAPIError as e:
            raise ToolProviderCredentialValidationError(str(e)) from e
