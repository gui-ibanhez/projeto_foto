from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Prefetch
from .models import Store, StoreSection, Photo


def store_list(request):
    q = request.GET.get('q', '').strip()
    stores = Store.objects.all()
    if q:
        stores = stores.filter(models.Q(code__icontains=q) | models.Q(name__icontains=q) | models.Q(city__icontains=q))
    stores = stores.annotate(photo_count=Count('photos'))
    return render(request, 'gallery/store_list.html', {"stores": stores, "q": q})


def store_detail(request, pk):
    store = get_object_or_404(Store, pk=pk)
    sections = store.sections.filter(is_active=True).prefetch_related(
        Prefetch('photos', queryset=Photo.objects.select_related('section').order_by('-created_at'))
    )
    return render(request, 'gallery/store_detail.html', {"store": store, "sections": sections})

from django.shortcuts import render

# Create your views here.
