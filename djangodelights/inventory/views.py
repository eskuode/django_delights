from django.shortcuts import render
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from django.views.generic import TemplateView, ListView

# Create your views here.
class HomeView(TemplateView):
  template_name = "inventory/home.html"

  def get_context_data(self):
    context = super().get_context_data()
    context["ingredients"] = Ingredient.objects.all()
    context["menu"] = MenuItem.objects.all()
    context["recipes"] = RecipeRequirement.objects.all()
    context["purchases"] = Purchase.objects.all()
    
    return context
  
class IngredientView(ListView):
    model = Ingredient
    template_name = "inventory/ingredients.html"
    def get_context_data(self):
       context = super().get_context_data()
       context["ingredients"] = Ingredient.objects.all()
       return context
    
class MenuView(ListView):
    model = MenuItem
    template = "inventory/menu.html"

class RecipeView(ListView):
    model = RecipeRequirement
    template_name = "inventory/recipes.html"

class PurchaseView(ListView):
    model = Purchase
    template_name = "inventory/purchases.html"
    
       
   
class ProfitView(TemplateView):
    template_name = "inventory/profit.html"