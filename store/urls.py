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
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('register/', views.register, name="register"), # Added registered page
]
