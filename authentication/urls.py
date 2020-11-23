from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.signUp.as_view(), name='sign_up'),
    path('sign_out/', views.user_sign_out, name='sign_out')
]
