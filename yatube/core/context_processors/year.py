import datetime


def year(request):
    """Adds a variable with the current year."""
    ye = datetime.datetime.now()
    actual_ye = int(ye.year)
    return {
        'year': actual_ye,
    }
