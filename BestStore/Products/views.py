import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.generic import ListView
from .models import Product, Category, SubCategory, Newsletter, Tags, Wishlist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from collections import OrderedDict
from BestStore.settings import PRODUCTS_PER_PAGE,\
    PAGINATION_URL, EMAIL_SUBJECT, DUMMY_EMAIL
from .helper import *


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
        import pdb
        pdb.set_trace()
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


# def product_listings(request):
#     """
#         List products via custom pagination algorithm
#         :param request: Django's HTTP Request object
#         :return: Rendered product list view with pagination
#     """
#     if request.method == 'GET':
#         search_term = ""
#         try:
#             # Extract page parameter from page request and try to convert to int
#             page = int(request.GET.get('page', 1))
#         except ValueError:
#             # If page argument is an alphabet this will set the page to 1
#             page = 1
#         # Grab all categories for filtering purposes on web page
#         all_category = Category.objects.all()
#         all_sub_category = SubCategory.objects.all()
#         # Grab all products to paginate
#         all_products = Product.objects.all()
#
#         # Search functionality
#         if 'search' in request.GET:
#             all_products = check_search(request, all_products, all_category, all_sub_category)
#         # If no products are in database then we have nothing to show the user
#         # Set appropriate values for pagination parameters
#         products = list()
#         prods_per_page = PRODUCTS_PER_PAGE
#         total_pages = ((abs(len(all_products)) - 1) // prods_per_page) + 1
#         if page < 1:
#             page = 1
#         elif page > total_pages:
#             page = total_pages
#         start_index = (page - 1) * prods_per_page
#         end_index = start_index + prods_per_page
#         if len(all_products) != 0:
#             products = all_products[start_index: end_index]
#
#         # Set context variable for template to use to display the products and paginated navigation
#         info = {
#             'category': all_category,
#             'product': products,
#             'pages': range(1, total_pages + 1),
#             'current_page': page,
#             'prev': f'{PAGINATION_URL}{page - 1}' if page != 1 else '#',
#             'next': f'{PAGINATION_URL}{page + 1}' if page != total_pages else '#',
#             'search_term': search_term,
#         }
#         # Render template with context containing pagination details
#         return render(request, 'Products/products.html', context=info)

def product_listings(request):
    """
        List products via custom pagination algorithm
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
        category_selected = ''
        # Search functionality
        if 'search' in request.GET:
            all_products = check_search(request, all_products, all_category, all_sub_category)
        # If no products are in database then we have nothing to show the user
        # Set appropriate values for pagination parameters
        products = list()
        prods_per_page = PRODUCTS_PER_PAGE
        total_pages = ((abs(len(all_products)) - 1) // prods_per_page) + 1
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages
        start_index = (page - 1) * prods_per_page
        end_index = start_index + prods_per_page
        if len(all_products) != 0:
            products = all_products[start_index: end_index]
        search_type = request.GET.get('search', None)
        if search_type:
            search_type = search_type.split(' [ in ')
            search_name = search_type[0]
            search_type = search_type[1].split(' ]')[0]
            if search_type == 'Category':
                category_selected = Category.objects.filter(category__icontains=search_name)
                for i in range(0, len(category_selected[0].subcategory_set.all())):
                    products_in_category = category_selected[0].subcategory_set.all()[i].product_set.all()
                    products = list(chain(products, products_in_category))
            if search_type == 'Sub-Category':
                sub_category = SubCategory.objects.filter(title__icontains=search_name)[0]
                products = sub_category.product_set.all()
            if search_type == 'Products':
                products = Product.objects.filter(name__icontains=search_name)
        # Set context variable for template to use to display the products and paginated navigation
        info = {
            'category': all_category,
            'category_selected': category_selected,
            'product': products,
            'pages': range(1, total_pages + 1),
            'current_page': page,
            'prev': f'{PAGINATION_URL}{page - 1}' if page != 1 else '#',
            'next': f'{PAGINATION_URL}{page + 1}' if page != total_pages else '#',
            'search_term': search_term,
        }
        # Render template with context containing pagination details
        return render(request, 'Products/products.html', context=info)

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
            if not new_qty_above_max:
                # Sets new quantity to 0 in case quantity has gone negative
                sess['cart'][str(pk)]['qty'] = int((abs(new_qty)+new_qty)/2)
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
            results.append(result.name + " [ in Products]")
        for result in category_set:
            results.append(result.category + " [ in Category]")
        for result in sub_category_set:
            results.append(result.title + " [ in Sub-Category]")
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

#
# def filter_listings(request):
#     if request.method == 'GET':
#         try:
#             page = int(request.GET.get('page', 1))
#         except:
#             page = 1
#         products_list = []
#         products_by_price = []
#         all_category = Category.objects.all()
#         all_products = Product.objects.all()
#         all_sub_category = SubCategory.objects.all()
#         prods_per_page = 6
#         total_pages = ((abs(len(all_products))-1)//prods_per_page) + 1
#         filter_value = request.GET.get('filter_value', None)
#
#         if filter_value:
#             category_filter = all_category.filter(category__icontains=filter_value)
#             sub_category_filter = all_sub_category.filter(title__icontains=filter_value)
#         else:
#             category_filter = all_category.filter(category__icontains="Electronics")
#             sub_category_filter = all_sub_category.filter(title__icontains="mobile")
#
#         if category_filter:
#             for i in range(0, len(category_filter[0].subcategory_set.all())):
#                 products_in_category = category_filter[0].subcategory_set.all()[i].product_set.all()
#                 products_list = list(chain(products_list, products_in_category))
#         if sub_category_filter:
#             products_list = sub_category_filter[0].product_set.all()
#         min_value = request.GET.get('min_value')
#         max_value = request.GET.get('max_value')
#         price_filter = all_products.filter(price__range=(min_value, max_value))
#         for i in range(0, len(price_filter)):
#             products_by_price.append(price_filter[i])
#         products = set(products_list)
#         products_by_price_set = set(products_by_price)
#         products = products.intersection(products_by_price_set)
#         if products:
#             info = {
#                 'category': all_category,
#                 'product': products,
#                 'pages': range(1, total_pages + 1),
#                 'current_page': page,
#                 'prev': f'/products/?page={page - 1}' if page != 1 else '#',
#                 'next': f'/products/?page={page + 1}' if page != total_pages else '#',
#             }
#         else:
#             info = {
#                 'message': "No products found!"
#             }
#     return render(request, 'Products/product_listings.html', context=info)


def filter_listings(request):
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', 1))
        except:
            page = 1
        products_list = []
        products_by_price = []
        products_by_size = []
        products_by_color = []
        products_by_weight = []
        all_category = Category.objects.all()
        all_products = Product.objects.all()
        prods_per_page = 6
        total_pages = ((abs(len(all_products))-1)//prods_per_page) + 1
        filter_value = request.GET.get('filter_category', None)
        if filter_value:
            category_filter = all_category.filter(category__icontains=filter_value)
            sub_category_filter = SubCategory.objects.filter(title__icontains=filter_value)
        else:
            category_filter = all_category.filter(category__icontains="Electronics")
            sub_category_filter = SubCategory.objects.filter(title__icontains="mobile")
        if category_filter:
            for i in range(0, len(category_filter[0].subcategory_set.all())):
                products_in_category = category_filter[0].subcategory_set.all()[i].product_set.all()
                products_list = list(chain(products_list, products_in_category))
        if sub_category_filter:
            products_list = sub_category_filter[0].product_set.all()
        min_value = request.GET.get('min_price_val')
        max_value = request.GET.get('max_price_val')
        products = set(products_list)
        if min_value:
            price_filter = all_products.filter(price__range=(min_value, max_value))
            for i in range(0, len(price_filter)):
                products_by_price.append(price_filter[i])
            products_by_price_set = set(products_by_price)
            all_products = set(all_products)
            products = all_products.intersection(products_by_price_set)
        # min_weight_value = request.GET.get('min_weight_val')
        # max_weight_value = request.GET.get('max_weight_val')
        # weight_filter = all_products.filter(tags__weight__range=(min_weight_value, max_weight_value))
        # for i in range(0, len(weight_filter)):
        #     products_by_weight.append(weight_filter[i])
        # size = request.GET.get('filter_size')
        # size_filter = all_products.filter(tags__size__icontains=size)
        # for i in range(0, len(size_filter)):
        #     products_by_size.append(size_filter[i])
        # color = request.GET.get('filter_color')
        # color_filter = all_products.filter(tags__color__icontains=color)
        # for i in range(0, len(color_filter)):
        #     products_by_color.append(color_filter[i])
        # products_by_size_set = set(products_by_size)
        # products_by_color_set = set(products_by_color)
        # products_by_weight_set = set(products_by_weight)
        # products = products.intersection(products_by_weight_set)
        # products = products.intersection(products_by_size_set)
        # products = products.intersection(products_by_color_set)
        if products:
            info = {
                'category': all_category,
                'category_selected': category_filter,
                'product': products,
                'pages': range(1, total_pages + 1),
                'current_page': page,
                'prev': f'/products/?page={page - 1}' if page != 1 else '#',
                'next': f'/products/?page={page + 1}' if page != total_pages else '#',
            }
        else:
            info = {
                'message': "No products found!"
            }
    return render(request, 'Products/products.html', context=info)


@login_required
def wishlist_items(request):
    try:
        user = User.objects.get(email=request.user.email)
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
            return HttpResponse('Item Already Exists in your Wishlist')
        except Wishlist.DoesNotExist:
            Wishlist.objects.create(customer=request.user, item=item)
            return HttpResponse('Item Added To Wishlist successfully')
    else:
        return redirect('loginform')


@login_required
def add_wishlist_to_cart(request, product_id):
    #cart_add(request, product_id)
    delete_from_wishlist(request, product_id)
    return HttpResponse(wishlist_items(request))


@login_required
def delete_from_wishlist(request, pk):
    try:
        user = User.objects.get(email=request.user.email)
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

