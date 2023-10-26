from django.shortcuts import render
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import IngredientCreateForm, MenuItemCreateForm, RecipeRequirementCreateForm, PurchaseCreateForm
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Sum

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
    
class IngredientCreate(CreateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = "inventory/add_ingredient.html"

class UpdateIngredientView(UpdateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = "inventory/update_ingredient.html"
    
class MenuView(ListView):
    model = MenuItem
    template_name = "inventory/menu.html"
    def get_context_data(self):
       context = super().get_context_data()
       context["menu"] = MenuItem.objects.all()   
       return context
    
class MenuCreate(CreateView):
    model = MenuItem
    form_class = MenuItemCreateForm
    template_name = "inventory/add_menu.html"

class RecipeView(ListView):
    model = RecipeRequirement
    template_name = "inventory/menu.html"
    def get_context_data(self):
        context = super().get_context_data()
        context["ingredients"] = Ingredient.objects.all()
        context["menu"] = MenuItem.objects.all()
        context["recipes"] = RecipeRequirement.objects.all()
        return context
    
class RecipeCreate(CreateView):
    model = RecipeRequirement
    form_class = RecipeRequirementCreateForm
    template_name = "inventory/add_recipe.html"

    
class PurchaseView(ListView):
    model = Purchase
    template_name = "inventory/purchases.html"
    def get_context_data(self):
        context = super().get_context_data()
        context["purchases"] = Purchase.objects.all()
        return context
   
class PurchaseCreate(CreateView):
    model = Purchase
    form_class = PurchaseCreateForm
    template_name = "inventory/add_purchase.html"

class ProfitView(TemplateView):
    template_name = "inventory/profit.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menu"] = MenuItem.objects.all()
        context["recipes"] = RecipeRequirement.objects.all()
        context["purchases"] = Purchase.objects.all()
        revenue = Purchase.objects.aggregate(
            revenue=Sum("menu_item__price"))["revenue"]
        total_cost = 0
        for purchase in Purchase.objects.all():
            for recipe_requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += recipe_requirement.ingredient.unit_price * recipe_requirement.quantity   
        context["revenue"] = revenue
        context["total_cost"] = total_cost
        context["profit"] = revenue - total_cost
    
     
        


      

        return context
    
    #def recipe_cost(self, recipe):
        ##for menu_item in MenuItem.objects.all():
            #for recipe in menu_item.reciperequirement_set.all():
                #return recipe.aggregate(Sum('cost'))
  
