from django.contrib import admin
from .models import Category, Post
from django.urls import path, include
from django.views.generic import TemplateView


def nullfy_quantity(modeladmin, request,queryset):  # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.

   queryset.update(rating = 0)


nullfy_quantity.short_description = 'Обнулить рейтинг статьей и новостей'  # описание для более понятного представления в админ панеле задаётся, как будто это объект


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
   # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
   list_display = ('title', 'date_in', 'rating', 'poste_type')  # оставляем только имя и цену товара
   list_filter = ('date_in', 'rating', 'poste_type')  # добавляем примитивные фильтры в нашу админку
   search_fields = ('poste_type', 'date_in')  # тут всё очень похоже на фильтры из запросов в базу
   actions = [nullfy_quantity]  # добавляем действия в список

admin.site.register(Category)
admin.site.register(Post, PostAdmin)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('news/', include('news.urls')),
]

# Register your models here.
