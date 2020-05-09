from django import template
from datetime import datetime , timezone

register = template.Library()

@register.filter(name='time_elapsed')
def time_elapsed(created_time):
    """Takes in when a model was created 
    and returns a string representation"""

    now = datetime.now(timezone.utc)

    diff = now - created_time

    seconds_elapsed = diff.seconds
    weeks_elapsed =  diff.days//7

    if diff.days:
        if diff.days == 1:
            return f"{diff.days} day ago" 

        elif diff.days < 7:
            return f"{diff.days} days ago"      
    
        elif weeks_elapsed == 1:
            return f"{weeks_elapsed} week ago" 

        elif weeks_elapsed < 52:
            return f"{weeks_elapsed} weeks ago" 

        elif weeks_elapsed < 104:
            return f"{weeks_elapsed//52} year ago" 

        else:
            return f"{weeks_elapsed//52} years ago" 


    elif seconds_elapsed < 3600:
        timeelapsed =  diff.seconds//60
        if timeelapsed < 1:
            return "less than a minitue ago"
        elif timeelapsed ==1:
            return f"{timeelapsed} minute ago"
        else:
            return f"{timeelapsed} minutes ago"


    else:
        timeelapsed =  diff.seconds//3600
        if timeelapsed < 1:
            return f"{timeelapsed} hour ago" 
        else:
            return f"{timeelapsed} hours ago" 


# register.filter('time_elapsed', time_elapsed)




