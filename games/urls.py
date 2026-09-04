from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('catalog/', views.catalog, name='catalog'),
    # Категория теперь тоже ведёт на универсальную функцию views.catalog:
    path('catalog/<slug:category_slug>/', views.catalog, name='category_detail'),
    path('game/<slug:game_slug>/', views.game_detail, name='game_detail'),
    path('privacy/', views.privacy, name='privacy'),
]