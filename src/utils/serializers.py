import datetime as dt

def signed_timestamp(timestamp: float) -> str:
    time_signature = dt.datetime.fromtimestamp(timestamp)

    if time_signature.date() != dt.datetime.now().date():
        time_signature = time_signature.strftime('%a %b-%d-%Y %H:%M')
    else:
        time_signature = 'Today ' + time_signature.strftime('%H:%M')

    return time_signature
