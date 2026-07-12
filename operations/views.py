from django.shortcuts import render
from operations.models import OperationEntry
from catalog.models import Status
from catalog.views import build_tree


def get_all_subcategory_ids(tree, type_ids, cat_ids, subcat_ids):
    """
    Возвращает множество id подкатегорий, соответствующих выбранным
    типам, категориям и подкатегориям.
    """
    result = set(subcat_ids)  # явно выбранные подкатегории

    # Строим отображения: категория -> множество подкатегорий
    #                       тип -> множество подкатегорий
    cat_to_subcats = {}
    type_to_subcats = {}

    for type_node in tree:
        t_id = type_node['id']
        subcats = set()
        for cat in type_node.get('categories', []):
            c_id = cat['id']
            cat_subcats = {sub['id'] for sub in cat.get('subcategories', [])}
            cat_to_subcats[c_id] = cat_subcats
            subcats.update(cat_subcats)
        type_to_subcats[t_id] = subcats

    # Добавляем подкатегории выбранных категорий
    for cat_id in cat_ids:
        if cat_id in cat_to_subcats:
            result.update(cat_to_subcats[cat_id])

    # Добавляем подкатегории выбранных типов
    for type_id in type_ids:
        if type_id in type_to_subcats:
            result.update(type_to_subcats[type_id])

    return result


def index(request):
    entries = OperationEntry.objects.all()

    # 1. Фильтр по датам
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        entries = entries.filter(date__gte=date_from)
    if date_to:
        entries = entries.filter(date__lte=date_to)

    # 2. Фильтр по статусам
    selected_statuses_str = request.GET.getlist('status')
    selected_statuses = [int(s) for s in selected_statuses_str if s.isdigit()]
    if selected_statuses:
        entries = entries.filter(status_id__in=selected_statuses)

    # 3. Дерево структуры (нужно и для фильтра, и для отображения)
    tree = build_tree()

    # 4. Получаем выбранные элементы структуры
    selected_types_str = request.GET.getlist('type')
    selected_categories_str = request.GET.getlist('category')
    selected_subcategories_str = request.GET.getlist('subcategory')

    selected_types_int = [int(x) for x in selected_types_str if x.isdigit()]
    selected_categories_int = [int(x) for x in selected_categories_str if x.isdigit()]
    selected_subcategories_int = [int(x) for x in selected_subcategories_str if x.isdigit()]

    if selected_types_int or selected_categories_int or selected_subcategories_int:
        expanded_ids = get_all_subcategory_ids(
            tree,
            selected_types_int,
            selected_categories_int,
            selected_subcategories_int
        )
        entries = entries.filter(subcategory_id__in=expanded_ids)

    # Подготовка контекста
    entries = entries.order_by("date")
    dates = entries.values_list("date", flat=True).distinct()
    statuses = Status.objects.values("id", "name")

    context = {
        'dates': dates,
        'entries': entries,
        'statuses': statuses,
        'tree': tree,
        'selected_statuses': selected_statuses,            
        'selected_types': selected_types_str,       
        'selected_categories': selected_categories_str,   
        'selected_subcategories': selected_subcategories_str,
    }
    return render(request, 'operations/index.html', context)
