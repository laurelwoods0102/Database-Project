from django.db import models

class CityData(models.Model):
    city = models.CharField(max_length=25, unique=True)

class CategoryData(models.Model):
    category = models.CharField(max_length=25, unique=True)
