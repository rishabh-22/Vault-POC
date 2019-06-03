from django.shortcuts import render
from Products.models import Product


def checkout(request):
    context = {'products': get_cart_items(request)}
    return render(request, 'Orders/checkout.html', context=context)


def cart_detail_to_product(prod_dict):
    copy = prod_dict.copy()
    pk = copy.pop('pk')
    copy['product'] = Product.objects.get(pk=pk)
    copy['total_product_price'] = copy['product'].price * copy['qty']
    return copy


def orders(request):
    context = {'products': get_cart_items(request)}
    return render(request, 'Orders/orders.html', context=context)


def get_cart_items(request):
    cart = request.session.get('cart', dict())
    return {k: cart_detail_to_product(v) for k, v in cart.items()}

#
# def process_order(request):
#     if request.method == 'GET':
#         order = Order.objects.create(
#             buyer=request.user,
#             product=product,
#             payment_type=payment_type,
#             shipping_address=address,
#
#)
