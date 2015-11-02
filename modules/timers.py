import datetime

def timers():
    current_date = datetime.datetime.now()
    day_of_week_now = datetime.datetime.today().weekday()
    
    # daily timer calculation 
    if (current_date.hour < 11):
        extra_day_daily = 0
    else:
        extra_day_daily = 1

    daily_timer = datetime.datetime(
            current_date.year,
            current_date.month,
            current_date.day + extra_day_daily,
            11,
            0,
            0)

    daily_delta = daily_timer - current_date

    # get daily seconds, minutes & hours
    daily_hours, daily_remainder = divmod(daily_delta.seconds, 3600)
    daily_minutes, daily_seconds = divmod(daily_remainder, 60)

    if (daily_hours == 1): dhstr = ' hour, '
    else: dhstr = ' hours, '
    if (daily_minutes == 1): dmstr = ' minute'
    else: dmstr = ' minutes'
    if (daily_seconds == 1): dsstr = ' second'
    else: dsstr = ' seconds'

    # weekly timer calculation
    if (day_of_week_now == 0):
        days_until_weekly = 1
    elif (day_of_week_now == 1):
        if (current_date.hour < 4):
            days_until_weekly = 0
        else:
            days_until_weekly = 7
    else:
        days_until_weekly = 7 - day_of_week_now

    weekly_timer = datetime.datetime(
            current_date.year,
            current_date.month,
            current_date.day,
            4,
            0,
            0)

    weekly_delta = weekly_timer - current_date

    # get weekly seconds, minutes & hours
    weekly_hours, weekly_remainder = divmod(weekly_delta.seconds, 3600)
    weekly_minutes, weekly_seconds = divmod(weekly_remainder, 60)
    weekly_days = weekly_delta.days + days_until_weekly

    if (weekly_days == 1): wdstr = ' day, '
    else: wdstr = ' days, '
    if (weekly_hours == 1): whstr = ' hour, '
    else: whstr = ' hours, '
    if (weekly_minutes == 1): wmstr = ' minute'
    else: wmstr = ' minutes'
    if (weekly_seconds == 1): wsstr = ' second'
    else: wsstr = ' seconds'

    # scrip reset calculation
    if (day_of_week_now == 0):
            days_until_scrip = 3
    elif (day_of_week_now == 1):
        days_until_scrip = 2
    elif (day_of_week_now == 2):
        days_until_scrip = 1
    elif (day_of_week_now == 3):
        if (current_date.hour < 4):
            days_until_scrip = 0
        else:
            days_until_scrip = 7
    else:
        days_until_scrip = 9 - day_of_week_now

    scrip_timer = datetime.datetime(
            current_date.year,
            current_date.month,
            current_date.day,
            4,
            0,
            0)
    
    scrip_delta = scrip_timer - current_date

    # get scrip seconds, minutes & hours
    scrip_hours, scrip_remainder = divmod(scrip_delta.seconds, 3600)
    scrip_minutes, scrip_seconds = divmod(scrip_remainder, 60)
    scrip_days = scrip_delta.days + days_until_scrip

    if (scrip_days == 1): sdstr = ' day, '
    else: sdstr = ' days, '
    if (scrip_hours == 1): shstr = ' hour, '
    else: shstr = ' hours, '
    if (scrip_minutes == 1): smstr = ' minute'
    else: smstr = ' minutes'
    if (scrip_seconds == 1): ssstr = ' second'
    else: ssstr = ' seconds'

    # return results
    if (weekly_days == 0):
        timer = "%s%s%s%s and %s%s until daily reset\n" % (str(daily_hours), dhstr, str(daily_minutes), dmstr, str(daily_seconds), dsstr)
        timer += "%s%s%s%s and %s%s until weekly reset\n" % (str(weekly_hours), whstr, str(weekly_minutes), wmstr, str(weekly_seconds), wsstr)
        timer += "%s%s%s%s%s%s and %s%s until scrip and grand company reset" % (str(scrip_days), sdstr, str(scrip_hours), shstr, str(scrip_minutes), smstr, str(scrip_seconds), ssstr)
    elif (scrip_delta.days == 0):
        timer = "%s%s%s%s and %s%s until daily reset\n" % (str(daily_hours), dhstr, str(daily_minutes), dmstr, str(daily_seconds), dsstr)
        timer += "%s%s%s%s%s%s and %s%s until weekly reset\n" % (str(weekly_days), wdstr, str(weekly_hours), whstr, str(weekly_minutes), wmstr, str(weekly_seconds), wsstr)
        timer += "%s%s%s%s%s and %s%s until scrip and grand company reset" % (str(scrip_days), sdstr, str(scrip_hours), shstr, str(scrip_minutes), smstr, str(scrip_seconds), ssstr)
    else:
        timer = "%s%s%s%s and %s%s until daily reset\n" % (str(daily_hours), dhstr, str(daily_minutes), dmstr, str(daily_seconds), dsstr)
        timer += "%s%s%s%s%s%s and %s%s until weekly reset\n" % (str(weekly_days), wdstr, str(weekly_hours), whstr, str(weekly_minutes), wmstr, str(weekly_seconds), wsstr)
        timer += "%s%s%s%s%s%s and %s%s until scrip and grand company reset" % (str(scrip_days), sdstr, str(scrip_hours), shstr, str(scrip_minutes), smstr, str(scrip_seconds), ssstr)

    return timer