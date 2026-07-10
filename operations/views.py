from django.shortcuts import render

from operations.models import OperationEntry

def index(request):

    entries = OperationEntry.objects.order_by("date")

    dates = (
    OperationEntry.objects
    .values_list("date", flat=True)
    .distinct()
    )

    context = {
        'dates': dates,
        'entries': entries
    }

    return render(request, 'operations/index.html', context)
