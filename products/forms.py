from django import forms
from django.urls import reverse_lazy
from .models import *

#Form inserimento campi Product
class ProductForm(forms.ModelForm):
    image=forms.ImageField(required=True)
    name =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire nome'})) 
    product_code =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire codice prodotto'}))
    productor =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire produttore'}))
    color =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire colore prodotto'}))
    size =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire dimensione prodotto'}))
    weight =forms.FloatField(required=True,min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Inserire peso'}))
    full_price =forms.FloatField(required=True,min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Inserire prezzo totale'}))
    discount =forms.IntegerField(required=True,min_value=0,max_value=99, widget=forms.NumberInput(attrs={'placeholder': 'Inserire sconto (se presente)'}))
    quantity =forms.IntegerField(required=True,min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Inserire quantità'}))

    #Imposto le label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = 'Immagine'  
        self.fields['name'].label = 'Nome'
        self.fields['product_code'].label = 'Codice Prodotto'
        self.fields['productor'].label = 'Produttore'
        self.fields['color'].label = 'Colore'
        self.fields['size'].label = 'Dimensione (L/A/P)'
        self.fields['weight'].label = 'Peso (Kg)'
        self.fields['full_price'].label = 'Prezzo Totale (€)'
        self.fields['discount'].label = 'Sconto (%)'
        self.fields['quantity'].label = 'Quantità'

    def validate_product_code(self, value):
        if Product.objects.filter(product_code=value).exists():
            raise forms.ValidationError("Codice prodotto già presente nel sistema, inserirne un altro.")
        return value

#Form inserimento campi Computer
class ComputerForm(ProductForm):
    display_size =forms.FloatField(required=True, min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Inserire dimensione display'}))
    display_resolution =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire risoluzione display'}))
    cpu =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire processore'}))
    ram =forms.IntegerField(required=True,min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Inserire ram'}))
    disk_size =forms.FloatField(required=True, min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Inserire dimensione disco'}))
    disk_type =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire tipologia disco'}))
    operating_system =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire sistema operativo'}))
    graphic_card =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire scheda grafica'}))
    battery_autonomy =forms.FloatField(required=True,min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Inserire autonomia batteria'}))
    additional_function =forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Inserire funzionalità aggiuntive','rows': 5, 'cols': 40}))

    class Meta:
        model=Computer
        fields=["image","name","product_code","productor","color","size","weight","full_price","discount","quantity",
                "display_size","display_resolution","cpu","ram","disk_size","disk_type","operating_system","graphic_card","battery_autonomy","additional_function"]
        
    #Imposto le label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['display_size'].label = 'Dimensione display (pollici)'  
        self.fields['display_resolution'].label = 'Risoluzione display (pixel)'
        self.fields['cpu'].label = 'Processore'
        self.fields['ram'].label = 'Ram (GB)'
        self.fields['disk_size'].label = 'Dimensione disco (GB)'
        self.fields['operating_system'].label = 'Sistema operativo'
        self.fields['graphic_card'].label = 'Scheda grafica'
        self.fields['battery_autonomy'].label = 'Autonomia batteria (ore)'
        self.fields['additional_function'].label = 'Funzionalità aggiuntive'

#Form inserimento campi Smartphone
class SmartphoneForm(ProductForm):
    display_size =forms.FloatField(required=True,min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Inserire dimensione display'}))
    cpu =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire processore'}))
    ram =forms.IntegerField(required=True,min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Inserire ram'}))
    disk_size =forms.FloatField(required=True, min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Inserire dimensione disco'}))
    operating_system =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire sistema operativo'}))
    battery_autonomy =forms.FloatField(required=True,min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Inserire autonomia batteria'}))
    camera=forms.IntegerField(required=True,min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Inserire fotocamera'}))
    additional_function =forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Inserire funzionalità aggiuntive','rows': 5, 'cols': 40}))
    
    class Meta:
        model=Smartphone
        fields=["image","name","product_code","productor","color","size","weight","full_price","discount","quantity",
                "display_size","cpu","ram","disk_size","operating_system","battery_autonomy","camera","additional_function"]

    #Imposto le label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['display_size'].label = 'Dimensione display (pollici)'  
        self.fields['cpu'].label = 'Processore'
        self.fields['ram'].label = 'Ram (GB)'
        self.fields['disk_size'].label = 'Dimensione disco (GB)'
        self.fields['operating_system'].label = 'Sistema operativo'
        self.fields['battery_autonomy'].label = 'Autonomia batteria (ore)'
        self.fields['camera'].label = 'Fotocamera (MPx)'
        self.fields['additional_function'].label = 'Funzionalità aggiuntive'

#Form inserimento campi Televisore  
class TelevisoreForm(ProductForm):
    display_size =forms.FloatField(required=True,min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Inserire dimensione display'}))
    display_resolution =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire risoluzione display'}))
    display_technology =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire tecnologia display'}))
    display_quality =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire qualità display'}))
    cpu =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire processore'}))
    frame_frequency =forms.IntegerField(required=True,min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Inserire Frequenza frame'}))
    reception_type =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire ricezione antenna'}))
    additional_function =forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Inserire funzionalità aggiuntive','rows': 5, 'cols': 40}))

    class Meta:
        model=Televisore
        fields=["image","name","product_code","productor","color","size","weight","full_price","discount","quantity",
                "display_size","display_resolution","display_technology","display_quality","cpu","frame_frequency","reception_type","additional_function"]

    #Imposto le label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['display_size'].label = 'Dimensione display (pollici)' 
        self.fields['display_resolution'].label = 'Risoluzione display (pixel)' 
        self.fields['display_technology'].label = 'Tecnologia display'
        self.fields['display_quality'].label = 'Qualità display'
        self.fields['cpu'].label = 'Processore'
        self.fields['frame_frequency'].label = 'Frequenza frame (Hz)'
        self.fields['reception_type'].label = 'Ricezione antenna'
        self.fields['additional_function'].label = 'Funzionalità aggiuntive'
    
#Form inserimento campi Cover
class CoverForm(ProductForm):
    compatibilità =forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Inserire compatibilità','rows': 2, 'cols': 40}))
    caratteristiche =forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Inserire caratteristiche','rows': 5, 'cols': 40}))
    
    class Meta:
        model=Cover
        fields=["image","name","product_code","productor","color","size","weight","full_price","discount","quantity",
                "compatibilità","caratteristiche"]

    #Imposto le label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['compatibilità'].label = 'Compatibilità' 
        self.fields['caratteristiche'].label = 'Caratteristiche'

#Form inserimento campi Cuffie
class CuffieForm(ProductForm):
    cuffie_type =forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Inserire tipologia'}))
    caratteristiche =forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Inserire caratteristiche','rows': 5, 'cols': 40}))
    
    class Meta:
        model=Cuffie
        fields=["image","name","product_code","productor","color","size","weight","full_price","discount","quantity",
                "cuffie_type","caratteristiche"]
        
    #Imposto le label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cuffie_type'].label = 'Tipologia' 
        self.fields['caratteristiche'].label = 'Caratteristiche' 

#Form inserimento dati Recensione
class RecensioneForm(forms.ModelForm):
    description=forms.CharField(required=True,widget=forms.Textarea(attrs={'placeholder': 'Inserire descrizione','rows': 5, 'cols': 40}))
    valutation = forms.IntegerField(required=True, min_value=1, max_value=5, widget=forms.NumberInput(attrs={'placeholder': 'Inserire valutazione'}))

    class Meta:
        model=Recensione
        fields=['description','valutation']

    #Imposto le label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].label = 'Descrizione' 
        self.fields['valutation'].label = 'Valutazione' 