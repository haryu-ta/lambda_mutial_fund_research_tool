import json
from .models import FundRequest
from .scraper import YahooFinanceScraper
from .notifier import LineNotifier

def lambda_handler(event, context):
    """
    AWS Lambda Handler
    event: List of dicts with 'id' and 'display_name'
    """
    print(f"Received event: {json.dumps(event)}")
    
    # 1. Parse EventBridge Input (FR-001)
    # EventBridge typically passes the custom JSON directly as 'event'
    try:
        fund_requests = [
            FundRequest(id=item['id'], display_name=item['display_name'])
            for item in event
        ]
    except (KeyError, TypeError) as e:
        error_msg = f"Invalid input format: {e}"
        print(error_msg)
        raise Exception(error_msg)

    # 2. Scrape Data
    scraper = YahooFinanceScraper()
    results = []
    for request in fund_requests:
        print(f"Processing {request.display_name} ({request.id})...")
        data = scraper.fetch_and_parse(request)
        results.append(data)

    # 3. Format and Notify
    notifier = LineNotifier()
    message = notifier.format_message(results)
    print(f"Sending notification:\n{message}")
    
    success = notifier.notify(message)
    
    if not success:
        # If notification fails, we might want to throw an exception to retry or alert (FR-005)
        raise Exception("Failed to send LINE notification")

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Notification sent successfully'})
    }
