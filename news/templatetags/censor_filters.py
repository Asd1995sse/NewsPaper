from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

# Список запрещённых слов
BAD_WORDS = [
    'редиска',
    'дурак',
    'сволочь',
    'гад',
    'квадробер',
    'хобихорсинг',
]

# Регистрация фильтра + проверка на то, что аргумент строка
@register.filter(name='censor')
@stringfilter
def censor(value):
    """
    Фильтр заменяет запрещённые слова в строке на символ '*'.
    Учитывает регистр первой буквы (верхний или нижний).
    """
    if not isinstance(value, str):
        raise TypeError("Фильтр 'censor' применяется только к строкам")

    result = value
    for word in BAD_WORDS:
        # Проверяем разные варианты написания, Нижний или Верхний регистр
        variants = [word, word.capitalize()]
        for variant in variants:
            if variant in result:
                # Заменяем все буквы слова (кроме первой) на '*'
                censored = variant[0] + '*' * (len(variant) - 1)
                result = result.replace(variant, censored)

    return result