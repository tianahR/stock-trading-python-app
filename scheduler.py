import schedule
import time
from script import run_stock_job

from datetime import datetime

def basic_job():
    print("Job started at:", datetime.now())


# Run every minute
schedule.every().minute.do(basic_job)
# Run every 30 minutes
schedule.every(30).minutes.do(run_stock_job)

# '''
# schedule.every(10).minutes.do(run_stock_job)
# schedule.every().hour.do(run_stock_job)
# schedule.every().day.at("10:30").do(run_stock_job)
# schedule.every().monday.do(run_stock_job)
# schedule.every().wednesday.at("13:15").do(run_stock_job)
# schedule.every().day.at("12:42", "Europe/Amsterdam").do(run_stock_job)
# schedule.every().minute.at(":17").do(run_stock_job)
# '''



while True:
    schedule.run_pending()
    time.sleep(1)