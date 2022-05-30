import datetime


def year(request):
    """Adds a variable with the current year."""
    date = datetime.datetime.now()
    actual_year = str(date.year)
    return {
        'year': actual_year,
    }
