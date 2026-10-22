"""Unit tests with the HTTP layer mocked. Run: pytest tests"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from provider.geekflare import GeekflareProvider  # noqa: E402
from tools.geekflare_brand import GeekflareBrandTool  # noqa: E402
from tools.geekflare_metadata import GeekflareMetadataTool  # noqa: E402
from tools.geekflare_scrape import GeekflareScrapeTool  # noqa: E402
from tools.geekflare_screenshot import GeekflareScreenshotTool  # noqa: E402
from tools.geekflare_search import GeekflareSearchTool  # noqa: E402
from tools.geekflare_site_check import CHECKS, GeekflareSiteCheckTool  # noqa: E402
from tools.geekflare_url_to_pdf import GeekflareUrlToPdfTool  # noqa: E402

CREDENTIALS = {"geekflare_api_key": "test-key"}


def _response(status: int = 200, body: dict | None = None) -> MagicMock:
    response = MagicMock()
    response.status_code = status
    response.json.return_value = body if body is not None else {"apiStatus": "success", "data": {"ok": True}}
    return response


@pytest.fixture
def mock_post():
    with patch("tools.utils.requests.post") as post:
        post.return_value = _response()
        yield post


def _run(tool_cls, params):
    return list(tool_cls.from_credentials(CREDENTIALS).invoke(params))


def test_search(mock_post):
    messages = _run(GeekflareSearchTool, {"query": "best crm", "limit": 5, "serp": True, "city": "London,England,United Kingdom"})
    assert messages[0].type == ToolInvokeMessage.MessageType.JSON
    args, kwargs = mock_post.call_args
    assert args[0] == "https://api.geekflare.com/search"
    assert kwargs["headers"]["x-api-key"] == "test-key"
    assert kwargs["json"] == {"query": "best crm", "limit": 5, "city": "London,England,United Kingdom", "serp": True}


def test_scrape_template_and_bare_domain(mock_post):
    _run(GeekflareScrapeTool, {"url": "example.com", "format": "markdown-llm", "template": "product"})
    args, kwargs = mock_post.call_args
    assert args[0] == "https://api.geekflare.com/webscraping"
    assert kwargs["json"] == {
        "url": "https://example.com",
        "format": ["markdown-llm"],
        "template": "product",
        "extractionMode": "template",
    }


@pytest.mark.parametrize(
    ("tool_cls", "params", "path"),
    [
        (GeekflareMetadataTool, {"url": "https://example.com"}, "metascraping"),
        (GeekflareBrandTool, {"url": "stripe.com", "mode": "enriched"}, "brand"),
        (GeekflareScreenshotTool, {"url": "https://example.com", "full_page": True, "image_type": "webp"}, "screenshot"),
        (GeekflareUrlToPdfTool, {"url": "https://example.com", "paper_format": "letter"}, "url2pdf"),
    ],
)
def test_content_tools_route(mock_post, tool_cls, params, path):
    _run(tool_cls, params)
    args, kwargs = mock_post.call_args
    assert args[0] == f"https://api.geekflare.com/{path}"
    assert kwargs["json"]["url"].startswith("https://")


@pytest.mark.parametrize(("check", "path"), list(CHECKS.items()))
def test_site_check_routes(mock_post, check, path):
    _run(GeekflareSiteCheckTool, {"url": "example.com", "check": check})
    args, kwargs = mock_post.call_args
    assert args[0] == f"https://api.geekflare.com/{path}"
    assert kwargs["json"] == {"url": "https://example.com"}


def test_site_check_unknown_check(mock_post):
    messages = _run(GeekflareSiteCheckTool, {"url": "example.com", "check": "nope"})
    assert messages[0].type == ToolInvokeMessage.MessageType.TEXT
    mock_post.assert_not_called()


def test_api_error_becomes_text_message(mock_post):
    mock_post.return_value = _response(401, {"apiCode": 401, "message": "Invalid x-api-key"})
    messages = _run(GeekflareSearchTool, {"query": "x"})
    assert messages[0].type == ToolInvokeMessage.MessageType.TEXT
    assert "Invalid x-api-key" in messages[0].message.text


def test_provider_validates_key(mock_post):
    GeekflareProvider()._validate_credentials(CREDENTIALS)
    args, kwargs = mock_post.call_args
    assert args[0] == "https://api.geekflare.com/dnsrecord"


def test_provider_rejects_bad_key(mock_post):
    mock_post.return_value = _response(401, {"apiCode": 401, "message": "Invalid x-api-key"})
    with pytest.raises(ToolProviderCredentialValidationError, match="Invalid x-api-key"):
        GeekflareProvider()._validate_credentials(CREDENTIALS)


def test_provider_requires_key():
    with pytest.raises(ToolProviderCredentialValidationError, match="missing"):
        GeekflareProvider()._validate_credentials({})
