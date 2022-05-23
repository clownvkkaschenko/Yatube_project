import datetime

def year(request):
    """Добавляет переменную с текущим годом."""
    ye = datetime.datetime.now()
    actual_ye = int(ye.year)
    return {
        'year': actual_ye,
    }