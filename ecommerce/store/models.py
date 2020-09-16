from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phonenumber = models.CharField(max_length=10)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.IntegerField()
    in_stock = models.BooleanField(default=False,blank=False,null=True)
    description = models.TextField(null=True,blank=True)
    #categories = models.CharField(max_length=100,null=True,blank=True)
    # image

    def __str__(self):
        return self.name
    

# a single order contains multiple orderitems   
# items in cart  
class OrderItem(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=1,null=True,blank=True)
    ordered = models.BooleanField(default=False, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def get_total_item_price(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return "{0}-{1}".format(self.product.name,self.customer.username)
# cart    


class Wishlist(models.Model):
    customer= models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(OrderItem) # items in wishlist
    start_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.customer.username

# address
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.CharField(max_length=200,null=False)
    city = models.CharField(max_length=50,null=False)
    state = models.CharField(max_length=50,null=False)
    zipcode = models.CharField(max_length=50,null=False)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ManyToManyField(OrderItem) #items in cart
    start_date = models.DateTimeField(auto_now_add=True)
    #open cart or not and it shows the changes of the cart status
    ordered_date = models.DateTimeField()
    closed = models.BooleanField(default=False,null=True,blank=False) 
    billingaddress = models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,null=True,blank=True) 
    # transcation id 

    def __str__(self):
        return self.customer.username