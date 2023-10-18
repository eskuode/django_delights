from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('ingredient/list', views.IngredientView.as_view(), name="ingredients"),
    path('menu/list', views.MenuView.as_view(), name="menu"),
    path('recipe/list', views.RecipeView.as_view(), name="recipes"),
    path('purchase/list', views.PurchaseView.as_view(), name="purchases"),
]