# Research: Mutual Fund LINE Notifier

## Decision: Yahoo! Finance Scraping
- **Findings**: Yahoo! Finance investment fund pages follow the pattern `https://finance.yahoo.co.jp/quote/[ID]`. For example, `8931123C` would be `https://finance.yahoo.co.jp/quote/8931123C`.
- **Rationale**: Direct URL access via ID is reliable. The ID format is alphanumeric 8 characters as clarified.
- **Implementation**: Use `urllib.request` to fetch HTML and `BeautifulSoup4` to parse the price and daily change.
- **Price Element**: Usually found in a specific `span` or `div` with a class related to "price" or "fund".

## Decision: LINE Messaging API
- **Findings**: `line-bot-sdk` provides `PushMessageRequest` and `MessagingApi.push_message` (v3).
- **Rationale**: Official SDK simplifies authentication and request construction.
- **Authentication**: Requires `Channel Access Token` and `User ID`. Both will be stored in environment variables.

## Decision: EventBridge Trigger Format
- **Findings**: EventBridge can pass a custom JSON payload.
- **Payload Schema**:
  ```json
  [
    {"id": "8931123C", "display_name": "Sample Fund A"},
    {"id": "12345678", "display_name": "Sample Fund B"}
  ]
  ```
- **Rationale**: Matches FR-001 requirement.

## Alternatives Considered
- **Alternative**: Using Selenium for scraping.
- **Rejected**: Too heavy for Lambda, slow, and Yahoo! Finance doesn't strictly require JS rendering for basic price data.
