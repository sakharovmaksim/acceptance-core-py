import logging
import time
from calendar import timegm
from datetime import datetime
from datetime import timedelta
from time import strptime
from typing import Dict

from dateutil.relativedelta import relativedelta

from acceptance_core_py.core.exception.at_exception import ATException


def generate_date(
    relative_delta: int = +0, delta_type: str = "days", format_date: str = "%d.%m.%Y"
) -> str:
    date = generate_datetime(relative_delta, delta_type).strftime(format_date)
    logging.info(
        f"Generate date '{date}' with delta_type '{delta_type}' and relative_delta '{str(relative_delta)}'"
    )
    return date


def generate_datetime(relative_delta: int = +0, delta_type: str = "days") -> datetime:
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
        logging.warning(
            f"Set correct delta_type argument, given '{delta_type}'. Set to 'days'"
        )
        date = date_now + relativedelta(days=relative_delta)

    logging.info(
        f"Generate date '{date}' with delta_type '{delta_type}' and relative_delta '{str(relative_delta)}'"
    )
    return date


def generate_timestamp() -> float:
    """Return like: 1585818190.7445524"""
    timestamp = time.time()
    logging.info(f"Generated timestamp '{str(timestamp)}'")
    return timestamp


def convert_to_timestamp(
    date_to_convert: str, directive_format: str = "%d.%m.%Y"
) -> int:
    """Convert a date in int timestamp, return like: 976579200"""
    date_timestamp = int(timegm(strptime(date_to_convert, directive_format)))
    logging.info(f"Convert date {date_to_convert} to timestamp '{date_timestamp}'")
    return date_timestamp


def days_from_date(days: int) -> int:
    """Возвращает дату 'сейчас +/- переданное кол-во дней'"""
    return int((datetime.now() + timedelta(days=days)).timestamp())


def get_month_eng_name_by_index(index: int) -> str:
    prepared_index = int(index)
    needed_month_name = __get_month_eng_names().get(prepared_index)
    if not needed_month_name:
        raise ATException(f"Could not find month name with {prepared_index=} in months")
    return needed_month_name


def __get_month_eng_names() -> Dict:
    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }
    return months
