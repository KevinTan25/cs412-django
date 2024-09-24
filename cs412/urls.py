"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf.urls.static import static 
from django.conf import settings # settings file that has all the settings in it

urlpatterns = [
    path("admin/", admin.site.urls),
    # Each app has its own path
    path("hw/", include("hw.urls")), ## we create the URL hw/, 
                                     ## and associate it with URLs in another file
    path("quotes/", include("quotes.urls")), # create the URL quotes and assosiate it with
                                            # URLS in quotes/urls.py
    path("formdata/", include("formdata.urls")) # Assosiate with formdata/urls.py
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
