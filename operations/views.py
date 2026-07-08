from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {
        'status': ['Бизнес', 'Личное', 'Налог'],
        'dates': ['01-01-2025', '02-01-2025', '03-01-2025', '06-02-2025'],
        'type': ['Пополнение', 'Списание'],
        'category': ['Инфраструктура', 'Маркетинг'],
        'subcategory': ['VPS', 'Proxy']
    }
    return render(request, 'operations/index.html', context)
