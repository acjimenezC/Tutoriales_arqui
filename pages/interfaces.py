from abc import ABC, abstractmethod

from django.http import HttpRequest


class ImageStorage(ABC):
    """Abstract base class for image storage implementations."""
    
    @abstractmethod
    def store(self, request: HttpRequest):
        """Store an image from the request.
        
        Args:
            request: The HTTP request object containing the image.
        """
        pass