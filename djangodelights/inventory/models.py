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
    quantity = models.FloatField(default = 0.0)
    unit = models.CharField(max_length=2, choices=UNIT_TYPE_CHOICES, default=OTHER)
    unit_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name 

class MenuItem(models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.title 
    
class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.0)

    def __str__(self):
        return self.menu_item.title + " " + self.ingredient.name

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.menu_item.title + " " + self.timestamp   
