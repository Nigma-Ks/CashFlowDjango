from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.core.exceptions import ValidationError
from django.utils import timezone


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    active = models.BooleanField(default=True, verbose_name="Не было удалено")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "types"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Category(models.Model):
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "categories"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "subcategories"
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Status(models.Model):
    name = models.CharField(
        max_length=100, blank=True, null=True, unique=True, verbose_name="Название"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "statuses"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


def get_default_date():
    return timezone.now().date()


class OperationEntry(models.Model):
    date = models.DateField(default=get_default_date)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Статус",
        validators=[],
    )
    type = models.ForeignKey(
        Type, on_delete=models.PROTECT, blank=False, null=False, verbose_name="Тип"
    )
    category = ChainedForeignKey(
        Category,
        chained_field="type",
        chained_model_field="type",
        on_delete=models.PROTECT,
        verbose_name="Категория",
        auto_choose=True,
        sort=True,
    )

    subcategory = ChainedForeignKey(
        SubCategory,
        chained_field="category",
        chained_model_field="category",
        on_delete=models.PROTECT,
        verbose_name="Подкатегория",
        auto_choose=True,
        sort=True,
    )
    sum = models.IntegerField(blank=False, null=False, verbose_name="Сумма")
    comment = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Комментарий"
    )

    def __str__(self):
        return f"{self.sum} {self.type} — {self.category} ({self.subcategory})"

    def clean(self):
        super().clean()
        errors = {}

        if self.category_id and self.type_id:
            if self.category.type_id != self.type_id:
                errors["category"] = "Категория не принадлежит выбранному типу."
                errors["type"] = "Тип не соответствует выбранной категории."

        if self.subcategory_id and self.category_id:
            if self.subcategory.category_id != self.category_id:
                errors["subcategory"] = (
                    "Подкатегория не принадлежит выбранной категории."
                )
                errors["category"] = (
                    "Категория не соответствует выбранной подкатегории."
                )

        if (self.sum or self.sum == 0) and self.sum <= 0:
            errors["sum"] = "Введенная сумма не должна быть отрицательной."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "operations"
        verbose_name = "Запись об операции"
        verbose_name_plural = "Записи об операциях"
