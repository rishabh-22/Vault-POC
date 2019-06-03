
import json

from django.http import JsonResponse
from django.shortcuts import render
from Products.models import Product
from Orders.models import Order


def checkout(request):
    context = {'products': get_cart_items(request)}
    return render(request, 'Orders/checkout.html', context=context)


def cart_detail_to_product(prod_dict):
    copy = prod_dict.copy()
    pk = copy.pop('pk')
    copy['product'] = Product.objects.get(pk=pk)
    copy['total_product_price'] = copy['product'].price * copy['qty']
    return copy

  
def get_cart_items(request):
    cart = request.session.get('cart', dict())
    return {k: cart_detail_to_product(v) for k, v in cart.items()}

  
def orders(request):
    if request.method == 'POST':
        address = json.loads(request.body)['address']
        data = request.session['cart']
        for key, value in data.items():
            product_id = int(value['pk'])
            qty = int(value['qty'])
            ord = Order(
                buyer=request.user,
                product=Product.objects.get(pk=product_id),
                quantity=qty,
                shipping_address=address,
            )
            ord.save()
        del request.session['cart']
        request.session.modified = True
        return JsonResponse({'success': True})

    if request.method == 'GET':
            context = {'products': get_cart_items(request)}

            return render(request, 'Orders/orders.html', context=context)





    #         import pdb;pdb.set_trace()
#return render(request, 'Orders/orders.html')

