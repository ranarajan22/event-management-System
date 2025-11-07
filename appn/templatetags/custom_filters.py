from django import template

register = template.Library()

@register.filter
def has_role(user, roles):
    """Check if a user has one of the specified roles."""
    return user.role in roles.split(',')

@register.filter
def is_registered(event, user):
    return event.registrations.filter(user=user).exists()
