

from django import template


register = template.Library()

POST_TYPE ={
   'news':  'NA',
   'articles': 'AR',
}

@register.filter()
def posts_type(value, code='news'):
   postfix = POST_TYPE[code]
   # Возвращаемое функцией значение подставится в шаблон.
   return f'{value} {postfix}'

