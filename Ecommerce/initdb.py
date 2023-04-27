from products.models import *
from authentication.models import *
from orders.models import Ordine, Ordine_Item
from cart.models import *
from django.db import connection
import datetime

def erase_db_Products():
    print("-- Cancello il DB Product --\n")
    Product.objects.all().delete() #Cancello oggetti table products

    cursor = connection.cursor()
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_product'; ''') #Resetta ID table products_product
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_smartphone'; ''') #Resetta ID table products_smartphone
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_computer'; ''') #Resetta ID table products_computer
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_televisore'; ''') #Resetta ID table products_televisore
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_custodia'; ''') #Resetta ID table products_custodia
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_cuffie'; ''') #Resetta ID table products_cuffie

def init_db_Products():

    if len(Product.objects.all()) != 0:
        return

    #Se vuoto lo inizializzo

    #Dizionario contenente i dati dei computer
    computerdict = {
        "image" : ["Macbook_pro_M1Pro.jpg","Acer_aspire.jpg","Macbook_air_2022.jpg","Acer_Predator_helios.jpg"],
        "name" : ["Macbook Pro 14","Acer Aspire","Macbook Air 2022","Acer Predator Helios 300"],
        "product_code" : ["172534","183359","176212","164300"  ],
        "productor" : ["Apple","Acer","Apple","Acer"  ],
        "color" : ["Gray","Silver","Gray","Black"  ],
        "size" : ["31.2x1.5x22","36.3x1.79x23.8","30.4x1.1x21.5","39.8x2.6x27.5"  ],
        "full_price" : [2849.00,999.99,1529.00,1750.00],
        "discount":[12,20,17,13],
        "quantity" : [7,5,4,2 ],
        "weight" : [1.71,1.9,1.24,2.9 ],

        "display_resolution":["3024x1964","1920x1080","2560x1664","1920x1080"],
        "cpu":["M1 PRO CPU 10-Core","Core i7 1165G7","M2 CPU 8-Core","Core i7 11800H"],
        "ram":[16,16,8,16],
        "disk_size":[1000,1024,256,1024],
        "disk_type":["SSD","SSD","SSD","SSD"],
        "operating_system":["MacOS","Windows 11 Home","MacOS Monterey","Windows 11 Home"],
        "graphic_card":["Apple GPU 16-Core","Intel Iris Xe Graphics","Apple GPU 8-Core","NVIDIA GeForce RTX 3070"],
        "battery_autonomy":[11,8,15,5],
        "additional_function":["Webcam integrata","Display IPS","2 porte thunderbolt","Refresh rate 144Hz"],
        "display_size":[14,15.6,13.6,17.3]
    }

    #Dizionario contenente i dati degli smartphone
    smartphonedict = {
        "image" : ["Apple_Iphone_13.jpg","Apple_Iphone_11.jpg"],
        "name" : ["Iphone 13","Iphone 11"],
        "product_code" : ["172081","172013"],
        "productor" : ["Apple","Apple"],
        "color" : ["Black","Black"],
        "size" : ["7x14x0.7","7.5x15x0.8" ],
        "full_price" : [939.00,609.00],
        "discount":[15,9],
        "quantity" : [13,0],
        "weight" : [0.17,0.19],

        "cpu":["A15 Bionic","A13 Bionic"],
        "ram":[4,4],
        "disk_size":[128,128],
        "operating_system":["IOS","IOS"],
        "battery_autonomy":[15,12],
        "camera":[12,12],
        "additional_function":["Doppia fotocamera","Display LCD"],
        "display_size":[6.1,6.1]

    }   

    #Dizionario contenente i dati dei televisori
    televisoredict={
        "image" : ["Samsung_UE50AU7170UXZT.png","Samsung_QE85Q950TSTXZT.png",],
        "name" : ["Samsung UE50AU7170UXZT","Samsung QE85Q950TSTXZT"],
        "product_code" : ["153372","139572"],
        "productor" : ["Samsung","Samsung" ],
        "color" : ["Black","Black" ],
        "size" : ["116.8x72x25","187.7x113.1x34"],
        "full_price" : [449.99,8999.99],
        "discount":[15,0],
        "quantity" : [10,2 ],
        "weight" : [11.6,65.8],

        "display_size":[50,85],
        "display_resolution":["3840x2160","7680x4320"],
        "display_technology":["LED","QLED"],
        "display_quality":["UHD 4K","QLED 8K"],
        "cpu":["Crystal 4K","Quantum 8K"],
        "frame_frequency":[60,120],
        "reception_type":["DVB-T2","DVB-T2"],
        "additional_function":["Smart TV, 3xHdmi","Smart TV, HDR, 4xHdmi ARC"]


    }

    #Dizionario contenente i dati delle custodie
    coverdict={
        "image" : ["Custodia_iphone13_rosa.png","Custodia_iphone11_nero.png",],
        "name" : ["Cover Iphone 13","Cover Iphone 11"],
        "product_code" : ["172236","172268"],
        "productor" : ["Apple","Apple" ],
        "color" : ["Rosa pomelo","Black" ],
        "size" : ["7x14x0.7","7.5x15x0.8"],
        "full_price" : [59,45],
        "discount":[17,7],
        "quantity" : [4,2 ],
        "weight" : [0.6,0.6],

        "compatibilità":["Iphone 13","Iphone 11"],
        "caratteristiche":["Materiale: silicone. Fodera interna: soffice microfibra. Compatibile ricarica wireless; Protegge da graffi e cadute.",
                           "Progettata da Apple, la custodia in silicone aderisce perfettamente ai tasti del volume e al tasto laterale, e avvolge le curve del telefono senza appesantirne il profilo. La morbida fodera interna in microfibra protegge l’iPhone, mentre l’esterno è in silicone e permette la ricarica in wireless."]

    }

    #Dizionario contenente i dati delle cuffie
    cuffiedict={
        "image" : ["Airpodsmax_celeste.png","Bose_700_nere.png",],
        "name" : ["Airpods Max Celeste","Bose 700"],
        "product_code" : ["172853","108221"],
        "productor" : ["Apple","Bose" ],
        "color" : ["Celeste","Black" ],
        "size" : ["18.7x16.8x8.3","16.5x20.3x5"],
        "full_price" : [629,329.99],
        "discount":[0,10],
        "quantity" : [3,5 ],
        "weight" : [0.38,0.25],

        "cuffie_type":["Bluetooth over-ear","Bluetooth over-ear"],
        "caratteristiche":["Processore audio: Apple H1, cancellazione del rumore","Facile accesso agli assistenti vocali inclusi Assistente Google e Amazon Alexa. Cancellazione del rumore fino a 11 livelli."]
    }

    #Acquisisco i fornitori che inseriscono i prodotti
    admin_1=User.objects.get(username="Filippo") #Acquisisco utente Filippo
    admin_2=User.objects.get(username="Massimo") #Acquisisco utente Massimo

    
     #-----------       Prodotti Computer -----------------
    for i in range(4): # 4 prodotti computer
        c = Computer() #Oggetto prodotto
        for k in computerdict:
            if k =="image":
                c.image=computerdict[k][i]
            if k=="name":
                c.name=computerdict[k][i]
            if k=="product_code":
                c.product_code=computerdict[k][i]
            if k=="productor":
                c.productor=computerdict[k][i]
            if k=="color":
                c.color=computerdict[k][i]
            if k =="size":
                c.size=computerdict[k][i]
            if k=="full_price":
                c.full_price=computerdict[k][i]
            if k=="discount":
                c.discount=computerdict[k][i] 
            if k=="quantity":
                c.quantity=computerdict[k][i]
            if k=="weight":
                c.weight=computerdict[k][i]

            if k =="display_resolution":
                c.display_resolution=computerdict[k][i]
            if k=="cpu":
                c.cpu=computerdict[k][i]
            if k=="ram":
                c.ram=computerdict[k][i]
            if k=="disk_size":
                c.disk_size=computerdict[k][i]
            if k=="disk_type":
                c.disk_type=computerdict[k][i]
            if k=="operating_system":
                c.operating_system=computerdict[k][i]
            if k=="graphic_card":
                c.graphic_card=computerdict[k][i]
            if k=="battery_autonomy":
                c.battery_autonomy=computerdict[k][i]
            if k=="additional_function":
                c.additional_function=computerdict[k][i]
            if k=="display_size":
                c.display_size=computerdict[k][i]

        c.supplier=admin_2
        c.type="computer"
        c.final_price= round(c.full_price-((c.full_price/100)*c.discount),2) #Calcolo prezzo finale scontato
        c.save() #Salvo prodotti nel DB

    #-----------       Prodotti Televisore -----------------

    for i in range(2): # 2 prodotti televisore
        t =Televisore() #Oggetto televisore
        for k in televisoredict:
            if k =="image":
                t.image=televisoredict[k][i]
            if k =="name":
                t.name=televisoredict[k][i]
            if k =="product_code":
                t.product_code=televisoredict[k][i]
            if k =="productor":
                t.productor=televisoredict[k][i]
            if k =="color":
                t.color=televisoredict[k][i]
            if k =="size":
                t.size=televisoredict[k][i]
            if k =="full_price":
                t.full_price=televisoredict[k][i]
            if k =="discount":
                t.discount=televisoredict[k][i] 
            if k =="quantity":
                t.quantity=televisoredict[k][i]
            if k =="weight":
                t.weight=televisoredict[k][i]
        
            if k =="display_size":
                t.display_size=televisoredict[k][i]
            if k=="display_resolution":
                t.display_resolution=televisoredict[k][i]
            if k=="display_technology":
                t.display_technology=televisoredict[k][i]
            if k=="display_quality":
                t.display_quality=televisoredict[k][i]
            if k=="cpu":
                t.cpu=televisoredict[k][i]
            if k=="frame_frequency":
                t.frame_frequency=televisoredict[k][i]
            if k=="reception_type":
                t.reception_type=televisoredict[k][i]
            if k=="additional_function":
                t.additional_function=televisoredict[k][i]

        t.supplier=admin_2
        t.type="televisore"
        t.final_price= round(t.full_price-((t.full_price/100)*t.discount),2) #Calcolo prezzo finale scontato
        t.save()


    #-----------       Prodotti Smartphone  -----------------

    for i in range(2): # 2 prodotti smartphone
        s =Smartphone() #Oggetto smartphone
        for k in smartphonedict:
            if k =="image":
                s.image=smartphonedict[k][i]
            if k=="name":
                s.name=smartphonedict[k][i]
            if k=="product_code":
                s.product_code=smartphonedict[k][i]
            if k=="productor":
                s.productor=smartphonedict[k][i]
            if k=="color":
                s.color=smartphonedict[k][i]
            if k =="size":
                s.size=smartphonedict[k][i]
            if k=="full_price":
                s.full_price=smartphonedict[k][i]
            if k=="discount":
                s.discount=smartphonedict[k][i] 
            if k=="quantity":
                s.quantity=smartphonedict[k][i]
            if k=="weight":
                s.weight=smartphonedict[k][i]

            if k =="cpu":
                s.cpu=smartphonedict[k][i]
            if k =="ram":
                s.ram=smartphonedict[k][i]
            if k =="disk_size":
                s.disk_size=smartphonedict[k][i]
            if k =="battery_autonomy":
                s.battery_autonomy=smartphonedict[k][i]
            if k =="operating_system":
                s.operating_system=smartphonedict[k][i]
            if k =="camera":
                s.camera=smartphonedict[k][i]
            if k =="additional_function":
                s.additional_function=smartphonedict[k][i]
            if k =="display_size":
                s.display_size=smartphonedict[k][i]
        
        s.supplier=admin_1
        s.type="smartphone"
        s.final_price= round(s.full_price-((s.full_price/100)*s.discount),2) #Calcolo prezzo finale scontato
        s.save()


    #-----------       Prodotti Cover  -----------------
    
    for i in range(2): # 2 prodotti cover
        c =Cover() #Oggetto cover
        for k in coverdict:
            if k =="image":
                c.image=coverdict[k][i]
            if k=="name":
                c.name=coverdict[k][i]
            if k=="product_code":
                c.product_code=coverdict[k][i]
            if k=="productor":
                c.productor=coverdict[k][i]
            if k=="color":
                c.color=coverdict[k][i]
            if k =="size":
                c.size=coverdict[k][i]
            if k=="full_price":
                c.full_price=coverdict[k][i]
            if k=="discount":
                c.discount=coverdict[k][i] 
            if k=="quantity":
                c.quantity=coverdict[k][i]
            if k=="weight":
                c.weight=coverdict[k][i]
            
            if k=="compatibilità":
                c.compatibilità=coverdict[k][i]
            if k=="caratteristiche":
                c.caratteristiche=coverdict[k][i]

        c.supplier=admin_1
        c.type="cover"
        c.final_price= round(c.full_price-((c.full_price/100)*c.discount),2) #Calcolo prezzo finale scontato
        c.save()

    #-----------       Prodotti Cuffie  -----------------
    for i in range(2):
        c=Cuffie()
        for k in cuffiedict:
            if k =="image":
                c.image=cuffiedict[k][i]
            if k=="name":
                c.name=cuffiedict[k][i]
            if k=="product_code":
                c.product_code=cuffiedict[k][i]
            if k=="productor":
                c.productor=cuffiedict[k][i]
            if k=="color":
                c.color=cuffiedict[k][i]
            if k =="size":
                c.size=cuffiedict[k][i]
            if k=="full_price":
                c.full_price=cuffiedict[k][i]
            if k=="discount":
                c.discount=cuffiedict[k][i] 
            if k=="quantity":
                c.quantity=cuffiedict[k][i]
            if k=="weight":
                c.weight=cuffiedict[k][i]
            
            if k=="cuffie_type":
                c.cuffie_type=cuffiedict[k][i]
            if k=="caratteristiche":
                c.caratteristiche=cuffiedict[k][i]
            
        c.supplier=admin_1
        c.type="cuffie"
        c.final_price= round(c.full_price-((c.full_price/100)*c.discount),2) #Calcolo prezzo finale scontato
        c.save()

    print("-- Popolo il DB Product --\n")

def erase_db_Users():

    print("-- Cancello il DB Users --\n")
    User.objects.all().delete() #Cancello oggetti table users

    cursor = connection.cursor()
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='auth_user'; ''') #Resetta ID table auth_user
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='authentication_client'; ''') #Resetta ID table authentication_client
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='cart_carrello'; ''') #Resetta ID table cart_carrello
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='cart_carrello_item'; ''') #Resetta ID table cart_carrello_item
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='cart_carrello_prodotto'; ''') #Resetta ID table cart_carrello_item

def init_db_Users():

    if len(User.objects.all()) != 0:
        return
    
    clientdict = {
        "first_name" : ["Jennifer","Daniele"],
        "last_name" : ["Reggiani","Zanoli"],
        "username" : ["Jennifer","Daniele"  ],
        "email" : ["reggianije@live.it","daniele99@gmail.com"  ],
        "password" : ["1234","1234"  ],

        "birth_date":[datetime.date(1999,12,30),datetime.date(1999,6,7)],
        "telephone":["331678923","3393456781"],
        "address":["via marconi","via san michele"],
        "house_number":[15,35],
        "city":["Soliera","Soliera"],
        "province":["Modena","Modena"],
        "cap":["41019","41019"]
    }

    admindict ={
        "first_name" : ["Filippo","Massimo"],
        "last_name" : ["Reggiani","Rossi"],
        "username" : ["Filippo","Massimo"  ],
        "email" : ["reggianifilippo@live.it","massimorossi@live.it"  ],
        "password" : ["1234","1234"  ],
    }

    #Aggiungo oggetti di tipo user (client)
    for i in range(2): # 1 oggetto user
        user = User() #Oggetto user
        client=Client()
        for k in clientdict:
            if k =="first_name":
                first_name=clientdict[k][i]
            if k=="last_name":
                last_name=clientdict[k][i]
            if k=="username":
                username=clientdict[k][i]
            if k=="email":
                email=clientdict[k][i]
            if k=="password":
                password=clientdict[k][i]

            if k=="birth_date":
                client.birth_date=clientdict[k][i]
            if k=="telephone":
                client.telephone=clientdict[k][i]
            if k=="address":
                client.address=clientdict[k][i]
            if k=="house_number":
                client.house_number=clientdict[k][i]
            if k=="city":
                client.city=clientdict[k][i]
            if k=="province":
                client.province=clientdict[k][i]
            if k=="cap":
                client.cap=clientdict[k][i]
            
        user=User.objects.create_user(username,email,password)
        user.first_name=first_name
        user.last_name=last_name
        user.is_active=True
        user.is_staff=False
        user.is_superuser=False
        user.save() #Salvo sul DB oggetto user
        client.user=user

        client.save() #Salvo sul DB oggetto client

        #Creo carrello per utente cliente
        carrello= Carrello()
        carrello.user=client
        carrello.save()


    #Aggiungo oggetti di tipo user (admin)
    for i in range(2): # 1 oggetto user
        user = User() #Oggetto user
        for k in admindict:
            if k =="first_name":
                first_name=admindict[k][i]
            if k=="last_name":
                last_name=admindict[k][i]
            if k=="username":
                username=admindict[k][i]
            if k=="email":
                email=admindict[k][i]
            if k=="password":
                password=admindict[k][i]
        
        user=User.objects.create_user(username,email,password)
        user.first_name=first_name
        user.last_name=last_name
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.save() #Salvo sul DB oggetto user
    
    print("-- Popolo il DB User --\n")

def erase_db_Orders():

    print("-- Cancello il DB Orders --\n")
    Ordine.objects.all().delete() #Cancello oggetti table ordine
    Ordine_Item.objects.all().delete() #Cancello oggetti table ordine_item

    cursor = connection.cursor()
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='orders_ordine'; ''') #Resetta ID table orders_ordine
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='orders_ordine_item'; ''') #Resetta ID table orders_ordine_item
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='orders_ordine_prodotto'; ''') #Resetta ID table orders_ordine_prodotto
    
def init_db_Orders():

    if len(Ordine.objects.all()) != 0 or len(Ordine_Item.objects.all()!=0):
        return


    ordersdict = {
        "id_ordine" : ["Jennifer","Daniele"],
        "Date" : ["Reggiani","Zanoli"],
        "total_price" : ["Jennifer","Daniele"  ],
        
    }

    #Aggiungo oggetti di tipo Ordine e Ordine_Item
    for i in range(2): # 1 oggetto user
        user = Ordine() #Oggetto user
        for k in admindict:
            if k =="first_name":
                first_name=admindict[k][i]
            if k=="last_name":
                last_name=admindict[k][i]
            if k=="username":
                username=admindict[k][i]
            if k=="email":
                email=admindict[k][i]
            if k=="password":
                password=admindict[k][i]
        
        user=User.objects.create_user(username,email,password)
        user.first_name=first_name
        user.last_name=last_name
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.save() #Salvo sul DB oggetto user
    
    print("-- Popolo il DB User --\n")


    



