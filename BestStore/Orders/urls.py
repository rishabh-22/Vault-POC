from django.urls import path
from .views import checkout, orders, order_display, cancel_order


urlpatterns = [
    path('checkout/', checkout, name="checkout"),
    path('orders/', orders, name='orders'),
    path('your_order/', order_display, name='order_display'),
    path('cancle_order/<int:pk>/', cancel_order, name="cancle_order"),

]
