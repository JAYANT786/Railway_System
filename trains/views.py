from django.shortcuts import render
from .models import Train

def train_list(request):
    trains = None   

    source = request.GET.get('source', '').strip()
    destination = request.GET.get('destination', '').strip()

    if source and destination:
        trains = Train.objects.filter(
            source__icontains=source,
            destination__icontains=destination
        )

    context = {
        'trains': trains,
        'source': source,
        'destination': destination
    }

    return render(request, 'train_list.html', context)