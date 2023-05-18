from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from datetime import date, timedelta
from django.conf import settings
import re

#Form per la creazione degli admin
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire email'}))  
    first_name =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire nome'})) 
    last_name= forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire cognome'})) 

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email','first_name','last_name' )  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Inserire username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Inserire password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Conferma password'
        self.fields['email'].label = 'Email'  
        self.fields['first_name'].label ='Nome'
        self.fields['last_name'].label='Cognome'

    #Controlla che il nome sia composto solo da caratteri
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.match(r'^[a-zA-Z\s]+$', first_name):
            raise forms.ValidationError("Il nome può contenere solo caratteri.")
        return first_name

    #Controlla che il cognome sia composto solo da caratteri
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.match(r'^[a-zA-Z\s]+$', last_name):
            raise forms.ValidationError("Il cognome può contenere solo caratteri.")
        return last_name
    
    #Controlla che l'email non sia già presente
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("L'email inserita è già presente. Reinserisci un'email valida.")
        return email
    

#Form per la registrazione dei clienti
class ClientCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire email'}))  
    first_name =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire nome'})) 
    last_name= forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire cognome'})) 
    profile_image=forms.ImageField(required=False)
    telephone=forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Inserire telefono'}))
    address=forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire indirizzo'}))
    house_number=forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Inserire numero civico'}))
    city=forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire città'}))
    province=forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire provincia'}))
    cap=forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Inserire CAP'}))
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date','min': '1900-01-01','max':str(date.today() - timedelta(days=14*365))})) #Dal 1900 a 14 anni fa almeno

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email','first_name','last_name','profile_image','telephone','address','house_number','city','province','cap','birth_date' )  
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Inserire username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Inserire password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Conferma password'
        self.fields['email'].label = 'Email'  
        self.fields['first_name'].label ='Nome'
        self.fields['last_name'].label='Cognome'
        self.fields['profile_image'].label='Immagine'
        self.fields['telephone'].label='Telefono'
        self.fields['address'].label='Indirizzo'
        self.fields['house_number'].label='Numero civico'
        self.fields['city'].label='Città'
        self.fields['province'].label='Provincia'
        self.fields['cap'].label='CAP'
        self.fields['birth_date'].label='Data di nascita'

    #Controlla che il nome sia composto solo da caratteri
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.match(r'^[a-zA-Z\s]+$', first_name):
            raise forms.ValidationError("Il nome può contenere solo caratteri.")
        return first_name

    #Controlla che il cognome sia composto solo da caratteri
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.match(r'^[a-zA-Z\s]+$', last_name):
            raise forms.ValidationError("Il cognome può contenere solo caratteri.")
        return last_name
    
    #Controlla che non sia presente la mail inserita
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("L'email inserita è già presente. Reinserisci un'email valida.")
        return email
    
    #Imposta immagine del profilo di default nel caso non venga inserita
    def clean_profile_image(self):
        profile_image = self.cleaned_data['profile_image']
        if not profile_image:
            profile_image = 'unknown.jpeg'  # Imposta l'immagine di default 
        return profile_image
    
    #Controlla che la città non abbia numeri all'interno
    def clean_city(self):
        city = self.cleaned_data['city']
        if any(char.isdigit() for char in city):
            raise forms.ValidationError("Il nome della città non può contenere numeri.")
        return city

    #Controlla che la provincia non abbia numeri all'interno
    def clean_province(self):
        province = self.cleaned_data['province']
        if any(char.isdigit() for char in province):
            raise forms.ValidationError("Il nome della provincia non può contenere numeri.")
        return province

#Form per il cambio password
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['old_password'].widget.attrs['placeholder'] = 'Inserire vecchia password'
        self.fields['old_password'].label = 'Vecchia password'
        
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Inserire nuova password'
        self.fields['new_password1'].label = 'Nuova password'

        self.fields['new_password2'].widget.attrs['placeholder'] = 'Reinserire nuova password'
        self.fields['new_password2'].label = 'Conferma nuova password'