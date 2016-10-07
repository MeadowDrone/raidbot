import datetime


def timers():
    current_date = datetime.datetime.now()
    day_of_week_now = datetime.datetime.today().weekday()

    # daily timer calculation
    extra_day_daily = 0 if current_date.hour < 11 else 1

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
    
    dhstr = " hour, " if daily_hours == 1 else " hours, "
    dmstr = " minute " if daily_minutes == 1 else " minutes, "
    dsstr = " second" if daily_seconds == 1 else " seconds"

    # weekly timer calculation
    if (day_of_week_now == 0):
        days_until_weekly = 1
    elif (day_of_week_now == 1):
        days_until_weekly = 0 if current_date.hour < 4 else 7
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
        
    wdstr = " day, " if weekly_days == 1 else " days, "
    whstr = " hour, " if weekly_hours == 1 else " hours, "
    wmstr = " minute" if weekly_minutes == 1 else " minutes"
    wsstr = " second" if weekly_seconds == 1 else " seconds"

    # scrip reset calculation
    if (day_of_week_now == 0):
        days_until_scrip = 3
    elif (day_of_week_now == 1):
        days_until_scrip = 2
    elif (day_of_week_now == 2):
        days_until_scrip = 1
    elif (day_of_week_now == 3):
        days_until_scrip = 0 if current_date.hour < 4 else 7
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
    
    sdstr = " day, " if scrip_days == 1 else " days, "
    shstr = " hour, " if scrip_hours == 1 else " hours, "
    smstr = " minute" if scrip_minutes == 1 else " minutes"
    ssstr = " second" if scrip_seconds == 1 else " seconds"

    # return results
    if (weekly_days == 0):
        timer = "%s%s%s%s and %s%s until daily reset\n" % (
            str(daily_hours), dhstr, str(daily_minutes), dmstr, str(daily_seconds), dsstr)
        timer += "%s%s%s%s and %s%s until weekly reset\n" % (
            str(weekly_hours), whstr, str(weekly_minutes), wmstr, str(weekly_seconds), wsstr)
        timer += "%s%s%s%s%s%s and %s%s until scrip and grand company reset" % (str(
            scrip_days), sdstr, str(scrip_hours), shstr, str(scrip_minutes), smstr, str(scrip_seconds), ssstr)
    elif (scrip_delta.days == 0):
        timer = "%s%s%s%s and %s%s until daily reset\n" % (
            str(daily_hours), dhstr, str(daily_minutes), dmstr, str(daily_seconds), dsstr)
        timer += "%s%s%s%s%s%s and %s%s until weekly reset\n" % (str(weekly_days), wdstr, str(
            weekly_hours), whstr, str(weekly_minutes), wmstr, str(weekly_seconds), wsstr)
        timer += "%s%s%s%s%s and %s%s until scrip and grand company reset" % (str(scrip_days), sdstr, str(
            scrip_hours), shstr, str(scrip_minutes), smstr, str(scrip_seconds), ssstr)
    else:
        timer = "%s%s%s%s and %s%s until daily reset\n" % (
            str(daily_hours), dhstr, str(daily_minutes), dmstr, str(daily_seconds), dsstr)
        timer += "%s%s%s%s%s%s and %s%s until weekly reset\n" % (str(weekly_days), wdstr, str(
            weekly_hours), whstr, str(weekly_minutes), wmstr, str(weekly_seconds), wsstr)
        timer += "%s%s%s%s%s%s and %s%s until scrip and grand company reset" % (str(
            scrip_days), sdstr, str(scrip_hours), shstr, str(scrip_minutes), smstr, str(scrip_seconds), ssstr)

    return timer
