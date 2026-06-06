import urllib.request
import re
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional
from .models import FundRequest, FundData

class YahooFinanceScraper:
    BASE_URL = "https://finance.yahoo.co.jp/quote/"

    def generate_url(self, request: FundRequest) -> str:
        return f"{self.BASE_URL}{request.id}"

    def parse_html(self, html: str, display_name: str) -> FundData:
        soup = BeautifulSoup(html, "html.parser")
        data = FundData(name=display_name, timestamp=datetime.now().isoformat())
        
        try:
            # メインの価格ボードセクションを特定
            price_board = soup.select_one('section[class*="PriceBoard"]')
            
            if price_board:
                # セクション内から基準価額を探す
                price_element = price_board.select_one('span[class*="value"]')
                if price_element:
                    price_text = price_element.get_text().replace(",", "")
                    # 数値のみを抽出（不要な記号を除去）
                    price_val = re.search(r'(\d+)', price_text)
                    if price_val:
                        data.price = int(price_val.group(1))
                
                # 前日比を探す
                change_element = price_board.select_one('span[class*="DailyChange__value"]')
                if change_element:
                    change_text = change_element.get_text().replace(",", "")
                    change_val = re.search(r'([+-]?\d+)', change_text)
                    if change_val:
                        data.change = int(change_val.group(1))
            
            # フォールバック: クラス名が完全に一致しない場合 (noscript 内など)
            if data.price is None:
                # "基準価額" の直後の数値を限定的に探す
                price_match = re.search(r'基準価額.*?(\d{1,3}(?:,\d{3})+)', html)
                if price_match:
                    data.price = int(price_match.group(1).replace(",", ""))
                
                change_match = re.search(r'前日比.*?([+-]?\d{1,3}(?:,\d{3})*)', html)
                if change_match:
                    data.change = int(change_match.group(1).replace(",", "").replace("+", ""))

            if data.price is not None:
                data.is_success = True
        except (ValueError, AttributeError, IndexError, Exception) as e:
            print(f"Error parsing HTML for {display_name}: {e}")
            data.is_success = False
            
        return data

    def fetch_and_parse(self, request: FundRequest) -> FundData:
        url = self.generate_url(request)
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                html = response.read().decode("utf-8")
                return self.parse_html(html, request.display_name)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return FundData(name=request.display_name, is_success=False, timestamp=datetime.now().isoformat())
