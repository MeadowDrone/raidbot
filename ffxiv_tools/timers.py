import datetime


def timers():
    """
    """
    current_date = datetime.datetime.now()
    day_of_week_now = datetime.datetime.today().weekday()
    #current_day = current_date.day

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
    elif current_date.hour < 4:
        days_until_weekly = 8 - day_of_week_now
        days_until_scrip = 10 - day_of_week_now
    else:
    	days_until_weekly = 7 - day_of_week_now
        days_until_scrip = 9 - day_of_week_now

    # daily timer calculation
    #current_day += 1 if current_date.hour >= 11 else 0
    daily_timer = datetime.datetime(
        current_date.year,
        current_date.month,
        current_date.day,
        11,
        0,
        0)
        
    weekly_timer = datetime.datetime(
        current_date.year,
        current_date.month,
        current_date.day,
        4,
        0,
        0)

    daily_delta = daily_timer - current_date
    weekly_delta = weekly_timer - current_date
    
    # get time left until daily reset
    daily_hours, daily_minutes = calculate_time_parts(daily_delta)
    dhstr = build_time_part_string(daily_hours, "hour")
    dmstr = build_time_part_string(daily_minutes, "minute")[:-2]

    # get time left until weekly reset
    weekly_hours, weekly_minutes = calculate_time_parts(weekly_delta)
    wdstr = build_time_part_string(days_until_weekly, "day")
    whstr = build_time_part_string(weekly_hours, "hour")
    wmstr = build_time_part_string(weekly_minutes, "minute")[:-2]

    # get time left until scrip reset
    scrip_hours, scrip_minutes = calculate_time_parts(weekly_delta)
    sdstr = build_time_part_string(days_until_scrip, "day") 
    shstr = build_time_part_string(scrip_hours, "hour")
    smstr = build_time_part_string(scrip_minutes, "minute")[:-2]

    # return results
    timer = "{}{} until daily reset\n".format(dhstr, dmstr)
    timer += "{}{}{} until weekly reset\n".format(wdstr, whstr, wmstr)
    timer += "{}{}{} until scrip and grand company reset".format(sdstr, shstr, smstr)
        
    return timer

def calculate_time_parts(time_delta):
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)    
    return hours, minutes

def build_time_part_string(time_value, part):
    if time_value == 0:
        return ""
    elif time_value == 1:
        return "{} {}, ".format(str(time_value), part)
    else:
        return "{} {}s, ".format(str(time_value), part)