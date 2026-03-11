# fetch_data.py
from typing import List
from asset_data import AssetData
from fetch_yfinance import fetch_data, get_price, get_fx_to_thb, get_52_week_high, get_52_week_low, get_trailing_pe, get_trailing_dividend_yield

def can_fetch_data() -> bool:
    return fetch_data()

def enrich_asset(asset: AssetData) -> AssetData:
    """
    Fetch price and fx_rate for an asset and compute its values.
    """
    # FX rate
    if asset.currency == 'THB':
        asset.fx_rate = 1
    else:
        asset.fx_rate = get_fx_to_thb(asset.currency)

    # Price handling
    if asset.symbol == 'CASH':
        asset.price = 1
    elif asset.symbol == 'BOND':
        pass  # Use user-assigned value
    elif asset.symbol == 'FUNDTH':
        pass  # Use user-assigned value
    else:
        asset.price = get_price(asset.symbol)
        asset.high_52w = get_52_week_high(asset.symbol)
        asset.low_52w = get_52_week_low(asset.symbol)
        asset.pe_ratio = get_trailing_pe(asset.symbol)
        asset.dividend_yield = get_trailing_dividend_yield(asset.symbol)

    return asset


def enrich_assets(assets: List[AssetData]) -> List[AssetData]:
    return [enrich_asset(asset) for asset in assets]
