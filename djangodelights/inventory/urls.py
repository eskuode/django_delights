from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("logout/", views.log_out, name="logout"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("", views.HomeView.as_view(), name="home"),
    path("ingredients", views.IngredientView.as_view(), name="ingredients"),
    path(
        "ingredients/create",
        views.CreateIngredientView.as_view(),
        name="ingredientcreate",
    ),
    path(
        "ingredients/<pk>/update",
        views.UpdateIngredientView.as_view(),
        name="ingredientupdate",
    ),
    path("menu", views.MenuView.as_view(), name="menu"),
    path("menu/create", views.CreateMenuView.as_view(), name="menucreate"),
    path("recipes", views.CreateRecipeView.as_view(), name="recipecreate"),
    path("purchases", views.PurchaseView.as_view(), name="purchases"),
    path("purchase/create", views.CreatePurchaseView.as_view(), name="purchasecreate"),
    path("profit", views.ProfitView.as_view(), name="profit"),
]
