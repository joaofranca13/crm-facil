from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """Model that register customer's data"""
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, verbose_name='Nome')
    phone = models.CharField(max_length=255, null=True, verbose_name='Fone:')
    email = models.CharField(max_length=255, null=True, verbose_name='Email')
    date_created = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(
        default='profile_placeholder.jpeg',
        null=True, blank=True,
        verbose_name='Foto de Perfil'
    )

    def __str__(self):
        if self.name is None:
            return 'ERROR-CUSTOMER NAME IS NULL'
        return self.name


class Tag(models.Model):
    """Model that register tags"""
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Model that register product's data"""
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )
    name = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True, choices=CATEGORY)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        if self.name is None:
            return 'ERROR-PRODUCT NAME IS NULL'
        return self.name


class Order(models.Model):
    """Model that register order's data"""
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL, verbose_name='Cliente')
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL, verbose_name='Produto')
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação')
    status = models.CharField(
        max_length=255, null=True, choices=STATUS, verbose_name='Status')

    def __str__(self):
        if self.product.name is None:
            return 'ERROR-ORDER-PRODUCT NAME IS NULL'
        return self.product.name
