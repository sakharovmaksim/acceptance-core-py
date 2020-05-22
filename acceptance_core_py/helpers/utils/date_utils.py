import logging
import time
from calendar import timegm
from datetime import datetime
from time import strptime

from dateutil.relativedelta import relativedelta


def generate_date(relative_delta: int = +0, delta_type: str = "days", format_date: str = "%d.%m.%Y") -> str:
    date_now = datetime.now()

    if delta_type == "days":
        date = date_now + relativedelta(days=relative_delta)
    elif delta_type == "weeks":
        date = date_now + relativedelta(weeks=relative_delta)
    elif delta_type == "months":
        date = date_now + relativedelta(months=relative_delta)
    elif delta_type == "years":
        date = date_now + relativedelta(years=relative_delta)
    else:
        logging.error(f"Set correct delta_type argument, given '{delta_type}'. Set to 'days'")
        date = date_now + relativedelta(days=relative_delta)

    date = date.strftime(format_date)
    logging.info(f"Generate date '{date}' with delta_type '{delta_type}' and relative_delta '{str(relative_delta)}'")
    return date

def generate_timestamp() -> float:
    """Return like: 1585818190.7445524"""
    timestamp = time.time()
    logging.info(f"Generated timestamp '{str(timestamp)}'")
    return timestamp


def convert_to_timestamp(date_to_convert: str, directive_format: str = '%d.%m.%Y') -> int:
    """Convert a date in int timestamp, return like: 976579200"""
    date_timestamp = int(timegm(strptime(date_to_convert, directive_format)))
    logging.info(f"Convert date {date_to_convert} to timestamp '{date_timestamp}'")
    return date_timestamp
