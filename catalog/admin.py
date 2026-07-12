from django.contrib import admin

from catalog.models import Type, Category, SubCategory, Status

admin.site.register(Type)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Status)
