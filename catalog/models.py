from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    active = models.BooleanField(default=True, verbose_name='Не было удалено')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'types'
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

class Category(models.Model):
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'subcategories'
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

class Status(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'statuses'
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
