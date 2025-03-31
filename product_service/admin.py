from django.contrib import admin
from .models import Category, Product, Book, Phone, Clothing

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Book)
admin.site.register(Phone)
admin.site.register(Clothing)