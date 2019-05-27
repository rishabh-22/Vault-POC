from django.shortcuts import render
from Products.models import Product


def checkout(request):
    cart = request.session['cart']
    context = {'products': list()}
    for detail in cart:
        product = Product.objects.get(pk=detail['pk'])
        context_detail = {'qty': detail['qty'], 'product': product}
        context['products'].append(context_detail)
    return render(request, 'Orders/checkout.html', context=context)

