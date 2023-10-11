from django.db import models

#models
class Ingredient(models.Model):
    TBSP = "TB"
    TSP = "TS"
    ML = "ML"
    G = "G"
    OTHER = "OT"
    UNIT_TYPE_CHOICES = [
        (TBSP, "tbsp"),
        (TSP, "tsp"),
        (ML, "mL"),
        (G, "g"),
        (OTHER, "other")
    ]
    name = models.CharField(max_length=30)
    quantity = models.IntegerFiel(default = 0)
    unit = models.CharField(max_length=2, choices=UNIT_TYPE_CHOICES, default=OTHER)
    unit_price = models.FloatField(default=0.0)

class MenuItem(models.Model):
    menu_item = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)

class RecipeRequirement(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

class Purchase(models.Model):
    purchase = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
