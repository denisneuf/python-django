from django import template
register = template.Library()

from datetime import datetime

from ..models import Person

# All custom template tag go here
@register.simple_tag
def myfirst_method(arg1, arg2, arg3):
    # Your method definition
    return 'Your output ' + arg1 + " " + str (arg2 + arg3)


@register.simple_tag
def mysecond_method(arg1, arg2, arg3, arg4):
    # Your method definition
    return 'Your output'


@register.simple_tag
def any_function():
    return Person.objects.count()

@register.simple_tag
def get_current_time(format_string):
    return datetime.now().strftime(format_string)


@register.inclusion_tag('display.html')
# Declare function to find out the even numbers within a range
def display_even_numbers(a, b):
    # Declare a empty list
    number = []
    # Iterate the loop to find out the even number between a and b
    for i in range(a, b):
        # Check the number is even or not
        if i % 2 == 0:
            # Add the number in the list if it is even
            number.append(i)
    # Return the list to the display.html file
    return {"output": number}


