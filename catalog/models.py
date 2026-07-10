from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'types'

class Category(models.Model):
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'subcategories'

class Status(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'statuses'
