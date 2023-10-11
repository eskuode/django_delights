from django.db import models

#models
class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=30)
    available_quantity = models.IntegerFiel(default = 0)
    price_per_unit = models.FloatField(default=0.0)

class MenuItem(models.Model):
    menu_item = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)

class RecipeRequirement(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

class Purchase(models.Model):
    purchase = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
