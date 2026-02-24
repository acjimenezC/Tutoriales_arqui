"""
Django admin configuration for the pages application.

This module registers models and configures their admin interfaces.
"""

from django.contrib import admin
from .models import Product, Comment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""
    
    list_display: tuple = ('name', 'price', 'created_at', 'updated_at')
    list_filter: tuple = ('created_at', 'price')
    search_fields: tuple = ('name', 'description')
    readonly_fields: tuple = ('created_at', 'updated_at')
    fieldsets: tuple = (
        ('Product Information', {
            'fields': ('name', 'description', 'price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model."""
    
    list_display: tuple = ('id', 'product', 'description')
    list_filter: tuple = ('product', 'id')
    search_fields: tuple = ('description', 'product__name')
    raw_id_fields: tuple = ('product',)