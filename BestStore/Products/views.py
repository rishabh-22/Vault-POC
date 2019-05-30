from .models import Product, Category
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.generic.detail import DetailView
from collections import OrderedDict
from BestStore.settings import PRODUCTS_PER_PAGE, PAGINATION_URL


def home(request):
    """
        This will render the homepage
        :param request: Django's HTTP Request object
        :return: Rendered homepage block to base template
    """
    return render(request, "Products/homepage.html")


def product_listings(request):
    """
        List products via custom pagination algorithm
        :param request: Django's HTTP Request object
        :return: Rendered product list view with pagination
    """
    if request.method == 'GET':
        # Set the page to 1 if page parameter in get request can't be converted to int or if it is missing
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1
        # Grab categories for filtering on listings page
        category = Category.objects.all()
        all_products = Product.objects.all()
        # If no products are in database then we have nothing to show the user
        if len(all_products) == 0:
            return Http404()
        # Set appropriate values for pagination parameters
        prods_per_page = PRODUCTS_PER_PAGE
        total_pages = ((abs(len(all_products)) - 1) // prods_per_page) + 1
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages
        start_index = (page - 1) * prods_per_page
        end_index = start_index + prods_per_page
        products = all_products[start_index: end_index]
        # Assign dict to be passed into the context parameter of the django render function
        info = {
            'category': category,
            'product': products,
            'pages': range(1, total_pages + 1),
            'current_page': page,
            'prev': f'{PAGINATION_URL}{page - 1}' if page != 1 else '#',
            'next': f'{PAGINATION_URL}{page + 1}' if page != total_pages else '#',
        }
        return render(request, 'Products/products.html', context=info)


def cart_add(request, pk):
    """
       Add single product (possible multiple qty of product) to cart
       :param   request: Django's HTTP Request object,
                pk: Primary key of 
                    products to be added to cart
       :return: Success message
    """
    if request.method == 'GET':
        sess = request.session
        qty = request.GET.get('qty', 1)
        # Initialize a cart and its total qty in session if they don't exist
        sess['cart_qty'] = sess.get('cart_qty', 0) + qty
        sess['cart'] = sess.get('cart', OrderedDict())

        new_cart_item = {'qty': 0, 'pk': pk}
        sess['cart'][pk] = sess['cart'].get(pk, new_cart_item)
        sess['cart'][pk]['qty'] += qty

        return JsonResponse({'success': True})


def cart_empty(request, pk=0):
    """Empty the cart"""
    if request.method == 'GET':
        if pk == 0:
            sess = request.session
            sess['cart_qty'] = 0
            sess['cart'] = OrderedDict()
            return JsonResponse({'success': True})


def cart_item_remove(request, pk=0):
    """Remove a single item (possible multiple qty of item) from the cart"""
    if request.method == 'GET' and pk > 0:
        cart = request.session['cart']
        qty = request.GET.get('qty', False)

        cart_item = cart.get(str(pk), False)
        if cart_item:
            cart_item['qty'] -= int(qty)
            if cart_item['qty'] <= 0:
                del cart[str(pk)]
                request.session.modified = True
        
        return JsonResponse({'success': True})


class ProductDetailView(DetailView):
    """
        Product Detail View
        :param:
        :return: A detailed view page for a specific product using slug
    """

    model = Product
    template_name = "Products/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adding list range to the template context so that user can see dynamic quantity options
        context['qty'] = range(1, context['object'].quantity + 1)
        # Product model object to be used on detail page
        product = kwargs['object']
        context['image'] = product.productimages_set.all()
        return context


