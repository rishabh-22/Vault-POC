from .models import Product
from .models import Category
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView


def home(request):
    """This will render the homepage"""
    return render(request, "Products/homepage.html")


def product_listings(request):
    """List products via pagination"""
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', 1))
        except:
            page = 1
        category = Category.objects.all()
        all_products = Product.objects.all()

        prods_per_page = 6

        total_pages = ((abs(len(all_products)) - 1) // prods_per_page) + 1
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages
        start_index = (page - 1) * prods_per_page
        end_index = start_index + prods_per_page
        products = all_products[start_index: end_index]

        info = {
            'category': category,
            'product': products,
            'pages': range(1, total_pages + 1),
            'current_page': page,
            'prev': f'/products/?page={page - 1}' if page != 1 else '#',
            'next': f'/products/?page={page + 1}' if page != total_pages else '#',
        }

        return render(request, 'Products/products.html', context=info)


def cart_add(request, pk):
    """Add products to card """
    if request.method == 'GET':
        sess = request.session
        qty = request.GET.get('qty', 1)

        sess['cart_qty'] = sess.get('cart_qty', 0) + qty
        sess['cart'] = sess.get('cart', list())

        already_in_cart = False
        for prod in sess['cart']:
            if prod['pk'] == pk:
                already_in_cart = True
                prod['qty'] += qty
        if not already_in_cart:
            sess['cart'].append({'pk': pk, 'qty': qty})
        return JsonResponse({'success': True})


def cart_empty(request, pk=0):
    """Empty the cart"""
    if request.method == 'GET':
        if pk == 0:
            sess = request.session
            sess['cart_qty'] = 0
            sess['cart'] = list()
            return JsonResponse({'success': True})


class ProductDetailView(DetailView):
    """Product Detail View """
    model = Product
    template_name = "Products/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qty'] = range(1, context['object'].quantity + 1)
        product = kwargs['object']
        context['image'] = product.productimages_set.all()
        return context


