from django import template


register = template.Library()

STOP_WORDS = ("Новый ", "новый ", 'Пост ', 'пост ', 'сбитый ', 'Сбитый ')

@register.filter()
def censor(text):
    for word in STOP_WORDS:
        text = text.replace(word, word[0] + ('*' * (len(word) - 1)) + ' ')
    return f'{text}'
