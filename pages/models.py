"""
Django models for the pages application.

This module defines Product and Comment models for the online store.
"""

from django.db import models


class Product(models.Model):
    """
    Represents a product in the online store.
    
    Attributes:
        name: Product name (max 255 characters).
        description: Detailed product description (optional).
        price: Product price as a float value.
        created_at: Timestamp when product was created (auto-set).
        updated_at: Timestamp of last product update (auto-set).
    """
    
    name: str = models.CharField(max_length=255, help_text="Product name")
    description: str = models.TextField(
        blank=True, 
        null=True, 
        help_text="Product description"
    )
    price: float = models.FloatField(help_text="Product price")
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation timestamp"
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        help_text="Last update timestamp"
    )

    class Meta:
        """Meta options for Product model."""
        
        ordering: list = ['-created_at']
        verbose_name: str = 'Product'
        verbose_name_plural: str = 'Products'

    def __str__(self) -> str:
        """Return string representation of product."""
        return self.name


class Comment(models.Model):
    """
    Represents a comment on a product.
    
    Attributes:
        product: Foreign key reference to Product model.
        description: Comment text content.
    """
    
    product: models.ForeignKey = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="Product being commented on"
    )
    description: str = models.TextField(help_text="Comment text")

    class Meta:
        """Meta options for Comment model."""
        
        ordering: list = ['-id']
        verbose_name: str = 'Comment'
        verbose_name_plural: str = 'Comments'

    def __str__(self) -> str:
        """Return string representation of comment."""
        return self.description
