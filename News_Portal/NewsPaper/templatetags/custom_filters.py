from django import template

register = template.Library()


@register.filter()
def censor(phrase):
        swear_words =['клубник', 'кокос', 'мопс']
        for word in swear_words:
            parts = []
            for symbol in range(len(phrase)):
                equal_part = phrase[symbol:symbol + len(word)]
                parts.append(equal_part)
            for part in parts:
                if part.lower() == word:
                    phrase = phrase.replace(part, '*' * len(part))
        return phrase  