"""
URL configuration for the pages application.

This module defines URL patterns for pages app views.
Routes are included in the main project urls.py.
"""

from django.urls import path
from .views import (
    HomePageView,
    AboutPageView,
    ContactPageView,
    ImageViewFactory,
    ImageViewNoDI,
    ProductIndexView,
    ProductShowView,
    ProductCreateView,
    ProductCreatedView,
    CartView,
    CartRemoveAllView,
)
from .utils import ImageLocalStorage

app_name = 'pages'

# Create image storage instance for dependency injection
image_storage = ImageLocalStorage()

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('products/', ProductIndexView.as_view(), name='index'),
    path('products/create/', ProductCreateView.as_view(), name='create'),
    path('products/created/', ProductCreatedView.as_view(), name='product-created'),
    path('products/<str:id>', ProductShowView.as_view(), name='show'),
    path('cart/', CartView.as_view(), name='cart_index'),
    path('cart/add/<str:product_id>', CartView.as_view(), name='cart_add'),
    path('cart/removeAll', CartRemoveAllView.as_view(), name='cart_removeAll'),
    path('image/', ImageViewFactory(image_storage).as_view(), name='image_index'),
    path('image/save', ImageViewFactory(image_storage).as_view(), name='image_save'),
    path('imagenotdi/', ImageViewNoDI.as_view(), name='imagenodi_index'),
    path('imagenotdi/save', ImageViewNoDI.as_view(), name='imagenodi_save'),
]
   
