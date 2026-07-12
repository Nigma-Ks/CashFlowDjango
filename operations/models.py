from django.db import models
from django.core.exceptions import ValidationError

from catalog.models import Type, Category, SubCategory, Status
from django.utils import timezone

def get_default_date():
    return timezone.now().date()

class OperationEntry(models.Model):
    date = models.DateField(default=get_default_date)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, blank=True, null=True, verbose_name = 'Статус', validators=[])
    type = models.ForeignKey(Type, on_delete=models.PROTECT, blank=False, null=False, verbose_name = 'Тип')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=False, null=False, verbose_name = 'Категория')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, blank=False, null=False, verbose_name = 'Подкатегория')
    sum = models.IntegerField(blank=False, null=False, verbose_name = 'Сумма')
    comment = models.CharField(max_length=200, blank=True, null=True, verbose_name = 'Комментарий')

    def __str__(self):
        return f"{self.sum} {self.type} — {self.category} ({self.subcategory})"
    
    def clean(self):
        super().clean()
        errors = {}

        if self.category and self.type:
            if self.category.type_id != self.type_id:
                errors['category'] = 'Категория не принадлежит выбранному типу.'
                errors['type'] = 'Тип не соответствует выбранной категории.'

        if self.subcategory and self.category:
            if self.subcategory.category_id != self.category_id:
                errors['subcategory'] = 'Подкатегория не принадлежит выбранной категории.'
                errors['category'] = 'Категория не соответствует выбранной подкатегории.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'operations'
        verbose_name = 'Запись об операции'
        verbose_name_plural = 'Записи об операциях'