"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
# Static imports a function and setting imports gives access to media url
from django.conf.urls.static import static
from django.conf import settings

# To connect our new urls from urls.py in our app folder we have to add include here
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('authentication.urls')),
]
# Appending to the list above and grabbing MEDIA_URL ('/images/') and setting that to media root which points to
# static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
