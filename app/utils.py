from datetime import date, timedelta


def get_start_date(period: str):
    today = date.today()
    if period == "daily":
        return today
    elif period == "weekly":
        return today - timedelta(days=today.weekday())
    elif period == "monthly":
        return date(today.year, today.month, 1)
    elif period == "annual":
        return date(today.year, 1, 1)
