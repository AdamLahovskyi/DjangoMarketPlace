from django.shortcuts import render, get_object_or_404
from .cart import Cart
from item.models import Item
from django.http import JsonResponse
from .models import Invoice

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities": quantities})
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        #look for item in db
        item = get_object_or_404(Item, id=product_id)
        #save to sess
        cart.add(item=item, quantity=product_qty)

        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_delete(request):
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')

        cart = Cart(request)
        cart.remove(product_id)

        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        cart.update(product=product_id, quantity = product_qty)
        response = JsonResponse({'qty':product_qty})

        return response


def buy_now(request):
    cart = Cart(request)
    cart_products = []
    total_price = 0

    for item in cart.get_prods():
        quantity = cart.get_quants().get(str(item.id), 0)
        cart_products.append({"item": item, "quantity": quantity})
        total_price += item.price * quantity

    # Save the purchase information to the database
    if cart_products:
        invoice = Invoice.objects.create(
            total_price=total_price,
            quantities=cart.get_quants(),
        )
        invoice.items.set(cart.get_prods())
        invoice.save()


    return render(request, "buy_now.html", {"cart_products": cart_products, "total_price": total_price})