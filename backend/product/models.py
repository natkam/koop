from django.db import models


class Week(models.Model):
    number = models.IntegerField()


class Product(models.Model):
    name = models.TextField()
    week = models.ForeignKey(Week, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    quantity = models.IntegerField(null=True)