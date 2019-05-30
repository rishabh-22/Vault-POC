import json
from itertools import chain
from django.views.generic import ListView
from .models import Product, Category, SubCategory, Newsletter
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from collections import OrderedDict
from BestStore.settings import PRODUCTS_PER_PAGE, PAGINATION_URL


def home(request):
    """
        This will render the homepage
        :param request: Django's HTTP Request object
        :return: Rendered homepage block to base template
    """
    featured = Product.objects.filter(is_featured=1).order_by('-modified_date')[:3]
    return render(request, "Products/homepage.html", {'featured_products': featured})


def product_listings(request):
    """
        List products via pagination
        :param request: Django's HTTP Request object
        :return: Rendered product list view with pagination
    """
    if request.method == 'GET':
        search_term = ""
        try:
            # Extract page parameter from page request and try to convert to int
            page = int(request.GET.get('page', 1))
        except ValueError:
            # If page argument is an alphabet this will set the page to 1
            page = 1
        # Grab all categories for filtering purposes on web page
        all_category = Category.objects.all()
        all_sub_category = SubCategory.objects.all()
        # Grab all products to paginate
        all_products = Product.objects.all()
        # If no products are in database then we have nothing to show the user
        if len(all_products) == 0:
            return Http404()
        # Set count of products to display for each individual page
        prods_per_page = PRODUCTS_PER_PAGE
        # Calculate total pages based on product count
        total_pages = ((abs(len(all_products)) - 1) // prods_per_page) + 1
        # Override page value if it is not a number in the valid range of pages
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages
        # Calculate start/end index for all_products list based on page value
        start_index = (page - 1) * prods_per_page
        end_index = start_index + prods_per_page
        # Use index slicing to get the products which are to be displayed on the rendered template
        products = all_products[start_index: end_index]
        # Set context variable for template to use to display the products and paginated navigation
        if 'search' in request.GET:
            products = []
            data = request.GET['search']
            data_split = data.split(" in ")
            search_term = data_split[0]
            products = all_products.filter(name__icontains=search_term)
            category_choice = all_category.filter(category__icontains=search_term)
            sub_category_choice = all_sub_category.filter(title__icontains=search_term)
            if sub_category_choice:
                products = sub_category_choice[0].product_set.all()
            if category_choice:
                for i in range(0, len(category_choice[0].subcategory_set.all())):
                    products_in_category = category_choice[0].subcategory_set.all()[i].product_set.all()
                    products = list(chain(products, products_in_category))

        info = {
            'category': all_category,
            'product': products,
            'pages': range(1, total_pages + 1),
            'current_page': page,
            'prev': f'{PAGINATION_URL}{page - 1}' if page != 1 else '#',
            'next': f'{PAGINATION_URL}{page + 1}' if page != total_pages else '#',
            'search_term': search_term,
        }
        # Render template with context containing pagination details
        return render(request, 'Products/products.html', context=info)


def cart_add(request, pk):
    """
       Add products to card
       :param request, pk: Django's HTTP Request object, Primary key of products to be added to cart
       :return: Success message
    """
    if request.method == 'GET':
        sess = request.session
        qty = request.GET.get('qty', 1)

        sess['cart_qty'] = sess.get('cart_qty', 0) + qty
        sess['cart'] = sess.get('cart', OrderedDict())

        if sess['cart'].get(pk, False):
            sess['cart'][pk]['qty'] += qty
        else:
            sess['cart'][pk] = {'qty': qty, 'pk': pk}

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
    """Remove a single item (possible multiple qty) from the cart"""
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


class FeaturedProduct(ListView):
    """
        Featured Products
        :param: Django's List View
        :return: Featured Page
    """
    model = Product
    template_name = "Products/featured.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Product model object to be used on detail page
        context['featured'] = Product.objects.filter(is_featured=1).order_by('-modified_date')
        return context


def autocompletemodel(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product_qs = Product.objects.filter(name__icontains=q)
        category_qs = Category.objects.filter(category__icontains=q)
        sub_category_qs = SubCategory.objects.filter(title__icontains=q)
        search_qs = list(chain(product_qs, category_qs, sub_category_qs))
        results = []
        for r in product_qs:
            results.append(r.name + " in Products")
        for r in category_qs:
            results.append(r.category + " in Category")
        for r in sub_category_qs:
            results.append(r.title + " in Sub-Category")
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def newsletter(request):
    if request.method == 'POST':
        mail = request.POST.get('news_letter_email')
        user = Newsletter.objects.create(email=mail)
        user.save()
        return redirect('homepage')
