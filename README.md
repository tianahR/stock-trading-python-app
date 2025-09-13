
# Polygon.io Stock Tickers Exporter

This script fetches all **active U.S. stock tickers** from the [Polygon.io](https://polygon.io) API and saves them to a CSV file.  
It automatically handles pagination and includes basic error handling for API rate limits.

---

## Requirements

- Python 3.8+
- A [Polygon.io API key](https://polygon.io/pricing) (free or paid)
- Dependencies:
  ```bash
  pip install -r requirements.txt

#Setup

Clone or download this repository.

Create a .env file in the project root with your Polygon API key:
POLYGON_API_KEY=your_api_key_here

Run the script:
python script.py

Output

The script will create a file called tickers.csv in the project folder.

Each row in the CSV represents a stock ticker with fields such as:

ticker, name, market, locale, primary_exchange, type, active,
currency_name, cik, composite_figi, share_class_figi, last_updated_utc
