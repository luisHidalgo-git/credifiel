from django.urls import path
from . import views

urlpatterns = [
    path('collection-stats/', views.collection_stats, name='collection-stats'),
]