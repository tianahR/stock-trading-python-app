# Polygon.io Stock Tickers Exporter

This script fetches all **active U.S. stock tickers** from the [Polygon.io](https://polygon.io) API and saves them to a CSV file or a database in snowflake.  
It automatically handles pagination and includes basic error handling for API rate limits.

---

## Requirements

- Python 3.8+
- A [Polygon.io API key](https://polygon.io/pricing) (free or paid)
- Dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Setup

Clone or download this repository.

Create a .env file in the project root with your Polygon API key:
POLYGON_API_KEY=your_api_key_here
SNOWFLAKE_ACCOUNT=your_snowflake_identifier_here
SNOWFLAKE_USER=your_snowflake_username_here
SNOWFLAKE_PASSWORD=your_snowflake_password_here
SNOWFLAKE_WAREHOUSE=your_snowflake_warehouse_here
SNOWFLAKE_DATABASE=your_snowflake_database_name_here
SNOWFLAKE_SCHEMA=your_snowflake_schema_here
SNOWFLAKE_ROLE=your_snowflake_role_here

Run the script in one time:
python script.py

To schedule run time every 30 minutes ( you can change code if you want to run it every hour or daily for example) manually
python scheduler.py

To Use Windows Task Scheduler 
Task Scheduler is a built-in Windows utility that lets you automatically run programs or scripts at specific times or in response to events—basically, it schedules tasks instead of you running them manually.
Now rows are inserted in Snowflake daily automatically
run_ticker_script.bat is created

<img width="1920" height="764" alt="image" src="https://github.com/user-attachments/assets/4337f614-1a36-48b0-ac76-5e5a66d71d98" />



## Output

The script created a file called tickers.csv in the project folder.
Now it will load the row in a database in snowflake
Each row represents a stock ticker with fields such as:ticker, name, market, locale, primary_exchange, type, active,currency_name, cik, composite_figi, share_class_figi, last_updated_utc,ds

## Learning Resources

This project was inspired and guided by:

- [DataExpert.io](https://dataexpert.io) — tutorials and learning resources - The Absolutely Free Beginner Data Engineering Boot Camp
- [Zach Wilson](https://www.linkedin.com/in/eczachly/) — for insights on data engineering and software development
