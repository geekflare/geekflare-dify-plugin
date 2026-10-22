# Privacy Policy

This privacy policy covers the Geekflare plugin for Dify.

## What the plugin sends

When a workflow, chatflow, or agent runs a Geekflare tool, the plugin sends the tool's inputs to the Geekflare API at `https://api.geekflare.com` over HTTPS. Inputs include search queries, URLs or domains, and options such as output format or device. The plugin also sends your Geekflare API key in the `x-api-key` request header to authenticate the call. No other third party receives this data.

## What the plugin collects, stores, or logs

The plugin itself does not collect, store, persist, or log any user data. It holds no database, writes no files, and keeps nothing between runs. Your API key is stored by Dify as an encrypted provider credential, not by the plugin.

## What Geekflare does with the data

Geekflare processes requests to return results and may log request metadata, such as the endpoint, timestamp, and account, for billing, rate limiting, and abuse prevention. Retention and handling are described in the Geekflare privacy policy: https://geekflare.com/privacy/

## Contact

Questions about this policy: support@geekflare.com
