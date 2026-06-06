from dataclasses import dataclass
from typing import Optional

@dataclass
class FundRequest:
    id: str  # 8-character alphanumeric Yahoo! Finance fund ID
    display_name: str

@dataclass
class FundData:
    name: str
    price: Optional[int] = None
    change: Optional[int] = None
    is_success: bool = False
    timestamp: Optional[str] = None
