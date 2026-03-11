# asset_data.py
from dataclasses import dataclass
from typing import Optional  # If User Leave Input Empty

@dataclass
class AssetData:
    # Google Sheet Variables
    name: str
    symbol: str
    currency: str
    shares: float
    price: Optional[float] = None
    fx_rate: Optional[float] = None
    asset_class: Optional[str] = None
    mdd: Optional[float] = None

    # Portfolio Value Variables
    value_local: Optional[float] = None
    value_thb: Optional[float] = None
    weight: Optional[float] = None

    # Price Change
    high_52w: Optional[float] = None
    low_52w: Optional[float] = None
    low_years: Optional[float] = None

    # P/E Signal
    pe_ratio: Optional[float] = None                    # Trailing P/E ratio
    pe_p25: Optional[float] = None                      # 25th percentile P/E
    pe_p75: Optional[float] = None                      # 75th percentile P/E

    # Dividend Yield Signal
    dividend_yield: Optional[float] = None              # Trailing dividend yield
