from datetime import datetime

from fameio.source import FameTime

DATE_FORMAT = "%Y-%m-%d_%H:%M:%S"
GUI_DATE_FORMAT = "%Y-%m-%d_%H:%M:%S"


def get_min_fame_date_time_obj() -> object:
    date_time_str = '01/01/2000 00:00:00'

    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y %H:%M:%S')

    return date_time_obj


def convert_gui_datetime_to_fame_time(widget_datetime_text: str) -> int:
    widget_datetime_text = widget_datetime_text.replace(".", "/")

    date_time_obj = datetime.strptime(widget_datetime_text, '%d/%m/%Y %H:%M:%S')
    date_string = date_time_obj.strftime("%Y-%m-%d_%H:%M:%S")

    fame_time: int = FameTime.convert_datetime_to_fame_time_step(date_string)

    return fame_time


def convert_datetime_to_fame(fame_time_string) -> int:
    return FameTime.convert_datetime_to_fame_time_step(fame_time_string.strftime("%Y-%m-%d_%H:%M:%S"))


def convert_fame_time_to_gui_datetime(fame_time_string: int) -> object:
    datetime_string = "0"

    datetime_string = FameTime.convert_fame_time_step_to_datetime(fame_time_string)

    date_time_obj = datetime.strptime(datetime_string, GUI_DATE_FORMAT)

    return date_time_obj
