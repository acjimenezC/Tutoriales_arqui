from django.core.files.storage import default_storage
from django.http import HttpRequest

from .interfaces import ImageStorage


class ImageLocalStorage(ImageStorage):
    """Concrete implementation of ImageStorage using local file system."""
    
    def store(self, request: HttpRequest):
        """
        Store an image from the request to local storage.
        
        Args:
            request: The HTTP request object containing the image file.
            
        Returns:
            The URL of the stored image, or None if no image was provided.
        """
        profile_image = request.FILES.get('image')
        if profile_image:
            file_name = default_storage.save('uploaded_images/' + profile_image.name, profile_image)
            return default_storage.url(file_name)
        return None
      