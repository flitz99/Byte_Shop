from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product

#Test sulla cancellazione di un prodotto
class DeleteProductViewTest(TestCase):

    def setUp(self):
        #Dati utente admin e prodotto di test
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product',
                                              type='Test Type',
                                              product_code='12345',
                                              productor='Test Productor',
                                              color='Test Color', 
                                              size='Test Size',
                                              weight=1.0,
                                              full_price=10.0,
                                              discount=0,
                                              final_price=10.0,
                                              quantity=1,
                                              supplier=self.user)

    def test_delete_product(self):
        self.client.login(username='testuser', password='testpassword') #Effettuo login
        response = self.client.post(reverse('products:delete_product', args=[self.product.product_code])) 
        
        self.assertEqual(response.status_code, 302) #Controllo status code
        self.assertEqual(response.url, '../allproducts')  #Controllo rerdirect
        self.assertFalse(Product.objects.filter(product_code='12345').exists()) #Controllo cancellazione prodotto

    def test_delete_nonexistent_product(self):
        self.client.login(username='testuser', password='testpassword') #Effettuo login
        response = self.client.post(reverse('products:delete_product', args=['nonexistent'])) 
        
        self.assertEqual(response.status_code, 200)  #Controllo status_code
        self.assertContains(response, "ERROR: product_code non valido")   #Controllo che dia errore di product_code non valido
        self.assertTrue(Product.objects.filter(product_code='12345').exists()) #Controllo prodotto non sia stato cancellato
    
