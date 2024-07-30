import django_filters
from .models import Ad
from django_ckeditor_5.fields import CKEditor5Field

class AdFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Заголовок')

    class Meta:
        model = Ad
        fields = ['category', 'title']  # Поля, по которым можно фильтровать

        filter_overrides = {
            CKEditor5Field: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }