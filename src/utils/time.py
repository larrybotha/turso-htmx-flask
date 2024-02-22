from datetime import datetime


def get_current_time():
    return datetime.now()


def get_current_time_in_seconds():
    return int(float((get_current_time() - datetime(1970, 1, 1)).total_seconds()))
