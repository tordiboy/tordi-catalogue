import re
from django import template

register = template.Library()

@register.filter
def highlight(text, word):
    if not word:
        return text

    pattern = re.compile(re.escape(word), re.IGNORECASE)

    return pattern.sub(
        lambda m: f"<mark>{m.group()}</mark>",
        text
    )