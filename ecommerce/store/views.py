from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import auth
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import datetime

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import jwt
from django_short_url.views import get_surl
from django_short_url.models import ShortURL

import random
from .serializers import *
from ecommerce.redis_connection import Redis
from .models import *

redis_object = Redis()

# Create your views here.
class LoginUser(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        username = request.data['username']
        phonenumber = request.data['phonenumber']
        token = jwt.encode({'username':username,'phonenumber':phonenumber}, 'SECRET_KEY').decode('utf-8')
        surl = get_surl(str(token))
        z = surl.split("/")
        surl = z[2]
        otp = random.randrange(100000,1000000)
        print(otp)
        redis_object.set(username,otp)
        return HttpResponseRedirect(reverse('otpvalidation',args=[surl]))

class Otpvalidation(GenericAPIView):
        serializer_class = OtpSerializer
        def post(self,request,surl):
            otp_valid = request.data['otp']
            url = ShortURL.objects.get(surl=surl)
            token = url.lurl
            user = jwt.decode(token,'SECRET_KEY')
            username = user['username']
            otp = str(redis_object.get(username).decode('UTF-8'))
            user = auth.authenticate(username=username)
            if otp_valid == otp and user is not None:
                auth.login(request,user)
                return Response("succesful logged in")
            return Response("invalide otp")
    
def logout(request):
    auth.logout(request)
    return HttpResponse('you are successfully logged out from your account')

class CreateProduct(GenericAPIView):
    serializer_class = ProductSerializer
    def post(self,request):
        if self.request.user.is_superuser:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response("product is created")
        return Response("invalid user")
       
class AddCart(GenericAPIView):
    serializer_class = CartSerializer
    def post(self,request):
        product = get_object_or_404(Product, pk=request.data['product'])
        quantity = int(request.data['quantity'])
        order_item,created = OrderItem.objects.get_or_create(product=product,
            customer=request.user,ordered=False)
        order_qs = Order.objects.filter(customer=request.user,closed=False)
        if order_qs.exists():
            order = order_qs[0]
            #check if orderitem in order or not
            if order.item.filter(product_id=request.data['product']).exists():
               order_item.quantity += quantity
               order_item.save()
               return Response("This item quantity was updated")
            else:
                order.item.add(order_item)
                return Response("This item add to your existed cart")
        else:
            ordered_date = datetime.datetime.now()
            order = Order.objects.create(customer=request.user,ordered_date=ordered_date)
            order.item.add(order_item)
            return Response("This item added to your created cart")

@api_view(["GET"])
def display_products(request):
    products = Product.objects.all().values()
    return Response({'Mobiles':products})

#display user cart items
class DisplayCart(GenericAPIView):
    queryset = Order.objects.all()
    def get(self,request):
        # filter user cart items
        items = OrderItem.objects.filter(customer=request.user,ordered=False)
        cart_items_count = items.count()
        cart_items = []
        for index in range(cart_items_count):
            cart_items.append({'name':items[index].product.name,
            "price":items[index].product.price,
            'quantity':items[index].quantity,
            'total_item_price':items[index].get_total_item_price()})
        dict_cart = {'Items':cart_items}
        return Response(dict_cart)

class OrderSummary(GenericAPIView):
    queryset = Order.objects.all()
    def get(self,request):
        # filter user cart items
        items = OrderItem.objects.filter(customer=request.user,ordered=False)
        cart_items_count = items.count()
        cart_items = []
        cart_total_amount = 0
        for index in range(cart_items_count):
            cart_items.append({'name':items[index].product.name,
            "price":items[index].product.price,
            'quantity':items[index].quantity,
            'total_item_price':items[index].get_total_item_price()})
            cart_total_amount += cart_items[index]['total_item_price']
        dict_cart = {"Items Count":cart_items_count,'Total Amount':cart_total_amount,'Items':cart_items}
        return Response(dict_cart)

@api_view(['GET'])
def remove_cart_items(request,product_id):
    product = get_object_or_404(Product, pk=product_id)
    order_qs = Order.objects.filter(customer=request.user,closed=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if orderitem in order or not
        if order.item.filter(product_id=product_id).exists():
            order_item = OrderItem.objects.filter(
                product=product,customer=request.user,ordered=False)[0]
            order.item.remove(order_item)
            return Response("This item removed from your cart")
        else:
            return Response("This item not in your cart")
    else:
        return Response("you don't have an active order")

@api_view(['GET'])
def remove_single_cart_item(request,product_id):
    product = get_object_or_404(Product, pk=product_id)
    order_qs = Order.objects.filter(customer=request.user,closed=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if orderitem in order or not
        if order.item.filter(product_id=product_id).exists():
            order_item = OrderItem.objects.filter(
                product=product,customer=request.user,ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.remove(order_item)
            return Response("This item removed from your cart")
        else:
            return Response("This item not in your cart")
    else:
        return Response("you don't have an active order")

class UpdateProduct(GenericAPIView):
    serializer_class = ProductSerializer
    def get(self,request,pk):
        item = Product.objects.get(pk=pk)
        if self.request.user.is_superuser:
            serializer = ProductSerializer(item)
            return Response(serializer.data)
        return Response("invalid user")
    def put(self,request,pk):
        item = Product.objects.get(pk=pk)
        serializer = ProductSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("This item details are updated")
        return Response("This product not existed")
    
class WishList(GenericAPIView):
    serializer_class = CartSerializer
    def post(self,request):
        product = get_object_or_404(Product, pk=request.data['product'])
        quantity = int(request.data['quantity'])
        order_item,created = OrderItem.objects.get_or_create(product=product,
            customer=request.user,ordered=False)
        wishlist_qs = Wishlist.objects.filter(customer=request.user)
        if wishlist_qs.exists():
            wishlist = wishlist_qs[0]
            #check if orderitem in order or not
            if wishlist.items.filter(product_id=request.data['product']).exists():
                order_item.quantity += quantity
                order_item.save()
                return Response("This item quantity was updated")
            else:
                wishlist.items.add(order_item)
                return Response("This item add to your existed cart")
        else:
            wishlist = Wishlist.objects.create(customer=request.user)
            wishlist.items.add(order_item)
            return Response("This item added to your created cart")
    
class DisplayWishList(GenericAPIView):
    queryset = Wishlist.objects.all()
    def get(self,request):
        # filter user wishlist items
        wishlist = Wishlist.objects.filter(customer=request.user)
        items = wishlist[0].items.filter(customer=request.user)
        wishlist_items_count = items.count()
        wishlist_items = []
        for index in range(wishlist_items_count):
            wishlist_items.append({'name':items[index].product.name,
            "price":items[index].product.price,
            'quantity':items[index].quantity,
            'total_item_price':items[index].get_total_item_price()})
        dict_wishlist = {"Items Count":wishlist_items_count,'Items':wishlist_items}
        return Response(dict_wishlist)

class Checkout(GenericAPIView):
    serializer_class = AddressSerializer
    def post(self,request):
        try:
            order = Order.objects.get(customer=request.user,closed=False)
            serializer = AddressSerializer(data=request.data)
            if serializer.is_valid():
                billing_address= serializer.save(customer=request.user)
                order.billingaddress = billing_address
                order.save()
                return redirect('order-summary')
        except ObjectDoesNotExist:
            return Response("You don't have active order")

class LastViewedItems(GenericAPIView):
    queryset = Product.objects.all()
    """Last 3 seen products should be shown on top even after reLogin, done using cache."""
    serializer_class = SearchSerializer
    def post(self,request):
        try:
            product = Product.objects.get(name=request.data['search'])
            request.user = ""
            print(redis_object.displaylist(request.user))
            redis_object.setlist(request.user,str(product))
            return Response(redis_object.displaylist(request.user))
        except ObjectDoesNotExist:
            return Response("product not existed")
