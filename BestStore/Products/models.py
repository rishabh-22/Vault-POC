from django.db import models
from django.contrib.auth.models import User
from .util import unique_slug_generator

CATEGORY_CHOICES = (
    ('Electronic', 'Electronic'),
    ('Cloth', 'Cloth'),
    ('Kid', 'Kid'),
)

SUB_CATEGORY_CHOICES = (
    ('Mobile', 'Mobile'),
    ('TV', 'TV'),
    ('Shirt', 'Shirt'),
    ('Pant', 'Pant'),
    ('Toy', 'Toy'),
    ('Book', 'Book'),
)

COLOR_CHOICES = (
    ('Black', 'Black'),
    ('Blue', 'Blue'),
    ('Red', 'Red'),
    ('Green', 'Green'),
    ('White', 'White'),
    ('Rose Gold', 'Rose Gold'),
    ('Grey', 'Grey'),
)

PAYMENT_CHOICES = (
    ('COD', 'COD'),
    ('Credit Card', 'Credit Card'),
    ('Debit Card', 'Debit Card'),
    ('WALLET', 'WALLET'),
    ('BTC', 'BTC'),
)


class Category(models.Model):
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.category


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, choices=SUB_CATEGORY_CHOICES)

    def __str__(self):
        return self.title

      
class Product(models.Model):
    merchant = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super(Product, self).save(*args, **kwargs)


class Tags(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, default=1)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    weight = models.CharField(max_length=20)


class ProductImages(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()


# class Orders(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE)
#     order_date = models.DateTimeField(auto_now_add=True)
#     payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
#     quantity = models.IntegerField()
#

class Newsletter(models.Model):
    email = models.EmailField(max_length=70, null=False)


