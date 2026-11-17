days_of_the_week = {
    'monday' : 1,
    'tuesday' : 2,
    'wednesday' : 3,
    'thursday' : 4,
    'friday' : 5,
    'saturday' : 6,
    'sunday' : 7
}

def add_time(start, duration, day=''):
    # We define 00:00 AM to be 0 minutes into the day 
    # We define 23:59 PM to be 1439 minutes into the day
    # This implies that after 1440 minutes after 00:00,
    # we arrive on a new day.
    minutes_in_a_day = 1440
    AM_or_PM = 'PM'

    # Total time with respect to a day.
    total_time_minutes = convert_start_time_to_minutes(start) + convert_duration_to_minutes(duration)
    # Days elapsed after the given start time
    days_passed_after_start = total_time_minutes//minutes_in_a_day
    # Current time of the day
    current_time = total_time_minutes % minutes_in_a_day
    current_time_hours = 0
    current_time_minutes = current_time % 60

    # Find the day of the week
    if day:
        number_current_day = (days_of_the_week[day.lower()] + days_passed_after_start)%7
        if number_current_day == 0:
            number_current_day = 7
        current_day = ''
        for day, i in days_of_the_week.items():
            if i == number_current_day:
                current_day = day[0].upper() + day[1:]
            

    # Current time will be in the interval [0, 1439] in the unit minutes
    if current_time < 60:
        current_time_hours = 12
        AM_or_PM = 'AM'
    elif current_time > 720 and current_time < 800:
        current_time_hours = 12
    elif current_time <= int(minutes_in_a_day/2):
        AM_or_PM = 'AM'
        current_time_hours = current_time//60
    else:
        current_time_hours = (current_time - int(minutes_in_a_day/2))//60

    if current_time_minutes >= 10:
        new_time = f'{current_time_hours}:{current_time_minutes} {AM_or_PM}'
    else: 
        new_time = f'{current_time_hours}:0{current_time_minutes} {AM_or_PM}' 


    if len(day) != 0:
        new_time += f', {current_day}'

    if days_passed_after_start == 1:
        new_time += f' (next day)'
    elif days_passed_after_start > 1:
        new_time += f' ({days_passed_after_start} days later)'
    else:
        pass

    return new_time

# We define another function that converts the duration input into elapsed minutes. 
# Duration being in the string form "XX...:XX" where hours can be of any size and minutes is in the interval [0,59].    

def convert_duration_to_minutes(duration):

    # Splits the duration into hours and minutes.
    hours = int(duration.split(':')[0])
    minutes = int(duration.split(':')[1])
    # Calculates the total amount of minutes in duration.
    total_minutes = hours * 60 + minutes

    return total_minutes 

def convert_start_time_to_minutes(start):
    minutes = 0

    time = start.split(' ')[0]
    time_hours = int(time.split(':')[0])
    time_minutes = int(time.split(':')[1])

    # Checks whether start is at AM or PM and converts
    # the start time into the appropriate amount of minutes
    # elapsed with respect to the definition of a day.

    if 'AM' in start:
        minutes += time_hours*60 + time_minutes
    else:
        minutes += 12*60 + time_hours*60 + time_minutes

    return minutes


print(add_time('11:59 AM', '0:5'))
print(add_time('11:55 AM', '3:12'))
print(add_time('2:59 AM', '24:00'))
print(add_time('11:59 PM', '24:05'))
print(add_time('8:16 PM', '466:02'))
print(add_time('3:30 PM', '2:12', 'Monday'))
print(add_time('2:59 AM', '24:00', 'saturDay'))
print(add_time('11:59 PM', '24:05', 'Wednesday'))
print(add_time('8:16 PM', '466:02', 'tuesday'))