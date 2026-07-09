from datetime import date
from random import randint, choice

from catalog.models import (
    Status,
    Type,
    Category,
    SubCategory,
)

from operations.models import OperationEntry


# ---------- Статусы ----------
business, _ = Status.objects.get_or_create(name="Бизнес")
personal, _ = Status.objects.get_or_create(name="Личное")
tax, _ = Status.objects.get_or_create(name="Налог")

# ---------- Типы ----------
income, _ = Type.objects.get_or_create(name="Пополнение")
expense, _ = Type.objects.get_or_create(name="Списание")

# ---------- Категории ----------
infra, _ = Category.objects.get_or_create(
    name="Инфраструктура",
    defaults={"type": expense},
)

marketing, _ = Category.objects.get_or_create(
    name="Маркетинг",
    defaults={"type": expense},
)

sales, _ = Category.objects.get_or_create(
    name="Продажи",
    defaults={"type": income},
)

# ---------- Подкатегории ----------
vps, _ = SubCategory.objects.get_or_create(
    category=infra,
    name="VPS",
)

proxy, _ = SubCategory.objects.get_or_create(
    category=infra,
    name="Proxy",
)

farpost, _ = SubCategory.objects.get_or_create(
    category=marketing,
    name="Farpost",
)

avito, _ = SubCategory.objects.get_or_create(
    category=marketing,
    name="Avito",
)

clients, _ = SubCategory.objects.get_or_create(
    category=sales,
    name="Клиенты",
)

# ---------- Данные операций ----------
operations = [
    {
        "date": date(2025, 1, 1),
        "status": business,
        "type": expense,
        "category": infra,
        "subcategory": vps,
        "sum": 1200,
        "comment": "Оплата VPS",
    },
    {
        "date": date(2025, 1, 3),
        "status": business,
        "type": expense,
        "category": infra,
        "subcategory": proxy,
        "sum": 800,
        "comment": "Покупка Proxy",
    },
    {
        "date": date(2025, 1, 5),
        "status": business,
        "type": expense,
        "category": marketing,
        "subcategory": farpost,
        "sum": 3500,
        "comment": "Размещение объявлений",
    },
    {
        "date": date(2025, 1, 7),
        "status": business,
        "type": expense,
        "category": marketing,
        "subcategory": avito,
        "sum": 2700,
        "comment": "Продвижение на Avito",
    },
    {
        "date": date(2025, 1, 10),
        "status": personal,
        "type": income,
        "category": sales,
        "subcategory": clients,
        "sum": 50000,
        "comment": "Поступление от клиента",
    },
    {
        "date": date(2025, 1, 12),
        "status": tax,
        "type": expense,
        "category": marketing,
        "subcategory": avito,
        "sum": 1500,
        "comment": "Налоговый платеж",
    },
    {
        "date": date(2025, 1, 15),
        "status": business,
        "type": income,
        "category": sales,
        "subcategory": clients,
        "sum": 75000,
        "comment": "Оплата заказа",
    },
    {
        "date": date(2025, 1, 18),
        "status": business,
        "type": expense,
        "category": infra,
        "subcategory": vps,
        "sum": 1300,
        "comment": "Продление VPS",
    },
    {
        "date": date(2025, 1, 21),
        "status": personal,
        "type": income,
        "category": sales,
        "subcategory": clients,
        "sum": 18000,
        "comment": "Возврат средств",
    },
    {
        "date": date(2025, 1, 25),
        "status": business,
        "type": expense,
        "category": marketing,
        "subcategory": farpost,
        "sum": 4200,
        "comment": "Реклама",
    },
]

for operation in operations:
    OperationEntry.objects.create(**operation)

print(f"Создано {len(operations)} операций.")