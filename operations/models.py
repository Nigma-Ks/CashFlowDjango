from unicodedata import category
from xmlrpc.client import DateTime
from django.db import models

from catalog.models import Type, Category, SubCategory, Status
from django.utils import timezone

def get_default_date():
    return timezone.now().date()

class OperationEntry(models.Model):
    date = models.DateField(default=get_default_date)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.PROTECT, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=False, null=False)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, blank=False, null=False)
    sum = models.IntegerField(blank=False, null=False)
    comment = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'operations'