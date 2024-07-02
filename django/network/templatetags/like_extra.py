from django import template

from network.models import Post

register = template.Library()


@register.simple_tag
def is_like(user, arg2):
        return arg2.likes.filter(id=user.id).exists()