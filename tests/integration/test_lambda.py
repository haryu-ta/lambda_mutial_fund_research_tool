import json
import pytest
from unittest.mock import patch, MagicMock
from src.lambda_function import lambda_handler

@pytest.fixture
def mock_event():
    return [
        {"id": "8931123C", "display_name": "Fund A"},
        {"id": "03311187", "display_name": "Fund B"}
    ]

@patch("src.scraper.urllib.request.urlopen")
@patch("src.notifier.MessagingApi")
@patch.dict("os.environ", {"LINE_CHANNEL_ACCESS_TOKEN": "dummy_token", "LINE_USER_ID": "dummy_user"})
def test_lambda_handler_success(mock_messaging_api, mock_urlopen, mock_event):
    # Mock scraper response
    mock_response = MagicMock()
    mock_response.read.return_value = b"""
    <html>
        <body>
            <span class="_3rXWJK9f">25,000</span>
            <span class="_3rXWJK9f">+150</span>
        </body>
    </html>
    """
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response

    # Mock MessagingApi instance
    mock_api_instance = mock_messaging_api.return_value

    # Execute handler
    context = MagicMock()
    response = lambda_handler(mock_event, context)

    assert response['statusCode'] == 200
    assert mock_api_instance.push_message.called
    
    # Check if push_message was called with correct data
    args, _ = mock_api_instance.push_message.call_args
    push_request = args[0]
    message = push_request.messages[0].text
    assert "Fund A 25,000円 +150円" in message
    assert "Fund B 25,000円 +150円" in message

@patch("src.scraper.urllib.request.urlopen")
@patch("src.notifier.MessagingApi")
@patch.dict("os.environ", {"LINE_CHANNEL_ACCESS_TOKEN": "dummy_token", "LINE_USER_ID": "dummy_user"})
def test_lambda_handler_partial_failure(mock_messaging_api, mock_urlopen, mock_event):
    # Mock scraper to fail for one and succeed for another
    def side_effect(req):
        if "03311187" in req.full_url:
            raise Exception("Scrape failed")
        mock_response = MagicMock()
        mock_response.read.return_value = b'<span class="_3rXWJK9f">10,000</span><span class="_3rXWJK9f">-50</span>'
        mock_response.__enter__.return_value = mock_response
        return mock_response

    mock_urlopen.side_effect = side_effect
    mock_api_instance = mock_messaging_api.return_value

    # Execute handler
    context = MagicMock()
    response = lambda_handler(mock_event, context)

    assert response['statusCode'] == 200
    
    args, _ = mock_api_instance.push_message.call_args
    message = args[0].messages[0].text
    assert "Fund A 10,000円 -50円" in message
    assert "Fund B 取得なし" in message
