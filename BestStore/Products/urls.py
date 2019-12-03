from django.urls import path
from .views import (
    cart_update, cart_empty, home, product_listings, ProductDetailView, 
    cart_item_remove, FeaturedProduct, auto_complete, filter_listings,
    wishlist_items, add_to_wishlist, delete_from_wishlist,
)


urlpatterns = [
    path('', home, name="homepage"),
    path('products/', product_listings, name="products"),
    path('products/<slug>/', ProductDetailView.as_view(), name="detail"),
    path('api/product/cart/update/<int:pk>/', cart_update, name='cart-update'),
    path('api/product/cart/empty/', cart_empty, name='cart-empty-all'),
    path('api/product/cart/empty/<int:pk>/', cart_empty, name='cart-empty'),
    path('api/product/cart/remove/<int:pk>/', cart_item_remove, name='cart-item-remove'),
    path('featured/', FeaturedProduct.as_view(), name='featured'),
    path('ajax/search/', auto_complete, name='auto'),
    path('wishlist/', wishlist_items, name='wishlist'),
    path('wishlist/add/<int:pk>/', add_to_wishlist, name='add_to_wishlist'),
    path('delete-item/<int:pk>/', delete_from_wishlist, name='delete_from_wishlist'),
]
