from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

API_BASE_URL = "https://api.geekflare.com"
REQUEST_TIMEOUT = 180


class GeekflareAPIError(Exception):
    """Raised when the Geekflare API returns an error or can't be reached."""


def call_api(api_key: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
    """POST a JSON body to a Geekflare endpoint and return the parsed response."""
    body = {k: v for k, v in payload.items() if v is not None and v != ""}
    try:
        response = requests.post(
            f"{API_BASE_URL}/{path}",
            json=body,
            headers={"x-api-key": api_key, "Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as e:
        raise GeekflareAPIError(f"Request to Geekflare failed: {e}") from e

    try:
        data: Any = response.json()
    except ValueError:
        data = {"message": response.text}
    if not isinstance(data, dict):
        data = {"data": data}

    if response.status_code >= 400 or data.get("apiStatus") == "failure":
        raise GeekflareAPIError(
            f"Geekflare API error ({response.status_code}): {data.get('message', 'unknown error')}"
        )
    return data


def normalize_url(url: str) -> str:
    """Accept bare domains such as example.com by adding https://."""
    url = (url or "").strip()
    if url and "://" not in url:
        url = f"https://{url}"
    return url


def invoke(tool: Tool, path: str, payload: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
    """Call the API with the provider's key and yield the JSON result, or a text error."""
    api_key = tool.runtime.credentials.get("geekflare_api_key", "")
    try:
        yield tool.create_json_message(call_api(api_key, path, payload))
    except GeekflareAPIError as e:
        yield tool.create_text_message(str(e))
