from collections import defaultdict
from django.shortcuts import render

from catalog.models import Type, Category, SubCategory, Status

def build_tree():
    result = []
    types = Type.objects.prefetch_related(
        'category_set__subcategory_set'
    ).filter(active=True)
    for type_obj in types:
        type_item = {
            "id": type_obj.id,
            "name": type_obj.name,
            "categories": []
        }
        for category in type_obj.category_set.all():
            category_item = {
                "id": category.id,
                "name": category.name,
                "subcategories": []
            }
            for subcategory in category.subcategory_set.all():

                    category_item["subcategories"].append({

                        "id": subcategory.id,
                        "name": subcategory.name

                    })
            type_item["categories"].append(category_item)
        result.append(type_item)
    return result

def catalog(request):

    statuses = Status.objects.values_list("name", flat=True)

    type_category_subcategory_tree = build_tree()
    content = {
        'statuses': statuses,
        'tree': type_category_subcategory_tree
    }
    return render(request, 'catalog/catalog.html', content)
