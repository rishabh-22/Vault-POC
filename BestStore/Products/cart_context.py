from .models import Product


def add_session_cart(request):
    """Adds the value of the products and shows the total"""
    total_qty = 0
    total_price = 0

    cart = request.session.get('cart', dict())

    for key in cart:
        qty = cart[key]['qty']
        pk = cart[key]['pk']
        price = Product.objects.get(pk=pk).price

        total_qty += qty
        total_price += price * qty

    return {'total_qty': total_qty, 'total_price': total_price}
