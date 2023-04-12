from products.models import *
from authentication.models import *
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


def init_db_Products():

    if len(Product.objects.all()) != 0:
        return

    #Se vuoto lo inizializzo

    #Lista computer
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
        "supplier_id" : [1,1],
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

    admin_1=User.objects.get(username="Filippo") #Acquisisco utente Filippo

    #Aggiungo prodotti di tipo computer
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

        c.supplier=admin_1
        c.type="computer"
        c.final_price= round(c.full_price-((c.full_price/100)*c.discount),2) #Calcolo prezzo finale scontato
        c.save() #Salvo prodotti nel DB

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
            if k=="supplier_id":
                s.supplier=admin_1
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
        
        s.type="smartphone"
        s.final_price= round(s.full_price-((s.full_price/100)*s.discount),2) #Calcolo prezzo finale scontato
        s.save()

    print("-- Popolo il DB Product --\n")

def erase_db_Users():

    print("-- Cancello il DB Users --\n")
    User.objects.all().delete() #Cancello oggetti table users

    cursor = connection.cursor()
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='auth_user'; ''') #Resetta ID table auth_user
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='authentication_client'; ''') #Resetta ID table authentication_client
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='cart_carrello'; ''') #Resetta ID table cart_carrello
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='cart_carrello_item'; ''') #Resetta ID table cart_carrello_item

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
            


