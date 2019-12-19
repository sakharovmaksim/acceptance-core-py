import os


def get_base_url() -> str:
    base_url = os.environ["HOST_URL"]
    if not base_url:
        raise Exception("Could not get value for variable HOST_URL from ENV")

    return base_url
