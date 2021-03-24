from django.test import TestCase
from .models import City
from .forms import CityForm
# Create your tests here.

class TestCity(TestCase):
    
    def setUp(self):
        self.city = City.objects.create(name='Test')
        
    def test_city_create(self):
        self.assertEqual(self.city.name, 'Test')
    
    def test_city_forms(self):
        city_form = CityForm(instance=self.city)
        assert False is city_form.is_valid()
        