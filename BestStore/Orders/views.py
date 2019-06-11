
import json

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from Products.models import Product
from Orders.models import Order
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def checkout(request):
    context = {'products': get_cart_items(request)}
    return render(request, 'Orders/checkout.html', context=context)


def order_display(request):
    context = {'your_orders': Order.objects.filter(buyer=request.user.id)}
    return render(request, 'Orders/order_processing.html', context)


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
            ord_price = Product.objects.get(pk=product_id).price
            ord = Order(
                buyer=request.user,
                product=Product.objects.get(pk=product_id),
                quantity=qty,
                shipping_address=address,
                order_price=ord_price,
            )
            ord.save()
        del request.session['cart']
        request.session.modified = True
        import pdb; pdb.set_trace()
        email = request.user.email
        html_message = render_to_string('Orders/order_confirm_template.html',)
        plain_message = strip_tags(html_message)
        send_mail("Order Conformation", plain_message, "rbtherib2@gmail.com", [email], html_message=html_message, fail_silently=False)
        return JsonResponse({'success': True})

    if request.method == 'GET':
            context = {'products': get_cart_items(request)}
            return render(request, 'Orders/orders.html', context=context)
