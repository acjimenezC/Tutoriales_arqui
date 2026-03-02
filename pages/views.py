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
from .utils import ImageLocalStorage


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


class CartView(View):
    """Display and manage shopping cart."""
    
    template_name: str = 'pages/cart/index.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET request to display cart.
        
        Args:
            request: The HTTP request object.
            
        Returns:
            Rendered template with cart contents.
        """
        # Simulated database for products
        products: Dict[int, Dict[str, str]] = {
            121: {'name': 'Tv samsung', 'price': '1000'},
            11: {'name': 'Iphone', 'price': '2000'},
        }

        # Get cart products from session
        cart_products: Dict[int, Dict[str, str]] = {}
        cart_product_data: Dict[str, Any] = request.session.get('cart_product_data', {})

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        # Prepare data for the view
        view_data: Dict[str, Any] = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }
        return render(request, self.template_name, view_data)

    def post(self, request: HttpRequest, product_id: str) -> HttpResponseRedirect:
        """
        Handle POST request to add product to cart.
        
        Args:
            request: The HTTP request object.
            product_id: Product ID to add to cart.
            
        Returns:
            Redirect to cart index.
        """
        # Get cart products from session and add the new product
        cart_product_data: Dict[str, Any] = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = product_id
        request.session['cart_product_data'] = cart_product_data

        return redirect('pages:cart_index')


class CartRemoveAllView(View):
    """Handle removal of all products from cart."""

    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        """
        Handle POST request to remove all products from cart.
        
        Args:
            request: The HTTP request object.
            
        Returns:
            Redirect to cart index.
        """
        # Remove all products from cart in session
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']

        return redirect('pages:cart_index')


def ImageViewFactory(image_storage):
    """
    Factory function to create an ImageView with injected image storage.
    
    Args:
        image_storage: An instance of ImageStorage implementation.
        
    Returns:
        ImageView class configured with the provided image storage.
    """
    
    class ImageView(View):
        """Display and manage image uploads."""
        
        template_name: str = 'pages/images/index.html'

        def get(self, request: HttpRequest) -> HttpResponse:
            """
            Handle GET request to display image upload form.
            
            Args:
                request: The HTTP request object.
                
            Returns:
                Rendered template with stored image URL.
            """
            image_url: str = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request: HttpRequest) -> HttpResponseRedirect:
            """
            Handle POST request to store uploaded image.
            
            Args:
                request: The HTTP request object containing the image file.
                
            Returns:
                Redirect to image index page.
            """
            image_url: str = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('pages:image_index')

    return ImageView


class ImageViewNoDI(View):
    """Display and manage image uploads without dependency injection."""
    
    template_name: str = 'pages/images/index.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET request to display image upload form.
        
        Args:
            request: The HTTP request object.
            
        Returns:
            Rendered template with stored image URL.
        """
        image_url: str = request.session.get('image_url', '')
        return render(request, self.template_name, {'image_url': image_url})

    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        """
        Handle POST request to store uploaded image.
        
        Args:
            request: The HTTP request object containing the image file.
            
        Returns:
            Redirect to image index page.
        """
        image_storage = ImageLocalStorage()
        image_url = image_storage.store(request)
        request.session['image_url'] = image_url
        return redirect('pages:image_index')