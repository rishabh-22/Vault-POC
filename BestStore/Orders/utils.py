# import random
# import string
#
# from Orders.models import Order
#
#
# def random_string_generator(size=10, chars=string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))
#
#
# def unique_order_id_generator(instance):
#     order_new_id = int(random_string_generator())
#
#     # Klass= instance.__class__
#     try:
#         order = Order.objects.get(id=order_new_id)
#     except Order.DoesNotExist:
#         return order_new_id
#
