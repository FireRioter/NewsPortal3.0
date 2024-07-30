from django.urls import path
from .views import AdsList, AdDetail, AdCreate, AdUpdate, AdDelete
from .views import ResponseCreate, ResponseDelete, ResponseAccept, ResponseListView
from .views import NewsletterView

urlpatterns = [
    path('ads/', AdsList.as_view(), name='ads_list'),
    path('ads/create/', AdCreate.as_view(), name='ad_create'),
    path('ads/<int:pk>/', AdDetail.as_view(), name='ad_detail'),
    path('ads/<int:pk>/edit/', AdUpdate.as_view(), name='ad_update'),
    path('ads/<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),
    path('ads/<int:ad_id>/respond/', ResponseCreate.as_view(), name='response_create'),
    path('responses/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
    path('responses/<int:pk>/accept/', ResponseAccept.as_view(), name='response_accept'),
    path('responses/', ResponseListView.as_view(), name='response_list'),
    path('newsletter/', NewsletterView.as_view(), name='newsletter'),
    ]