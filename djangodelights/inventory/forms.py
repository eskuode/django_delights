from django import forms
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase

class IngredientCreateForm(forms.ModelForm):
    model = Ingredient
    fields = "__all__"

class MenuItemCreateForm(forms.ModelForm):
    model = MenuItem
    fields = "__all__"

class RecipeRequirementCreateForm(forms.ModelForm):
    model = RecipeRequirement
    fields = "__all__"

class PurchaseCreateForm(forms.ModelForm):
    model = Purchase
    fields = "__all__"