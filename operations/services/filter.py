def filter_by_status(entries, statuses):
    """
    Фильтр по статусам
    """
    selected_statuses = [
        int(s) for s in statuses if s.isdigit()
    ]

    if selected_statuses:
        return entries.filter(status_id__in=selected_statuses)

    return entries


def filter_by_date(entries, date_from=None, date_to=None):
    """
    Фильтр по диапазону дат
    """
    if date_from:
        entries = entries.filter(date__gte=date_from)

    if date_to:
        entries = entries.filter(date__lte=date_to)

    return entries


def filter_by_structure(
    entries,
    tree,
    types=None,
    categories=None,
    subcategories=None,
    get_all_subcategory_ids=None
):
    """
    Фильтр по дереву структуры
    """

    types = [int(x) for x in types if x.isdigit()]
    categories = [int(x) for x in categories if x.isdigit()]
    subcategories = [int(x) for x in subcategories if x.isdigit()]

    if types or categories or subcategories:
        expanded_ids = get_all_subcategory_ids(
            tree,
            types,
            categories,
            subcategories
        )

        entries = entries.filter(
            subcategory_id__in=expanded_ids
        )

    return entries
