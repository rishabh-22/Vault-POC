from itertools import chain


def check_search(request, all_products, all_category, all_sub_category):
    data = request.GET['search']
    data_split = data.split(" [ ")
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
    return products
