from django.shortcuts import render
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from django.views.generic import ListView

# Create your views here.
class IngredientView(ListView):
    model = Ingredient
    template = "inventory/ingredient.html"

class MenuView(ListView):
    model = MenuItem
    template = "inventory/menu.html"

class RecipeView(ListView):
    model = RecipeRequirement
    template = "inventory/recipes.html"

class PurchaseView(ListView):
    model = Purchase
    template = "inventory/purchases.html"
   