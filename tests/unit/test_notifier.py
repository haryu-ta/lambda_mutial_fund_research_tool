import pytest
from datetime import datetime
from src.notifier import LineNotifier
from src.models import FundData

@pytest.fixture
def notifier():
    return LineNotifier(channel_access_token="test_token", user_id="test_user")

def test_format_message(notifier):
    funds = [
        FundData(name="Fund A", price=25000, change=150, is_success=True),
        FundData(name="Fund B", is_success=False)
    ]
    
    today = datetime.now().strftime("%Y/%m/%d")
    message = notifier.format_message(funds)
    
    assert f"{today} 基準値" in message
    assert "Fund A 25,000円 +150円" in message
    assert "Fund B 取得なし" in message

def test_format_message_empty(notifier):
    message = notifier.format_message([])
    today = datetime.now().strftime("%Y/%m/%d")
    assert f"{today} 基準値" in message
    assert message.strip() == f"{today} 基準値"
