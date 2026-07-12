from operations.models import Type

def build_tree():
    '''
    Функция build_tree() собирает зависимые таблицы (Тип --> Категория --> Подкатегория) в дерево
    '''
    result = []
    types = Type.objects.prefetch_related("category_set__subcategory_set")

    for type_obj in types:
        type_item = {"id": type_obj.id, "name": type_obj.name, "categories": []}
        for category in type_obj.category_set.all():
            category_item = {
                "id": category.id,
                "name": category.name,
                "subcategories": [],
            }

            for subcategory in category.subcategory_set.all():
                category_item["subcategories"].append(
                    {"id": subcategory.id, "name": subcategory.name}
                )
            type_item["categories"].append(category_item)
        result.append(type_item)
    return result

def get_all_subcategory_ids(tree, type_ids, cat_ids, subcat_ids):
    """
    Возвращает множество id подкатегорий, соответствующих выбранным
    типам, категориям и подкатегориям.
    """
    result = set(subcat_ids)

    cat_to_subcats = {}
    type_to_subcats = {}

    #Заполняем словари категории --> подкатегории и тип --> подкатегории
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