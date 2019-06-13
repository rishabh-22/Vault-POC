import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import render_to_string
from django.views.generic import ListView
from .models import Product, Category, SubCategory, Newsletter, Tags, Wishlist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from collections import OrderedDict
from BestStore.settings import PRODUCTS_PER_PAGE, \
    PAGINATION_URL, EMAIL_SUBJECT, DUMMY_EMAIL


def home(request):
    """
        This will render the homepage
        :param request: Django's HTTP Request object
        :return: Rendered homepage block to base template
    """
    featured = Product.objects.filter(is_featured=1).order_by('-modified_date')[:3]
    all_category = Category.objects.all()
    context = {'featured_products': featured, 'category': all_category}

    # Save newsletter information
    if request.method == 'POST':
        mail = request.POST.get('news_letter_email')
        try:
            user = Newsletter.objects.get(email=mail)
            context['mail_exists'] = False
        except Exception:
            user = Newsletter.objects.create(email=mail)
            user.save()
            context['Success'] = True
            plain_message = "Successfully Subscribed to our news letter!"
            html_message = render_to_string('General/newsletter.html')
            send_mail(EMAIL_SUBJECT,
                      plain_message,
                      DUMMY_EMAIL,
                      [mail],
                      html_message=html_message,
                      fail_silently=False)
        return render(request, "Products/homepage.html", context)

    return render(request, "Products/homepage.html", context)


def product_listings(request):
    """
        List products via custom pagination algorithm
        :param request: Django's HTTP Request object
        :return: Rendered product list view with pagination
    """
    search_term = ""
    filter = dict()
    filter_tags = dict()
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
    filter['product'] = all_products
    # Search functionality
    if 'search' in request.GET:
        filter = product_search(request)
    if 'filter_category' in request.GET or 'filter_sub_category' in request.GET:
        filters = filter_listings(request)
        if filters.get('filter_tag'):
            filter_tags = filters['filter_tag']
            filter_detail = filters['filter_detail']
            del filters['filter_detail']
            del filters['filter_tag']
        filter['product'] = Product.objects.filter(**filters)
        if filter_detail:
            product_detail = set()
            product_details = Tags.objects.filter(**filter_detail)
            for prod in product_details:
                product_detail.add(prod.product)
            filter['product'] = set(filter['product']).intersection(product_detail)
        filter['category'] = request.GET.get('filter_category')
        filter['sub_category'] = request.GET.get('filter_sub_category')
    # If no products are in database then we have nothing to show the user
    # Set appropriate values for pagination parameters
    paginator = Paginator(list(filter['product']), 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Set context variable for template to use to display the products and paginated navigation

    # import pdb; pdb.set_trace()
    if not filter.get('product'):


        info = {
            'category': all_category,
            'message': "No products found!",
            'filter_tags': filter_tags,
        }
    else:
        info = {
            'category': all_category,
            'category_selected': filter.get('category'),
            'sub_category_selected': filter.get('sub_category'),
            'product': filter.get('product'),
            'products': products,
            'search_term': search_term,
        }

    # Render template with context containing pagination details
    return render(request, 'Products/products.html', context=info)


def product_search(request):
    filter = dict()
    search_type = request.GET.get('search', None)
    try:
        search_type = search_type.split(' [ in ')
        search_name = search_type[0]
        search_type = search_type[1].split(' ]')[0]
        if search_type == 'Category':
            filter['category__category'] = search_name
        if search_type == 'Sub-Category':
            filter['subcategory__title'] = search_name
        filter['product'] = Product.objects.filter(**filter)
        if filter['category__category']:
            filter['category'] = search_name
        else:
            filter['sub_category'] = search_name
    except IndexError:
        search_type = 'Products'
    if search_type == 'Products':
        products = Product.objects.filter(name__icontains=search_name)
        filter['product'] = products
    return filter


# def filter_products(**filter):
#     products = set(Product.objects.all())
#     if filter.get('category'):
#         products_in_category = set(Category.objects.filter(category__icontains=filter['category'])[0].product_set.all())
#         products = products.intersection(products_in_category)
#     if filter.get('sub_category'):
#         products_in_sub_category = set(
#             SubCategory.objects.filter(title__icontains=filter['sub_category'])[0].product_set.all())
#         products = products.intersection(products_in_sub_category)
#     if filter.get('min_price_value'):
#         products_by_price = []
#         price_filter = Product.objects.filter(price__range=(filter['min_price_value'], filter['max_price_value']))
#         for i in range(0, len(price_filter)):
#             products_by_price.append(price_filter[i])
#         products = products.intersection(set(products_by_price))
#     if filter.get('min_weight_value'):
#         products_by_weight =[]
#         weight_filter = Product.objects.filter(tags__weight__range=(filter['min_weight_value'], filter['max_weight_value']))
#         for i in range(0, len(weight_filter)):
#             products_by_weight.append(weight_filter[i])
#         products = products.intersection(set(products_by_weight))
#     if filter.get('size') and filter.get('size') != 'All':
#         products_by_size = []
#         size_filter = Product.objects.filter(tags__size__icontains=filter['size'])
#         for i in range(0, len(size_filter)):
#             products_by_size.append(size_filter[i])
#         products = products.intersection(set(products_by_size))
#     if filter.get('color') and filter.get('size') != 'All':
#         products_by_color = []
#         color_filter = Product.objects.filter(tags__color__icontains=filter['color'])
#         for i in range(0, len(color_filter)):
#             products_by_color.append(color_filter[i])
#         products = products.intersection(set(products_by_color))
#     filter['product'] = products
#     return filter


def filter_listings(request):
        filter_detail = dict()
        filter = dict()
        filer_tag = []
        if request.GET.get('filter_category'):
            filter['category__category'] = request.GET.get('filter_category', None)
            filer_tag.append(filter['category__category'])
        if request.GET.get('filter_sub_category'):
            filter['subcategory__title'] = request.GET.get('filter_sub_category', None)
            filer_tag.append(filter['subcategory__title'])
        if request.GET.get('min_price_val'):
            filter['price__gte'] = request.GET.get('min_price_val', None)
            filer_tag.append(filter['price__gte'])
        if request.GET.get('max_price_val'):
            filter['price__lte'] = request.GET.get('max_price_val', None)
        if request.GET.get('min_weight_val'):
            filter_detail['weight__gte'] = request.GET.get('min_weight_val')
            filer_tag.append(filter_detail['weight__gte'])
        if request.GET.get('min_weight_val'):
            filter_detail['weight__lte'] = request.GET.get('max_weight_val')
        if request.GET.get('filter_size'):
            filter_detail['size'] = request.GET.get('filter_size')
            filer_tag.append(filter_detail['size'])
        if request.GET.get('filter_color'):
            filter_detail['color'] = request.GET.get('filter_color')
            filer_tag.append(filter_detail['color'])
        filter['filter_tag'] = filer_tag
        filter['filter_detail'] = filter_detail
        return filter


def cart_update(request, pk):
    """
       Add/Remove single product (possible multiple qty of product) to cart
       :param   request: Django's HTTP Request object,
                pk: Primary key of 
                    products to be added to cart
       :return: Success message
    """
    if request.method == 'GET':

        sess = request.session
        qty = request.GET.get('qty', False)
        if qty:
            # Initialize a cart and its qty in session if they don't exist
            sess['cart_qty'] = sess.get('cart_qty', 0) + int(qty)
            sess['cart'] = sess.get('cart', OrderedDict())
            # In case the it is add to cart and product not already in cart
            new_cart_item = {'qty': 0, 'pk': str(pk)}
            # Update cart item quantity of new/existing item
            sess['cart'][str(pk)] = sess['cart'].get(str(pk), new_cart_item)
            new_qty = sess['cart'][str(pk)]['qty'] + int(qty)
            new_qty_above_max = Product.objects.get(pk=pk).quantity < new_qty
            # import pdb; pdb.set_trace()
            if not new_qty_above_max:
                # Sets new quantity to 0 in case quantity has gone negative
                sess['cart'][str(pk)]['qty'] = int((abs(new_qty) + new_qty) / 2)
                return JsonResponse({'success': True})
            return JsonResponse({
                'success': False,
                'msg': 'Max quantity of this product has already been added.'
            })


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
        try:
            del cart[str(pk)]
            request.session.modified = True
            return JsonResponse({'success': True})
        except KeyError:
            return JsonResponse({'success': False})


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
        specifications = Tags.objects.get(product=product.id)
        context['image'] = product.productimages_set.all()
        context['specification'] = {'Size': specifications.size,
                                    'Color': specifications.color,
                                    'Weight': specifications.weight}

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


def auto_complete(request):
    # Search auto complete functionality
    if request.is_ajax():
        term = request.GET.get('term', '')
        product_set = Product.objects.filter(name__icontains=term)
        category_set = Category.objects.filter(category__icontains=term)
        sub_category_set = SubCategory.objects.filter(title__icontains=term)
        results = []
        for result in product_set:
            results.append(result.name + " [ in Products ]")
        for result in category_set:
            results.append(result.category + " [ in Category ]")
        for result in sub_category_set:
            results.append(result.title + " [ in Sub-Category ]")
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required
def wishlist_items(request):
    try:
        items = Wishlist.objects.filter(customer=request.user)
        if not len(items) == 0:
            context = {'items': items}
        else:
            context = {'no_item_found': True}
    except User.DoesNotExist:
        return redirect('Auth:loginform')
    return render(request, 'Products/wishlist.html', context)


def add_to_wishlist(request, pk):
    if request.user.is_authenticated:
        item = Product.objects.get(id=pk)
        try:
            Wishlist.objects.get(item=item)
            messages.error(request, "Item Already Exists in your Wishlist")
            return redirect('wishlist')
        except Wishlist.DoesNotExist:
            Wishlist.objects.create(customer=request.user, item=item)
            messages.error(request, "Item Added To Wishlist successfully")
            return redirect('products')
    else:
        return redirect('loginform')


# @login_required
# def add_wishlist_to_cart(request, product_id):
#     delete_from_wishlist(request, product_id)
#     return HttpResponse(wishlist_items(request))


@login_required
def delete_from_wishlist(request, pk):
    try:
        item = Wishlist.objects.get(item_id=pk)
        item.delete()
        items = Wishlist.objects.filter(customer=request.user)
        context = {'items': items}

        if not len(items) == 0:
            if request.method == 'POST':
                Wishlist.objects.filter(id=pk).delete()
                context = {'items': items}
        else:
            context = {'no_item_found': True}
        return HttpResponse(wishlist_items(request))
    except User.DoesNotExist:
        return redirect('loginform')
