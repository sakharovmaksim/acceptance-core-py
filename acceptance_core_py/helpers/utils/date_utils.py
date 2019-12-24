import logging
from datetime import datetime
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
