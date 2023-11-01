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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menu"] = MenuItem.objects.all()
        context["recipes"] = RecipeRequirement.objects.all()
        context["purchases"] = Purchase.objects.all()

        return context


class IngredientView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredients.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["ingredients"] = Ingredient.objects.all()
        return context


class CreateIngredientView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = "inventory/add_ingredient.html"


class UpdateIngredientView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = "inventory/update_ingredient.html"


class MenuView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/menu.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["menu"] = MenuItem.objects.all()
        context["ingredients"] = Ingredient.objects.all()
        return context


class CreateMenuView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemCreateForm
    template_name = "inventory/add_menu.html"


class RecipeView(LoginRequiredMixin, ListView):
    model = RecipeRequirement
    template_name = "inventory/menu.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["ingredients"] = Ingredient.objects.all()
        context["menu"] = MenuItem.objects.all()
        context["recipes"] = RecipeRequirement.objects.all()
        return context


class CreateRecipeView(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    form_class = RecipeRequirementCreateForm
    template_name = "inventory/add_recipe.html"


class PurchaseView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchases.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["purchases"] = Purchase.objects.all()
        return context


class CreatePurchaseView(LoginRequiredMixin, CreateView):
    template_name = "inventory/add_purchase.html"
    form_class = PurchaseCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_items = []
        for item in MenuItem.objects.all():
            for recipe in item.reciperequirement_set.all():
                if (
                    recipe.quantity <= recipe.ingredient.quantity
                    and recipe.menu_item not in menu_items
                ):
                    menu_items.append(recipe.menu_item)
                elif (
                    recipe.quantity > recipe.ingredient.quantity
                    and recipe.menu_item in menu_items
                ):
                    menu_items.remove(recipe.menu_item)
                    break
                else:
                    break
        context["menu_items"] = menu_items
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
        return redirect("/purchases")


class ProfitView(LoginRequiredMixin, TemplateView):
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


def log_out(request):
    logout(request)
    return redirect("/")
