import pytest
from src.scraper import YahooFinanceScraper
from src.models import FundRequest

@pytest.fixture
def scraper():
    return YahooFinanceScraper()

def test_generate_url(scraper):
    request = FundRequest(id="8931123C", display_name="Sample Fund")
    url = scraper.generate_url(request)
    assert url == "https://finance.yahoo.co.jp/quote/8931123C"

def test_parse_html_success(scraper):
    html = """
    <html>
        <body>
            <span class="PriceBoard__value__o0f7">28,512</span>
            <span class="DailyChange__value__2E63">+123</span>
        </body>
    </html>
    """
    data = scraper.parse_html(html, "Sample Fund")
    assert data.name == "Sample Fund"
    assert data.price == 28512
    assert data.change == 123
    assert data.is_success is True

def test_parse_html_failure(scraper):
    html = "<html><body>Error</body></html>"
    data = scraper.parse_html(html, "Sample Fund")
    assert data.name == "Sample Fund"
    assert data.is_success is False
    assert data.price is None
