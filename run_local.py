import os
import json
from dotenv import load_dotenv
from src.lambda_function import lambda_handler

# .env から環境変数を読み込む
load_dotenv()

# テスト用のイベントデータ (EventBridge から渡される想定の形式)
test_event = [
    {"id": "0331418A", "display_name": "eMAXIS Slim 全世界株式(ｵｰﾙ･ｶﾝﾄﾘｰ)"},
    {"id": "04311181", "display_name": "iFreeNEXT FANG+インデックス"},
]

if __name__ == "__main__":
    print("--- Local Run Start ---")

    # LINE トークンが設定されていない場合は警告を表示
    if (
        not os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        or os.getenv("LINE_CHANNEL_ACCESS_TOKEN") == "your_channel_access_token_here"
    ):
        print(
            "[Warning] LINE_CHANNEL_ACCESS_TOKEN is not set. Notification will fail but scraping will be shown in console."
        )

    try:
        # Lambda ハンドラーの実行
        response = lambda_handler(test_event, None)
        print("\n--- Response ---")
        print(json.dumps(response, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"\n[Error] {e}")

    print("\n--- Local Run End ---")
