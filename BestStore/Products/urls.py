from django.urls import path
from .views import (
    cart_add, cart_empty, home, product_listings, ProductDetailView, 
    cart_item_remove, FeaturedProduct, autocompletemodel
)

urlpatterns = [
    path('', home, name="homepage"),
    path('products/', product_listings, name="products"),
    path('products/<int:pk>/', ProductDetailView.as_view(), name="detail"),
    path('api/product/cart/add/<int:pk>/', cart_add, name='cart-add'),
    path('api/product/cart/empty/', cart_empty, name='cart-empty-all'),
    path('api/product/cart/empty/<int:pk>/', cart_empty, name='cart-empty'),
    path('api/product/cart/remove/<int:pk>/', cart_item_remove, name='cart-item-remove'),
    path('featured/', FeaturedProduct.as_view(), name='featured'),
    path('ajax/search/', autocompletemodel, name='auto'),
    #path('/newsletter/', newsletter, name='newsletter'),
]
