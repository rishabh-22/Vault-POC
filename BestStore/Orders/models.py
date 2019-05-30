from django.db import models
from Products.models import Product
from django.contrib.auth.models import User

PAYMENT_CHOICES = (
    ('COD', 'COD'),
    ('Card', 'Card'),
    ('UPI', 'UPI'),
    ('Wallet', 'Wallet'),
)

ORDER_STATUS = (
    ('IP', 'In Processing'),
    ('OH', 'On Hold'),
    ('C', 'Cancelled'),
    ('OFD', 'Out For Delivery'),
    ('R', 'Returned'),
    ('D', 'Delivered'),
)


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    quantity = models.IntegerField()
    shipping_address = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=ORDER_STATUS)
