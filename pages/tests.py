"""
Tests (pruebas) de la app pages.
Aquí se escriben pruebas unitarias y funcionales.

Ejemplo de test:

from django.test import TestCase, Client
from django.urls import reverse

class PagesTestCase(TestCase):
    def test_home_loads(self):
        response = self.client.get(reverse('pages:home'))
        self.assertEqual(response.status_code, 200)
        
    def test_producto_detail(self):
        response = self.client.get(reverse('pages:producto_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
"""
from django.test import TestCase

# Escribe tus tests aquí
# Ejemplo:
# class HomeTestCase(TestCase):
#     def test_home_view(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
