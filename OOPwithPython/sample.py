import calendar

def second_saturdays(year):

    for month in range(1, 13):
        cl = calendar.monthcalendar(year, month)
        if cl[0][5]:
            print(month, ':', cl[1][5])
        else:
            print(month, ':', cl[2][5])

second_saturdays(2025)