from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

#FORM DI INSERIMENTO PRODOTTI
class ComputerForm(forms.ModelForm):

    class Meta:
        model=Computer
        fields=["image","name","product_code","productor","color","size","weight","full_price","discount","quantity",
                "display_size","display_resolution","cpu","ram","disk_size","disk_type","operating_system","graphic_card","battery_autonomy","additional_function"]
    
    
    def is_valid(self):
        valid= super(ComputerForm,self).is_valid()
        return valid
        #Controlli sui campi
    
class SmartphoneForm(forms.ModelForm):

    class Meta:
        model=Smartphone
        fields=["image","name","product_code","productor","color","size","weight","full_price","discount","quantity",
                "display_size","cpu","ram","disk_size","operating_system","battery_autonomy","camera","additional_function"]

    def is_valid(self):
        valid= super(SmartphoneForm,self).is_valid()
    
        #Controlli sui campi
        return valid
    
class TelevisoreForm(forms.ModelForm):

    class Meta:
        model=Televisore
        fields=["image","name","product_code","productor","color","size","weight","full_price","discount","quantity",
                "display_size","display_resolution","display_technology","display_quality","cpu","frame_frequency","reception_type","additional_function"]

    def is_valid(self):
        valid= super(TelevisoreForm,self).is_valid()
    
        #Controlli sui campi
        return valid
     
class CoverForm(forms.ModelForm):

    class Meta:
        model=Cover
        fields=["image","name","product_code","productor","color","size","weight","full_price","discount","quantity",
                "compatibilità","caratteristiche"]

    def is_valid(self):
        valid= super(CoverForm,self).is_valid()
    
        #Controlli sui campi
        return valid
    
class CuffieForm(forms.ModelForm):

    class Meta:
        model=Cuffie
        fields=["image","name","product_code","productor","color","size","weight","full_price","discount","quantity",
                "cuffie_type","caratteristiche"]

    def is_valid(self):
        valid= super(CuffieForm,self).is_valid()
    
        #Controlli sui campi
        return valid
    
    
#FORM INSERIMENTO RECENSIONE

class RecensioneForm(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea)
    valutation = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model=Recensione
        fields=['description','valutation']
