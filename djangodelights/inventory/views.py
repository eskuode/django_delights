from django.shortcuts import render
from django.shortcuts import redirect
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import (
    IngredientCreateForm,
    MenuItemCreateForm,
    RecipeRequirementCreateForm,
    PurchaseCreateForm,
)
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Sum, F, Count


# Create your views here.
class HomeView(TemplateView):
    template_name = "inventory/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class CreateIngredientView(CreateView):
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
        context["ingredients"] = Ingredient.objects.all()
        return context


class CreateMenuView(CreateView):
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


class CreateRecipeView(CreateView):
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


class CreatePurchaseView(CreateView):
    model = Purchase
    form_class = PurchaseCreateForm
    template_name = "inventory/add_purchase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menu"] = MenuItem.objects.all()
        context["recipes"] = RecipeRequirement.objects.all()
        menu_item_list = []
        for menu_item in MenuItem.objects.all():
            for recipe in menu_item.reciperequirement_set.all():
                if (
                    recipe.quantity <= recipe.ingredient.quantity
                    and recipe.menu_item not in menu_item_list
                ):
                    menu_item_list.append(recipe.menu_item)
                elif recipe.quantity > recipe.ingredient.quantity:
                    menu_item_list.remove(recipe.menu_item)
                    break
        context["menu_item"] = menu_item_list
        return context

    def post(self, request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menu_item=menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.quantity -= requirement.quantity
            required_ingredient.save()

        purchase.save()
        return redirect("/purchases/list")


class ProfitView(TemplateView):
    template_name = "inventory/profit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        menu = MenuItem.objects.all()
        context["menu"] = menu
        context["recipes"] = RecipeRequirement.objects.all()
        context["purchases"] = Purchase.objects.all()
        revenue = Purchase.objects.aggregate(revenue=Sum("menu_item__price"))["revenue"]
        total_cost = 0
        for purchase in Purchase.objects.all():
            for recipe_requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += (
                    recipe_requirement.ingredient.unit_price
                    * recipe_requirement.quantity
                )
        context["revenue"] = revenue
        context["total_cost"] = total_cost
        context["profit"] = revenue - total_cost
        item_cost = [
            item.reciperequirement_set.aggregate(
                cost=Sum(F("quantity") * F("ingredient__unit_price"))
            )
            for item in MenuItem.objects.all()
        ]
        context["item_cost"] = item_cost
        purchase_count = [
            item.purchase_set.aggregate(total=Count("menu_item"))
            for item in MenuItem.objects.all()
        ]
        context["purchase_count"] = purchase_count
        item_report = zip(purchase_count, item_cost, menu)
        context["item_report"] = item_report
        return context
