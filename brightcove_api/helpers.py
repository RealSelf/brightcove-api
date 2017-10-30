from datetime import date
import time

def tidy_dates(params):
    """ Convert any date objects to a date string """

    date_keys = ("from_date", "to_date", "date")
    for date_key in date_keys:
        if date_key in params:
            if isinstance(params[date_key], date):
                date_obj = params[date_key]
                params[date_key] = date_obj.strftime("%Y-%m-%d")

    return params

def handle_leap_year(t):
	"""given a time struct, give the number of days in February for that year"""
	return (29 if t.tm_year % 4 == 0 else 28)

def month_days(t):
	"""given a time struct, give the number of days in the month"""
	mnth = time.strftime("%b",t)
	months = {
		"Jan":31,
		"Feb":handle_leap_year(t),
		"Mar":31,
		"Apr":30,
		"May":31,
		"Jun":30,
		"Jul":31,
		"Aug":31,
		"Sep":30,
		"Oct":31,
		"Nov":30,
		"Dec":31
	}
	return months[mnth]

def get_yesterday_string():
	day_seconds = 86400
	yesterday = time.localtime(time.time() - day_seconds)
	return time.strftime("%Y-%m-%d",yesterday)

def get_end_of_last_month():
	tk = time.localtime()
	tk = time.localtime(time.mktime(time.localtime()) - (tk.tm_mday * 86400))
	return time.strftime("%Y-%m-%d",tk)