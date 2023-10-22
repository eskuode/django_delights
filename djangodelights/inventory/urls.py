from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('ingredients/list', views.IngredientView.as_view(), name="ingredients"),
    path('menu/list', views.MenuView.as_view(), name='menu'),
    path('purchases/list', views.PurchaseView.as_view(), name="purchases"),
    path('profit/list', views.ProfitView.as_view(), name='profit'),
]