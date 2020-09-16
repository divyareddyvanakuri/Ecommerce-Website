"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginUser.as_view(),name='login'),
    path('otp/<slug:surl>',views.Otpvalidation.as_view(),name='otpvalidation'),
    path('logout/',views.logout,name='logout'),
    path('createprodcut/',views.CreateProduct.as_view(),name="createprodcut"),
    path('updateproduct/<int:pk>/',views.UpdateProduct.as_view(),name="update-product-details"),
    path('productslist/',views.display_products,name="display-list-of-products"),
    path('addcart/',views.AddCart.as_view(),name="addcart"),
    path('displaycart/',views.DisplayCart.as_view(),name="display-cart"),
    path('removecartitem/<int:product_id>/',views.remove_cart_items,name="remove-cart-item"),
    path('wishlist/',views.WishList.as_view(),name="wishlis"),
    path('displaywishlist/',views.DisplayWishList.as_view(),name="display-wishlis"),
    path('addshippingaddress/',views.Checkout.as_view(),name="add-shipping-address"),
    path('ordersummary/',views.OrderSummary.as_view(),name="order-summary"),
    path('search/',views.LastViewedItems.as_view(),name='last-viewed-items'),

]
