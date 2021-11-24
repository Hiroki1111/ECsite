from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/<slug>', views.ItemDetailView.as_view(), name='product'),
]