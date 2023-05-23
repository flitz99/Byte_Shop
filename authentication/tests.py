from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from authentication.models import Client
from cart.models import Carrello
from .forms import ClientCreationForm, CustomUserCreationForm
from django.contrib.auth import get_user_model

#Test registrazione cliente
class ClientRegistrationTest(TestCase):
    def setUp(self):
        self.user_type = 'client'  # Imposto il valore di user_type
        self.url = reverse('authentication:signup', kwargs={'user_type': self.user_type}) 

    def test_client_registration(self):
        
        #Dati utente cliente di test
        user_data = {
            'username': 'clientuser',
            'email': 'clientuser@example.com',
            'first_name': 'clientname',
            'last_name': 'clientsurname',
            'telephone': '1234567890',
            'address': 'client address',
            'house_number': 1,
            'city': 'City',
            'province': 'Province',
            'cap': 11111,
            'birth_date': '1990-01-01',
            'password1': 'clientpassword',
            'password2': 'clientpassword',
        }

        #Controllo validità dei dati inseriti nel form di registrazione di un cliente
        form = ClientCreationForm(data=user_data)
        self.assertTrue(form.is_valid()) 

        cleaned_data = form.cleaned_data
        self.assertTrue('username' in cleaned_data)
        self.assertTrue('email' in cleaned_data)
        self.assertTrue('first_name' in cleaned_data)
        self.assertTrue('last_name' in cleaned_data)
        self.assertTrue('telephone' in cleaned_data)
        self.assertTrue('address' in cleaned_data)
        self.assertTrue('house_number' in cleaned_data)
        self.assertTrue('city' in cleaned_data)
        self.assertTrue('province' in cleaned_data)
        self.assertTrue('cap' in cleaned_data)
        self.assertTrue('birth_date' in cleaned_data)
        self.assertTrue('password1' in cleaned_data)
        self.assertTrue('password2' in cleaned_data)
        self.assertTrue('profile_image' in cleaned_data)

        #Verifico condizioni sui campi del form
        self.assertTrue(form.fields['username'].required)
        self.assertTrue(form.fields['email'].required)
        self.assertTrue(form.fields['first_name'].required)
        self.assertTrue(form.fields['last_name'].required)
        self.assertTrue(form.fields['telephone'].required)
        self.assertTrue(form.fields['address'].required)
        self.assertTrue(form.fields['house_number'].required)
        self.assertTrue(form.fields['city'].required)
        self.assertTrue(form.fields['province'].required)
        self.assertTrue(form.fields['cap'].required)
        self.assertTrue(form.fields['birth_date'].required)
        self.assertTrue(form.fields['password1'].required)
        self.assertTrue(form.fields['password2'].required)
        self.assertFalse(form.fields['profile_image'].required)

        # Effettua una richiesta POST alla view di registrazione del cliente
        response = self.client.post(self.url, data=user_data, follow=True)

        # Verifica che la registrazione sia avvenuta con successo
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('authentication:signin',kwargs={'user_type': 'client'}))

        # Verifica che l'utente e il cliente siano stati creati correttamente nel database
        User = get_user_model()
        user = User.objects.get(username=user_data['username'])
        self.assertTrue(Client.objects.filter(user=user).exists())
        client = Client.objects.get(user=user)

        #Controllo campi inseriti user
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name,user_data['last_name'])
        self.assertEqual(user.email,user_data['email'])
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(user.last_login,None) #Nessun login ancora

        #Controllo campi inseriti Client
        self.assertEqual(client.telephone, user_data['telephone'])
        self.assertEqual(client.address, user_data['address'])
        self.assertEqual(client.house_number, user_data['house_number'])
        self.assertEqual(client.city, user_data['city'])
        self.assertEqual(client.province, user_data['province'])
        self.assertEqual(client.cap, user_data['cap'])
        self.assertEqual(str(client.birth_date), user_data['birth_date'])
        self.assertEqual(client.profile_image,'unknown.jpeg') #Immagine di default

        # Controllo sul carrello relativo all'utente
        carrello =Carrello.objects.get(user=client)
        self.assertIsNotNone(carrello)
        self.assertEqual(carrello.user,client)

#Test registrazione admin
class AdminRegistrationTest(TestCase):
    def setUp(self):
        self.user_type = 'admin'  # Imposto il valore di user_type
        self.url = reverse('authentication:signup', kwargs={'user_type': self.user_type}) 

    def test_admin_registration(self):
        
        #Dati utente cliente di test
        user_data = {
            'username': 'adminuser',
            'email': 'adminuser@example.com',
            'first_name': 'adminname',
            'last_name': 'adminsurname',
            'password1': 'adminpassword',
            'password2': 'adminpassword',
        }

        #Controllo validità dei dati inseriti nel form di registrazione di un admin
        form = CustomUserCreationForm(data=user_data)
        self.assertTrue(form.is_valid()) 

        cleaned_data = form.cleaned_data
        self.assertTrue('username' in cleaned_data)
        self.assertTrue('email' in cleaned_data)
        self.assertTrue('first_name' in cleaned_data)
        self.assertTrue('last_name' in cleaned_data)
        self.assertTrue('password1' in cleaned_data)
        self.assertTrue('password2' in cleaned_data)

        #Verifico condizioni sui campi del form
        self.assertTrue(form.fields['username'].required)
        self.assertTrue(form.fields['email'].required)
        self.assertTrue(form.fields['first_name'].required)
        self.assertTrue(form.fields['last_name'].required)
        self.assertTrue(form.fields['password1'].required)
        self.assertTrue(form.fields['password2'].required)

        # Effettua una richiesta POST alla view di registrazione dell'admin
        response = self.client.post(self.url, data=user_data, follow=True)

        # Verifica che la registrazione sia avvenuta con successo
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('authentication:signin',kwargs={'user_type': 'admin'}))

        # Verifica che l'utente e il cliente siano stati creati correttamente nel database
        User = get_user_model()
        user = User.objects.get(username=user_data['username'])

        #Controllo campi inseriti user
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name,user_data['last_name'])
        self.assertEqual(user.email,user_data['email'])
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(user.last_login,None) #Nessun login ancora
