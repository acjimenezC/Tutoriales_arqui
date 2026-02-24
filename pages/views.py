"""
Django views for the pages application.

This module contains all view classes for handling requests related to products,
comments, and informational pages in the online store.
"""

from typing import Any, Dict

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class HomePageView(TemplateView):
    """Display the home page of the online store."""
    
    template_name: str = 'pages/home.html'


class AboutPageView(TemplateView):
    """Display the about page with company information."""
    
    template_name: str = 'pages/about.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Build context data for about page.
        
        Returns:
            Dictionary containing title, subtitle, description, and author.
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Your Name",
        })
        return context


class ContactPageView(TemplateView):
    """Display the contact page with company contact information."""
    
    template_name: str = 'pages/contact.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Build context data for contact page.
        
        Returns:
            Dictionary containing contact information (email, phone, address).
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact Us",
            "email": "info@onlinestore.com",
            "phone": "+1 (555) 123-4567",
            "address": "123 Main Street, New York, NY 10001, USA",
        })
        return context


class ProductIndexView(View):
    """Display the list of all available products."""
    
    template_name: str = 'pages/products/index.html'
    
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET request to display all products.
        
        Args:
            request: The HTTP request object.
            
        Returns:
            Rendered template with product list.
        """
        viewData: Dict[str, Any] = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all()
        }
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    """Display detailed information about a specific product."""
    
    template_name: str = 'pages/products/show.html'
    
    def get(self, request: HttpRequest, id: str) -> HttpResponse:
        """
        Handle GET request to display a product detail page.
        
        Args:
            request: The HTTP request object.
            id: Product ID from URL parameter.
            
        Returns:
            Rendered template with product details or redirect to home if invalid.
        """
        try:
            product_id: int = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product: Product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('pages:home'))
        
        viewData: Dict[str, Any] = {
            "title": f"{product.name} - Online Store",
            "subtitle": f"{product.name} - Product information",
            "product": product
        }
        return render(request, self.template_name, viewData)


class ProductListView(ListView):
    """Alternative ListView for displaying product list."""
    
    model: Any = Product
    template_name: str = 'pages/products/index.html'
    context_object_name: str = 'products'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Build context data for product list view.
        
        Returns:
            Dictionary with products, title, and subtitle.
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context


class ProductForm(forms.ModelForm):
    """Form for creating and updating products with validation."""
    
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    
    class Meta:
        """Meta configuration for ProductForm."""
        
        model: Any = Product
        fields: list = ['name', 'price']

    def clean_price(self) -> float:
        """
        Validate that price is greater than zero.
        
        Returns:
            The validated price value.
            
        Raises:
            ValidationError: If price is not greater than zero.
        """
        price: float | None = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price


class ProductCreateView(View):
    """Handle product creation (GET and POST requests)."""
    
    template_name: str = 'pages/products/create.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET request to display product creation form.
        
        Args:
            request: The HTTP request object.
            
        Returns:
            Rendered template with empty form.
        """
        form: ProductForm = ProductForm()
        viewData: Dict[str, Any] = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle POST request to create a new product.
        
        Args:
            request: The HTTP request object with form data.
            
        Returns:
            Redirect to success page if valid, or re-render form with errors.
        """
        form: ProductForm = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pages:product-created')
        else:
            viewData: Dict[str, Any] = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, viewData)


class ProductCreatedView(TemplateView):
    """Display success message after product creation."""
    
    template_name: str = 'pages/products/success.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Build context data for product created success page.
        
        Returns:
            Dictionary with success message title.
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['title'] = 'Product created'
        return context