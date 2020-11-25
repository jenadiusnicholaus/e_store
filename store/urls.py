from django.urls import path
from . import views

# After function views have been created in views.py file
# their urls are then configured in this file
# After creating this file we first need to import
# this file as seen on line 2

urlpatterns = [
    # inside here we provide the web url then the location
    # of the view itself (located at store/views) and lastly
    # giving all path names
    path('', views.store, name="store"),

    path('cart/', views.CartIterms.as_view(), name="cart"),
    path('checkout/', views.CheckOut.as_view(), name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('register/', views.register, name="register"),  # Added registered page

    # new modification
    path('product_details/<int:pk>/', views.Product_details, name="product_details"),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name="remove_from_cart"),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name="remove_from_cart"),

#     payement
    path('payment/<payment_option>/', views.Payment.as_view(), name="payment"),


]
