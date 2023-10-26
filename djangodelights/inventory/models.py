from django.db import models
from datetime import datetime   

# Create your models here.
class Ingredient(models.Model):
  OUNCE = "ounces"
  LBS = "lbs"
  GRAMS = "grams"
  EGGS = "eggs"
  OTHER = "other"
  UNIT_TYPE_CHOICES = [
    (OUNCE, "OC"),
    (LBS, "LB"),
    (GRAMS, "G"),
    (EGGS, "EG"),
    (OTHER, "OT")
  ]
  name = models.CharField(max_length=50, verbose_name= "Ingredient")
  quantity = models.FloatField(default=0.0, verbose_name="Quantity")
  unit = models.CharField(max_length=10, choices=UNIT_TYPE_CHOICES, default=OTHER, verbose_name="Units")
  unit_price = models.FloatField(default=0.0, verbose_name="Price per unit")
  def __str__(self):
    return self.name +"-"+ str(self.quantity) +" "+ str(self.unit_price)+"/"+self.unit
  def get_absolute_url(self):
    return "/ingredients"
  
class MenuItem(models.Model):
  title = models.CharField(max_length=50, verbose_name="Menu Item")
  price = models.FloatField(default=0.0, verbose_name="Price")
  def __str__(self):
    return self.title + " " + str(self.price)
  def get_absolute_url(self):
    return "/menu"
  
class RecipeRequirement(models.Model):
  menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="Menu Item")
  ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ingrediet")
  quantity = models.FloatField(default=0.0, verbose_name="Quantity")
  def __str__(self):
    return self.menu_item.title + ": " + self.ingredient.name + "/" + str(self.quantity)
  @property
  def cost(self):
    return self.quantity * self.ingredient.unit_price
  def get_absolute_url(self):
    return "/menu"


class Purchase(models.Model):
  menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="Menu Item")
  timestamp = models.DateTimeField(default=datetime.now(), blank=True, verbose_name="Order Time")
  def __str__(self):
    return self.menu_item.title + " " + str(self.timestamp)
  def get_absolute_url(self):
    return "/purchases"
# Create your models here.
