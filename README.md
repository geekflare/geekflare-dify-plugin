# Geekflare plugin for Dify

**Author:** [Geekflare](https://geekflare.com)
**Version:** 0.0.1
**Type:** tool
**Source repository:** https://github.com/geekflare/geekflare-dify-plugin
**Contact:** support@geekflare.com

## Overview

Give Dify workflows, chatflows, and agents live web data and website checks with the [Geekflare API](https://geekflare.com):

| Tool | What it does |
| --- | --- |
| Geekflare Search | Web, news, or image search. Turn on **Full Google SERP** for the full results page (organic results, AI Overview, People Also Ask) by country or city |
| Geekflare Scrape URL | Page content as Markdown, text, HTML, or JSON, with optional `product` or `contact` templates for structured data |
| Geekflare Page Metadata | Title, description, canonical URL, Open Graph, and Twitter Card tags |
| Geekflare Brand | Logos, brand colors, fonts, and social profiles for a website |
| Geekflare Screenshot | Viewport or full-page screenshot as a hosted image URL |
| Geekflare URL to PDF | Page as PDF, returned as a hosted download URL |
| Geekflare Website Check | Uptime, DNS records, TLS/SSL, redirect chain, broken links, load time, or a Lighthouse audit |

Every tool returns the API response as JSON.

## Setup

1. Get an API key at [dash.geekflare.com](https://dash.geekflare.com). A free tier is available.
2. In Dify, install **Geekflare** from the Marketplace (**Plugins → Marketplace**).
3. Open the plugin, click **Authorize**, and paste your API key. Dify checks the key with a single DNS lookup.

Requirements: a Geekflare API key and outbound HTTPS access from your Dify instance to `api.geekflare.com`.

## Usage

- **Agent or chatflow:** add the Geekflare tools you need to an Agent node. For example, ask "What does Google show for 'best crm' in London? Cite sources." and the agent calls Geekflare Search with SERP on.
- **Workflow:** add a tool node such as **Geekflare Scrape URL**, pass a URL from an earlier node, and use the returned Markdown in an LLM node.
- **Website monitoring:** use **Geekflare Website Check** with `check = tls_scan` or `site_status` in a scheduled workflow to report certificate expiry or downtime.

URLs can be full URLs or bare domains such as `example.com`. Use the tools for publicly accessible pages only.

## Pricing

Each call uses Geekflare credits on your account. See [pricing](https://geekflare.com/pricing/).

## Privacy

See [PRIVACY.md](PRIVACY.md). Inputs are sent to `api.geekflare.com` to fulfill each request; the plugin stores nothing.

## Support

Email support@geekflare.com or open an issue at https://github.com/geekflare/geekflare-dify-plugin/issues.
