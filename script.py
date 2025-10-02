import requests
import time
import snowflake.connector
from datetime import datetime
import os
import logging
from dotenv import load_dotenv

# Create a 'logs' folder inside your project if it doesn't exist
LOG_DIR = r"C:\Users\farah\Dev\stock-trading-python-app\logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "stock_app.log")

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logging.info("Logging started")

# === Load environment variables from .env ===
try:
    load_dotenv(dotenv_path=r"C:\Users\farah\Dev\stock-trading-python-app\.env")
    logging.info(".env file loaded successfully.")
except Exception as e:
    logging.error(f" Failed to load .env file: {e}")

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
LIMIT = 1000
DS = datetime.now().strftime('%Y-%m-%d')

def run_stock_job():
    tickers = []

    url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        logging.error(f" Failed to fetch initial tickers: {e}")
        return

    for ticker in data.get('results', []):
        ticker['ds'] = DS
        tickers.append(ticker)

    while 'next_url' in data:
        next_url = data['next_url']
        logging.info(f"Requesting next page: {next_url}")
        time.sleep(15)
        try:
            response = requests.get(next_url + f"&apiKey={POLYGON_API_KEY}")
            data = response.json()
        except Exception as e:
            logging.error(f"Failed to fetch next page: {e}")
            break

        for ticker in data.get('results', []):
            ticker['ds'] = DS
            tickers.append(ticker)

    logging.info(f"Fetched {len(tickers)} tickers from Polygon API.")

    # Determine schema from example
    example_ticker = tickers[0] if tickers else {}
    fieldnames = list(example_ticker.keys())

    load_to_snowflake(tickers, fieldnames)

def load_to_snowflake(rows, fieldnames):
    if not rows:
        logging.warning("No rows to insert into Snowflake.")
        return

    try:
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA'),
            role=os.getenv('SNOWFLAKE_ROLE'),
            session_parameters={"CLIENT_TELEMETRY_ENABLED": False},
        )
        cs = conn.cursor()

        # Test connection
        cs.execute("SELECT CURRENT_TIMESTAMP")
        server_time = cs.fetchone()[0]
        logging.info(f"Snowflake connection OK, server time: {server_time}")

        table_name = os.getenv('SNOWFLAKE_TABLE', 'stock_tickers')

        # Create table if not exists
        type_overrides = {
            'ticker': 'VARCHAR',
            'name': 'VARCHAR',
            'market': 'VARCHAR',
            'locale': 'VARCHAR',
            'primary_exchange': 'VARCHAR',
            'type': 'VARCHAR',
            'active': 'BOOLEAN',
            'currency_name': 'VARCHAR',
            'cik': 'VARCHAR',
            'composite_figi': 'VARCHAR',
            'share_class_figi': 'VARCHAR',
            'last_updated_utc': 'TIMESTAMP_NTZ',   
            'ds': 'VARCHAR'
        }
        columns_sql_parts = [f'"{col.upper()}" {type_overrides.get(col,"VARCHAR")}' for col in fieldnames]
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} (' + ', '.join(columns_sql_parts) + ')'
        cs.execute(create_table_sql)

        # Insert rows
        column_list = ', '.join([f'"{c.upper()}"' for c in fieldnames])
        placeholders = ', '.join([f'%({c})s' for c in fieldnames])
        insert_sql = f'INSERT INTO {table_name} ({column_list}) VALUES ({placeholders})'

        transformed = [{k: t.get(k, None) for k in fieldnames} for t in rows]

        if transformed:
            cs.executemany(insert_sql, transformed)
            conn.commit()
            logging.info(f"Inserted {len(transformed)} rows into {table_name}.")

        cs.close()
        conn.close()

    except Exception as e:
        logging.error(f"Snowflake load failed: {e}")
        raise

if __name__ == '__main__':
    run_stock_job()
    logging.info("=== Script finished ===")



# Write tickers to CSV with example_ticker schema
   
    # output_csv = 'tickers.csv'
    # with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for t in tickers:
    #         row = {key: t.get(key, '') for key in fieldnames}
    #         writer.writerow(row)
    # print(f'Wrote {len(tickers)} rows to {output_csv}')






