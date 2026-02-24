"""
Formularios (Forms) de la app pages.
Define formularios para validación de datos.
"""
from django import forms


class ProductForm(forms.Form):
    """
    Formulario para crear/editar productos.
    Incluye validación personalizada con clean_price.
    """
    nombre = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del producto'
        }),
        error_messages={
            'required': 'El nombre es requerido',
            'max_length': 'El nombre no puede exceder 100 caracteres'
        }
    )
    
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        }),
        error_messages={
            'required': 'El precio es requerido',
            'invalid': 'El precio debe ser un número válido'
        }
    )
    
    descripcion = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Descripción del producto'
        }),
        error_messages={
            'required': 'La descripción es requerida'
        }
    )
    
    def clean_precio(self):
        """
        Validación personalizada para el campo precio.
        Solo acepta valores mayores a cero.
        """
        precio = self.cleaned_data.get('precio')
        
        if precio is not None and precio <= 0:
            raise forms.ValidationError(
                'El precio debe ser mayor a cero.'
            )
        
        return precio
    
    def clean_nombre(self):
        """
        Validación personalizada para el campo nombre.
        No puede estar vacío ni solo espacios.
        """
        nombre = self.cleaned_data.get('nombre')
        
        if nombre and not nombre.strip():
            raise forms.ValidationError(
                'El nombre no puede estar vacío.'
            )
        
        return nombre.strip() if nombre else nombre
