import datetime
import os

# Translate filenames encoded with date and timestamps into datetime objects
def datetimeFromFilename(filename):
    date = []
    time = []
    filename = os.path.splitext(filename)[0]
    # Translate filenames to canonical YYYYMMDD and HHMMSS form
    if filename.startswith('VID-'):
        # Type 1: VID-YYYYMMDD-WAXXXX
        date = filename.split('-')[1]
    elif filename.startswith('VID_'):
        # Type 2: VID_YYYYMMDD_HHMMSS
        dates = filename.split('_')
        time = dates[2].strip('.mp4')
        date = dates[1]
    elif filename[:4].isdigit():
        # Type 3: YYYY-MM-DD
        # OR
        # YYYY-MM-DD HH.MM.SS
        dates = filename.split(' ')
        date = dates[0].replace('-', '')
        if len(dates) > 1:
            times = dates[1]
            time = times.replace('.', '')
    elif filename[:1].isdigit():
        # Type 4: D[D]-M[M]-YYYY
        # Must be done after all other date processing
        if filename.endswith(' (2)'):
            filename = filename[:-4]
        dates = filename.split('-')
        dates = dates[::-1]
        date = "%04d%02d%02d" % tuple(map(int,dates))

    # Catch unhandled cases, default to 1900-01-01, 00:00:00
    if not time:
        time = "000000"
    if not date:
        date = "19000101"
    #print(date)
    #print(time)
    # Translate canonical YYYYMMDD and HHMMSS into date and time
    date = [int(date[:4]), int(date[4:6]), int(date[6:])]
    time = [int(time[:2]), int(time[2:4]), int(time[4:])]
          
    #print(str(date))
    #print(str(time))
    try:
        dt = datetime.datetime(date[0],
                               date[1],
                               date[2],
                               time[0],
                               time[1],
                               time[2],
                               0)
    except ValueError as err:
        raise err
    #print(str(dt))

    return dt
