from django import template

register = template.Library()

@register.filter
def rating_stars(value):
    if value is None:
        return ''

    rating_rounded = round(value)

    stars = "★" * rating_rounded
    blank_stars = "☆" * (5 - rating_rounded)

    return stars + blank_stars
