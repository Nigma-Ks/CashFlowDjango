from django.contrib import admin

from operations.models import OperationEntry, Type, Category, SubCategory, Status

admin.site.register(OperationEntry)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Status)
