from django.db import models
from datetime import datetime   

# Create your models here.
class Ingredient(models.Model):
  OUNCE = "OC"
  LBS = "LB"
  GRAMS = "G"
  EGGS = "EG"
  OTHER = "OT"
  UNIT_TYPE_CHOICES = [
    (OUNCE, "ounces"),
    (LBS, "lbs"),
    (GRAMS, "grams"),
    (EGGS, "eggs"),
    (OTHER, "other")
  ]
  name = models.CharField(max_length=50)
  quantity = models.FloatField(default=0.0)
  unit = models.CharField(max_length=2, choices=UNIT_TYPE_CHOICES, default=OTHER)
  unit_price = models.FloatField(default=0.0)
  def __str__(self):
    return self.name +"-"+ str(self.quantity) +" "+ str(self.unit_price)+"/"+self.unit

class MenuItem(models.Model):
  title = models.CharField(max_length=50)
  price = models.FloatField(default=0.0)
  def __str__(self):
    return self.title + " " + str(self.price)
  
class RecipeRequirement(models.Model):
  menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
  ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
  quantity = models.FloatField(default=0.0)
  def __str__(self):
    return self.menu_item.title + ": " + self.ingredient.name + "/" + str(self.quantity)

class Purchase(models.Model):
  menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(default=datetime.now(), blank=True)
  def __str__(self):
    return self.menu_item.title + " " + str(self.timestamp)
# Create your models here.
