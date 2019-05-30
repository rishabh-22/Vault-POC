# from django.contrib import admin
# from product_master.models import Product
# from product_master.models import ProductImages
# from product_master.models import Category
# from product_master.models import SubCategory
# from product_master.models import Tags
#
#
# class ProductImage(admin.StackedInline):
#     model = ProductImages
#     initial_number = 1
#
#     def get_extra(self, request, obj=None, **kwargs):
#         return self.initial_number
#
#
# class CategoryNew(admin.TabularInline):
#     model = Category
#     initial_number = 1
#
#     def get_extra(self, request, obj=None, **kwargs):
#         return self.initial_number
#
#
# class SubcategoryNew(admin.StackedInline):
#     model = SubCategory
#     initial_number = 1
#
#     def get_extra(self, request, obj=None, **kwargs):
#         return self.initial_number
#
#
# class Tag(admin.StackedInline):
#     model = Tags
#     initial_number = 1
#
#     def get_extra(self, request, obj=None, **kwargs):
#         return self.initial_number
#
#
# class ProductAdmin(admin.ModelAdmin):
#
#     inlines = [
#         CategoryNew, Tag, ProductImage
#     ]
#
#
# admin.site.register(Product, ProductAdmin)
#
# # admin.site.register(ProductImages)
# # admin.site.register(Category)
# # admin.site.register(SubCategory)
# # admin.site.register(Tags)
#
#
#
#
#
#
