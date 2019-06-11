import json
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from Products.models import Product
from Orders.models import Order
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Orders.models import OrderDetail


def checkout(request):
    context = {'products': get_cart_items(request)}
    return render(request, 'Orders/checkout.html', context=context)


def order_display(request):
    import pdb;pdb.set_trace()
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
        email = request.user.email
        product = [Product.objects.get(id=int(item)) for item in request.session.get("cart", None) if item is not None]
        order = Order()
        order.buyer = request.user
        order.address = address
        order.save()
        total_amount = 0
        for products in product:
            OrderDetail.objects.create(order=order,quantity=request.session["cart"][str(products.id)]["qty"],
                                       price=products.price,
                                       product_id=products.id,
                                       )
            total_amount += products.price * request.session["cart"][str(products.id)]["qty"]
        
        html_message = render_to_string('Orders/order_confirm_template.html',)
        plain_message = strip_tags(html_message)
        send_mail("Order Conformation", plain_message, "rbtherib2@gmail.com", [email], html_message=html_message, fail_silently=False)
        return JsonResponse({'success': True})

    if request.method == 'GET':
            context = {'products': get_cart_items(request)}
            return render(request, 'Orders/orders.html', context=context)


def cancel_order(request, pk):
    new_status = Order.objects.get(pk=pk)
    new_status.status = 'C'
    new_status.save()
    return redirect('order_display')
