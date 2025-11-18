"""
Trading-Technical-Indicators (tti) python library

File name: download_historical_data.py
    Downloads historical data for assets.

Use as:
    python download_historical_data.py
"""

from tti.ml.data.downloaders import YahooFinanceDailyDownloader

if __name__ == "__main__":
    dl = YahooFinanceDailyDownloader()

    example_asset = "AAPL"

    try:
        # Similarly, dl.update can be use, if there are data downloaded before.
        dl.download(asset=example_asset, data_dir="./historical_data")
    except Exception as e:
        print(f"Failed to download asset {example_asset} with error {e}")
