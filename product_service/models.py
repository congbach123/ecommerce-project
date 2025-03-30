from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Book(Product):
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    publisher = models.CharField(max_length=200)
    pages = models.PositiveIntegerField(default=0)
    
class Phone(Product):
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    screen_size = models.DecimalField(max_digits=3, decimal_places=1)
    memory = models.PositiveIntegerField(help_text="Memory in GB")
    storage = models.PositiveIntegerField(help_text="Storage in GB")
    
class Clothing(Product):
    brand = models.CharField(max_length=100)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unisex'),
    ])