from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('ingredients/list', views.IngredientView.as_view(), name="ingredients"),
    path('ingredients/create', views.IngredientCreate.as_view(), name="ingredientcreate"),
    path('ingredients/<pk>/update', views.UpdateIngredientView.as_view(), name="ingredientupdate"),
    path('menu/list', views.MenuView.as_view(), name='menu'),
    path('menu/create', views.MenuCreate.as_view(), name="menucreate"),
    path('recipes/create', views.RecipeCreate.as_view(), name="recipecreate"),
    path('purchases/list', views.PurchaseView.as_view(), name="purchases"),
    path('purchase/create', views.PurchaseView.as_view(), name="purchasecreate"),
    path('profit/list', views.ProfitView.as_view(), name='profit'),
]