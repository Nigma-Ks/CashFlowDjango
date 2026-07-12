from django.shortcuts import render
from operations.services.chained_fields import build_tree, get_all_subcategory_ids
from operations.services.filter import (
    filter_by_status,
    filter_by_date,
    filter_by_structure,
)

from operations.models import OperationEntry, Status


def index(request):
    entries = OperationEntry.objects.all()

    # Параметры фильтрации из формы
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    selected_statuses = request.GET.getlist("status")
    selected_types = request.GET.getlist("type")
    selected_categories = request.GET.getlist("category")
    selected_subcategories = request.GET.getlist("subcategory")

    tree = build_tree()

    # Применение фильтров
    entries = filter_by_date(entries, date_from, date_to)

    entries = filter_by_status(entries, selected_statuses)

    entries = filter_by_structure(
        entries,
        tree,
        selected_types,
        selected_categories,
        selected_subcategories,
        get_all_subcategory_ids,
    )

    entries = entries.order_by("date")

    dates = entries.values_list("date", flat=True).distinct()

    statuses = Status.objects.values("id", "name")

    context = {
        "dates": dates,
        "entries": entries,
        "statuses": statuses,
        "tree": tree,
        "selected_statuses": selected_statuses,
        "selected_types": selected_types,
        "selected_categories": selected_categories,
        "selected_subcategories": selected_subcategories,
    }

    return render(request, "operations/index.html", context)
