from django import template



register = template.Library()

censor = ['террористической']

@register.filter()
def censor(word):
   if isinstance(word, str):
      for i in cens:
         word = word.replace(i[1:], '*' * len(i[1:]))
   else:
      raise ValueError(
         'custom_filters -> censor -> A string is expected, but a different data type has been entered')
   return word



@register.filter
def hide_forbidden(value):
    words = value.split()
    result = []
    for word in words:
        if word in forbidden_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)