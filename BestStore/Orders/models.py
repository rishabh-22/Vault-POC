import random
import string
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


def random_string_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator():
    order_new_id = int(random_string_generator())

    try:
        Order.objects.get(transaction_id=order_new_id)
        order_new_id = unique_order_id_generator()
    except Order.DoesNotExist:
        pass
    return order_new_id


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='IP')
    total_amount = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    coupons = models.CharField(max_length=50, blank=True, null=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='COD')
    shipping_address = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.transaction_id

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = unique_order_id_generator()

        super(Order, self).save(*args, **kwargs)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='IP')
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
