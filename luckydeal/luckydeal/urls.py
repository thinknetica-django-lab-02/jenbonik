"""luckydeal URL Configuration

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
from django.conf import settings

from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.flatpages.views import flatpage
from django.contrib.staticfiles.urls import static

from django.urls import path

from main.views import GoodListView
from main.views import GoodCreate
from main.views import GoodDetailView
from main.views import GoodUpdate

from main.views import home
from main.views import user_profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = 'home'),
    path('about/', flatpage, {'url': '/about/'}, name = 'about'),
    path('contacts/', flatpage, {'url': '/contacts/'}, name = 'contacts'),
    path('goods/', GoodListView.as_view(), name = 'goods'),
    path('goods/add', GoodCreate.as_view(), name = 'good_add'),
    path('goods/<pk>/edit', GoodUpdate.as_view(), name = 'good_edit'),
    path('goods/<pk>', GoodDetailView.as_view(), name = 'good_detail'),
    path('accounts/login/', LoginView.as_view(), name = 'login'),
    path('accounts/profile/', user_profile, name = 'user_profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
