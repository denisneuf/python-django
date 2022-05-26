"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from app.views import TemplateView, RenderView, ItemsView, SingleItem, AllItems, ItemsUploadViews, SingleOrder, GetItem

urlpatterns = [
    path('admin/', admin.site.urls),
    path('render/', RenderView.as_view()),
    path('items/', ItemsView.as_view()),
    path('item/<str:order_id>', SingleOrder.as_view()),
    path('sp-api/catalog/get_item/<str:asin>/', GetItem.as_view()),
    path('api/', AllItems.as_view()),
    path('api/<int:person_id>/', SingleItem.as_view()),
    path('uploads/', ItemsUploadViews.as_view()),
    path('', TemplateView.as_view())
]
