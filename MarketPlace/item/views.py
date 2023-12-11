from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from decimal import Decimal

from .forms import NewItemForm, EditItemForm
from .models import Item, Category


def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    sort_by = request.GET.get('sort_by', 'name')  # Default to sorting by name

    # Get min and max price from query parameters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Add sorting logic
    if sort_by == 'name_desc':
        items = items.order_by('-name')
    elif sort_by == 'price':
        items = items.order_by('price')
    elif sort_by == 'price_desc':
        items = items.order_by('-price')

    # Apply price range filter
    if min_price is not None:
        items = items.filter(price__gte=Decimal(min_price))
    if max_price is not None:
        items = items.filter(price__lte=Decimal(max_price))

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'sort_by': sort_by,
        'min_price': min_price,
        'max_price': max_price,
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold = False).exclude(pk=pk)[0:3]
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items':related_items,
    })
#
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk = item.id)
    else:
        form = NewItemForm()
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk = item.id)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item',
    })
