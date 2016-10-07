import datetime


def timers():
    current_date = datetime.datetime.now()
    day_of_week_now = datetime.datetime.today().weekday()

    # daily timer calculation
    extra_day_daily = 0 if current_date.hour < 11 else 1
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
    
    dhstr = str(daily_hours) + " hour, " if daily_hours == 1 else str(daily_hours) + " hours, "
    dmstr = str(daily_minutes) + " minute " if daily_minutes == 1 else str(daily_minutes) + " minutes, "
    dsstr = str(daily_seconds) + " second" if daily_seconds == 1 else str(daily_seconds) + " seconds"

    # weekly + scrip timer calculation
    if day_of_week_now == 0:
        days_until_weekly = 1
        days_until_scrip = 3
    elif day_of_week_now == 1:
        days_until_weekly = 0 if current_date.hour < 4 else 7
        days_until_scrip = 2
    elif day_of_week_now == 2:
        days_until_weekly = 8 - day_of_week_now
        days_until_scrip = 1
    elif day_of_week_now == 3:
        days_until_weekly = 8 - day_of_week_now
        days_until_scrip = 0 if current_date.hour < 4 else 7
    else:
        days_until_weekly = 8 - day_of_week_now
        days_until_scrip = 10 - day_of_week_now

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
        
    wdstr = str(weekly_days) + " day, " if weekly_days == 1 else str(weekly_days) + " days, "
    whstr = str(weekly_hours) + " hour, " if weekly_hours == 1 else str(weekly_hours) + " hours, "
    wmstr = str(weekly_minutes) + " minute" if weekly_minutes == 1 else str(weekly_minutes) + " minutes"
    wsstr = str(weekly_seconds) + " second" if weekly_seconds == 1 else str(weekly_seconds) + " seconds"

    # get scrip seconds, minutes & hours
    scrip_hours, scrip_remainder = divmod(weekly_delta.seconds, 3600)
    scrip_minutes, scrip_seconds = divmod(scrip_remainder, 60)
    scrip_days = weekly_delta.days + days_until_scrip
    
    sdstr = str(scrip_days) + " day, " if scrip_days == 1 else str(scrip_days) + " days, "
    shstr = str(scrip_hours) + " hour, " if scrip_hours == 1 else str(scrip_hours) + " hours, "
    smstr = str(scrip_minutes) + " minute" if scrip_minutes == 1 else str(scrip_minutes) + " minutes"
    ssstr = str(scrip_seconds) + " second" if scrip_seconds == 1 else str(scrip_seconds) + " seconds"

    # return results
    timer = "%s%s and %s until daily reset\n" % (dhstr, dmstr, dsstr)
    
    if weekly_days == 0:
        timer += "%s%s and %s until weekly reset\n" % (whstr, wmstr, wsstr)
        timer += "%s%s%s and %s until scrip and grand company reset" % (sdstr, shstr, smstr, ssstr)
    elif scrip_days == 0:
        timer += "%s%s%s and %s until weekly reset\n" % (wdstr, whstr, wmstr, wsstr)
        timer += "%s%s%s and %s until scrip and grand company reset" % (sdstr, shstr, smstr, ssstr)
    else:
        timer += "%s%s%s and %s until weekly reset\n" % (wdstr, whstr, wmstr, wsstr)
        timer += "%s%s%s and %s until scrip and grand company reset" % (sdstr, shstr, smstr, ssstr)

    return timer
