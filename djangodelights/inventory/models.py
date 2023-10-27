from django.db import models
from datetime import datetime   

# Create your models here.
class Ingredient(models.Model):
  OUNCE = "ounces"
  LBS = "lbs"
  GRAMS = "grams"
  UNITS = "units"
  OTHER = "other"
  UNIT_TYPE_CHOICES = [
    (OUNCE, "ounces"),
    (LBS, "lbs"),
    (GRAMS, "grams"),
    (UNITS, "units"),
    (OTHER, "other")
  ]
  name = models.CharField(max_length=50, verbose_name= "Ingredient")
  quantity = models.FloatField(default=0.0, verbose_name="Quantity")
  unit = models.CharField(max_length=10, choices=UNIT_TYPE_CHOICES, default=OTHER, verbose_name="Units")
  unit_price = models.FloatField(default=0.0, verbose_name="Price per unit")
  def __str__(self):
    return self.name +"-"+ str(self.quantity) +" "+ str(self.unit_price)+"/"+self.unit
  def get_absolute_url(self):
    return "/ingredients/list"
  
class MenuItem(models.Model):
  title = models.CharField(max_length=50, verbose_name="Menu Item")
  price = models.FloatField(default=0.0, verbose_name="Price")
  def __str__(self):
    return self.title + " " + str(self.price)
  
  def get_absolute_url(self):
    return "/menu/list"
  
class RecipeRequirement(models.Model):
  menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="Menu Item")
  ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ingrediet")
  quantity = models.FloatField(default=0.0, verbose_name="Quantity")
  cost = models.FloatField(...)

  def save(self):
    self.cost = self.quantity * self.ingredient.unit_price
    return super(example, self).save()
  def __str__(self):
    return self.menu_item.title + ": " + self.ingredient.name + "/" + str(self.quantity)
  def get_absolute_url(self):
    return "/menu/list"


class Purchase(models.Model):
  menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="Menu Item")
  timestamp = models.DateTimeField(default=datetime.now(), blank=True, verbose_name="Order Time")
  def __str__(self):
    return self.menu_item.title + " " + str(self.timestamp)
  def get_absolute_url(self):
    return "/purchases/list"
# Create your models here.
