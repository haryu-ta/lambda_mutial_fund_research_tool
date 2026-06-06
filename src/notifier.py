import os
from datetime import datetime
from typing import List
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage
)
from .models import FundData

class LineNotifier:
    def __init__(self, channel_access_token: str = None, user_id: str = None):
        self.channel_access_token = channel_access_token or os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        self.user_id = user_id or os.getenv("LINE_USER_ID")
        
        if self.channel_access_token:
            self.configuration = Configuration(access_token=self.channel_access_token)
        else:
            self.configuration = None

    def format_message(self, funds: List[FundData]) -> str:
        today = datetime.now().strftime("%Y/%m/%d")
        lines = [f"{today} 基準値"]
        
        for fund in funds:
            if fund.is_success:
                change_str = f"{fund.change:+}" if fund.change is not None else "0"
                lines.append(f"{fund.name} {fund.price:,}円 {change_str}円")
            else:
                lines.append(f"{fund.name} 取得なし")
                
        return "\n".join(lines)

    def notify(self, message: str) -> bool:
        if not self.configuration or not self.user_id:
            print("LINE configuration or User ID missing.")
            return False
            
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            push_message_request = PushMessageRequest(
                to=self.user_id,
                messages=[TextMessage(text=message)]
            )
            try:
                line_bot_api.push_message(push_message_request)
                return True
            except Exception as e:
                print(f"Error sending LINE notification: {e}")
                return False
