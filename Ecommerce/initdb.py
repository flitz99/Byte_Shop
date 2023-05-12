from products.models import *
from authentication.models import *
from orders.models import Ordine, Ordine_Item
from cart.models import *
from django.db import connection
import datetime, random, string

#Inizializzazione DB prodotti
def erase_db_Products():
    print("-- Cancello il DB Product --\n")
    Product.objects.all().delete() #Cancello oggetti table products

    cursor = connection.cursor()
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_product'; ''') #Resetta ID table products_product
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_product_recensioni'; ''') #Resetta ID table products_product_recensioni
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_recensione'; ''') #Resetta ID table products_recensione

#Popolamento DB prodotti
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
        "image" : ["Apple_Iphone_13.jpg","Apple_Iphone_11.jpg","Samsung_Galaxy_S23_Ultra.png"],
        "name" : ["Iphone 13","Iphone 11","Samsung Galaxy","Samsung Galaxy S23 Ultra"],
        "product_code" : ["172081","172013","185392"],
        "productor" : ["Apple","Apple","Samsung"],
        "color" : ["Black","Black","Green"],
        "size" : ["7x14x0.7","7.5x15x0.8","7.81x16.3x0.8",  ],
        "full_price" : [939.00,609.00,1479.00],
        "discount":[15,9,10],
        "quantity" : [13,0,3],
        "weight" : [0.17,0.19,0.23],

        "cpu":["A15 Bionic","A13 Bionic","Qualcomm SM8550"],
        "ram":[4,4,8],
        "disk_size":[128,128,256],
        "operating_system":["IOS","IOS","Android"],
        "battery_autonomy":[15,12,25],
        "camera":[12,12,200],
        "additional_function":["Doppia fotocamera","Display LCD","Display Dynamic AMOLED 2x, pennino incluso"],
        "display_size":[6.1,6.1,6.8]

    }   

    #Dizionario contenente i dati dei televisori
    televisoredict={
        "image" : ["Samsung_UE50AU7170UXZT.png","Samsung_QE85Q950TSTXZT.png","Sony_XR48A90KAEP.png"],
        "name" : ["Samsung UE50AU7170UXZT","Samsung QE85Q950TSTXZT","Sony XR48A90KAEP"],
        "product_code" : ["153372","139572","176064"],
        "productor" : ["Samsung","Samsung","Sony"],
        "color" : ["Black","Black","Black" ],
        "size" : ["116.8x72x25","187.7x113.1x34","106.9x62.9x22.5"],
        "full_price" : [449.99,8999.99,1949.99],
        "discount":[15,0,0],
        "quantity" : [10,2,5 ],
        "weight" : [11.6,65.8,16.5],

        "display_size":[50,85,48],
        "display_resolution":["3840x2160","7680x4320","3840x2160"],
        "display_technology":["LED","QLED","OLED"],
        "display_quality":["UHD 4K","QLED 8K","OLED 4K"],
        "cpu":["Crystal 4K","Quantum 8K","Cognitive Processor XR"],
        "frame_frequency":[60,120,120],
        "reception_type":["DVB-T2","DVB-T2","DVB-T2, DVB-C2"],
        "additional_function":["Smart TV, 3xHdmi","Smart TV, HDR, 4xHdmi ARC","Dolby Atmos"]


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
        "image" : ["Airpodsmax_celeste.png","Bose_700_nere.png","Airpods_3.png"],
        "name" : ["Airpods Max Celeste","Bose 700","Airpods 3"],
        "product_code" : ["172853","108221","179237"],
        "productor" : ["Apple","Bose","Apple" ],
        "color" : ["Celeste","Black","White" ],
        "size" : ["18.7x16.8x8.3","16.5x20.3x5","5x5.3x2.1"],
        "full_price" : [629,329.99,209.00],
        "discount":[0,10,10],
        "quantity" : [3,5,4],
        "weight" : [0.38,0.25,0.03],

        "cuffie_type":["Bluetooth over-ear","Bluetooth over-ear","Auricolari wireless"],
        "caratteristiche":["Processore audio: Apple H1, cancellazione del rumore","Facile accesso agli assistenti vocali inclusi Assistente Google e Amazon Alexa. Cancellazione del rumore fino a 11 livelli.","Il sensore di pressione ti dà ancora più controllo su quello che ascolti. Ti basta premere per far partire un brano, metterlo in pausa o passare a quello successivo, ma anche per rispondere a una chiamata e riagganciare."]
    }

    #Acquisisco i fornitori che inseriscono i prodotti
    admin_1=User.objects.get(username="Filippo") #Acquisisco utente Filippo
    admin_2=User.objects.get(username="Massimo") #Acquisisco utente Massimo
    admin_3=User.objects.get(username="Paolo") #Acquisisco utente Paolo
    
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

        c.supplier=admin_1 
        c.type="computer"
        c.final_price= round(c.full_price-((c.full_price/100)*c.discount),2) #Calcolo prezzo finale scontato
        c.save() #Salvo prodotti nel DB

    #-----------       Prodotti Televisore -----------------

    for i in range(3): # 2 prodotti televisore
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

        t.supplier=admin_3
        t.type="televisore"
        t.final_price= round(t.full_price-((t.full_price/100)*t.discount),2) #Calcolo prezzo finale scontato
        t.save()


    #-----------       Prodotti Smartphone  -----------------

    for i in range(3): # 2 prodotti smartphone
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
        
        s.supplier=admin_2
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

        c.supplier=admin_2
        c.type="cover"
        c.final_price= round(c.full_price-((c.full_price/100)*c.discount),2) #Calcolo prezzo finale scontato
        c.save()

    #-----------       Prodotti Cuffie  -----------------
    for i in range(3):
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

#Inizializzazione DB utenti
def erase_db_Users():

    print("-- Cancello il DB Users --\n")
    User.objects.all().delete() #Cancello oggetti table users

    cursor = connection.cursor()
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='auth_user'; ''') #Resetta ID table auth_user
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='authentication_client'; ''') #Resetta ID table authentication_client
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='cart_carrello'; ''') #Resetta ID table cart_carrello
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='cart_carrello_item'; ''') #Resetta ID table cart_carrello_item
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='cart_carrello_prodotto'; ''') #Resetta ID table cart_carrello_item

#Popolamento DB utente
def init_db_Users():

    if len(User.objects.all()) != 0:
        return
    
    clientdict = {
        "first_name" : ["Jennifer","Daniele","Lorenzo"],
        "last_name" : ["Reggiani","Zanoli","Corradi"],
        "username" : ["Jennifer","Daniele","Lorenzo"  ],
        "email" : ["reggianije@live.it","daniele99@gmail.com","lore213@gmail.com"  ],
        "password" : ["Je123499","DART_Fener99","Balotelli17"  ],

        "birth_date":[datetime.date(1999,12,30),datetime.date(1999,6,7),datetime.date(1997,3,4)],
        "telephone":["3316789232","3393456781","3389076567"],
        "address":["via marconi","via san michele","via paganini"],
        "house_number":[15,35,12],
        "city":["Soliera","Soliera","Soliera"],
        "province":["Modena","Modena","Modena"],
        "cap":["41019","41019","41019"]
    }

    admindict ={
        "first_name" : ["Filippo","Massimo","Paolo"],
        "last_name" : ["Reggiani","Rossi","Sidoti"],
        "username" : ["Filippo","Massimo","Paolo"],
        "email" : ["reggianifilippo@live.it","massimorossi@live.it","paolosido@gmail.com"  ],
        "password" : ["F30i12l99","MAX275zp4","274PA59olo"],
    }

    #Aggiungo oggetti di tipo user (client)
    for i in range(3): # 3 oggetti user
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
    for i in range(3): # 1 oggetto user
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

#Inizializzazione DB ordini
def erase_db_Orders():

    print("-- Cancello il DB Orders --\n")
    Ordine.objects.all().delete() #Cancello oggetti table ordine
    Ordine_Item.objects.all().delete() #Cancello oggetti table ordine_item

    cursor = connection.cursor()
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='orders_ordine'; ''') #Resetta ID table orders_ordine
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='orders_ordine_item'; ''') #Resetta ID table orders_ordine_item
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='orders_ordine_prodotti'; ''') #Resetta ID table orders_ordine_prodotto

def create_order_code():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

#Popolamento DB ordini 
def init_db_Orders():

    if len(Ordine.objects.all()) != 0 or len(Ordine_Item.objects.all()) !=0:
        return

    clienti=Client.objects.filter().all() #Acquisisco tutti i clienti
    prodotti=Product.objects.filter().all() #Acquisisco tutti i prodotti

    #Dizionari con gli oggetti per ciascun ordine
    order1_itemdict={
        "item":[prodotti[0],prodotti[12]], #macbook pro e cuffie
        "quantity":[1,1],
        "price":[prodotti[0].final_price,prodotti[12].final_price]
    }

    order2_itemdict={
        "item":[prodotti[7],prodotti[10]], #Iphone 13 e cover iphone 13
        "quantity":[1,1],
        "price":[prodotti[7].final_price,prodotti[10].final_price]
    }
    
    order3_itemdict={
        "item":[prodotti[8],prodotti[11]], #iphone 11 e cover iphone 11
        "quantity":[1,1],
        "price":[prodotti[8].final_price,prodotti[11].final_price]
    }
    
    order4_itemdict={
        "item":[prodotti[5]], #Samsung 85"
        "quantity":[1],
        "price":[prodotti[5].final_price]
    }

    order5_itemdict={
        "item":[prodotti[2],prodotti[14]], #Macbook air e airpods
        "quantity":[1,1],
        "price":[prodotti[2].final_price,prodotti[14].final_price]
    }

    order6_itemdict={
        "item":[prodotti[4],prodotti[13]], #Samsung tv e cuffie bose
        "quantity":[1,1],
        "price":[prodotti[4].final_price,prodotti[13].final_price]
    }

    order7_itemdict={
        "item":[prodotti[4]], #Samsung tv 
        "quantity":[2],
        "price":[prodotti[4].final_price]
    }

    order8_itemdict={
        "item":[prodotti[7]], #Iphone 13
        "quantity":[1],
        "price":[prodotti[7].final_price]
    }

    order9_itemdict={
        "item":[prodotti[14]], #airpods 
        "quantity":[1],
        "price":[prodotti[14].final_price]
    }

    #Lista coi dizionari degli oggetti di ciascun ordine
    order_items_list=[order1_itemdict,order2_itemdict,order3_itemdict,order4_itemdict,order5_itemdict,order6_itemdict,order7_itemdict,order8_itemdict,order9_itemdict]
    
    #Dizionario degli ordini
    ordersdict = {
        "id_ordine" : [create_order_code(),create_order_code(),create_order_code(),create_order_code(),create_order_code(),create_order_code(),create_order_code(),create_order_code(),create_order_code()],
        "date": [datetime.date(2023,1,15),datetime.date(2023,2,10),datetime.date(2022,3,8),datetime.date(2023,4,15),datetime.date(2023,4,12),datetime.date(2023,4,3),datetime.date(2023,4,20),datetime.date(2023,4,28),datetime.date(2023,1,3)],
        "client":[clienti[0],clienti[0],clienti[1],clienti[1],clienti[2],clienti[2],clienti[0],clienti[1],clienti[0]]
    }

    #Aggiungo oggetti di tipo Ordine e Ordine_Item
    cont=0
    for i in range(9): # 9 ordini
        order = Ordine() #Oggetto ordine
        for k in ordersdict:
            if k =="id_ordine":
                order.id_ordine=ordersdict[k][i]
            if k=="date":
                order.date=ordersdict [k][i]
            if k=="client":
                order.client=ordersdict[k][i]

        order.save() #Salvo oggetto ordine sul db

        total_price=0
        for j in range(len(order_items_list[cont]["item"])): #Lunghezza del dizionario che contiene gli oggetti di ciascun ordine
            order_item=Ordine_Item() #Oggetto ordine_item
            
            for z in order_items_list[cont]:
                if z=="item":
                    order_item.item=order_items_list[cont][z][j]
                if z=="quantity":
                    order_item.quantity=order_items_list[cont][z][j]
                    q= order_items_list[cont][z][j]
                if z=="price":
                    order_item.price=round(order_items_list[cont][z][j]*q,2)
                
            order_item.save() #Salvo ordine_item nel database
            total_price+=order_item.price
            order.prodotti.add(order_item) #Aggiungo al mio ordine oggetto ordine_item
        
        order.total_price=round(total_price,2)
        cont+=1
        order.save() #Risalvo nel database oggetto ordine con gli ordini_item        
    
    #Aggiungo recensioni
    recensionidict={
        "prodotto":[prodotti[0],prodotti[12],   prodotti[7],prodotti[10],     prodotti[8],prodotti[11],    prodotti[5],    prodotti[13]],
        "valutation":[4,4,   5,2,   2,4,   5,    4],
        "date":[datetime.date(2023,1,19),datetime.date(2023,1,19),   datetime.date(2023,2,20),datetime.date(2023,2,20),      datetime.date(2023,3,11),datetime.date(2023,3,11),      datetime.date(2023,4,17),    datetime.date(2023,4,15)],
        "description":["ottimo prodotto","Ottime cuffie, grande qualità del suono!",    "Il miglior iphone di sempre!","Pensavo meglio, cover di scarsa qualità",        "Il peggior iphone di sempre!","Cover di ottima qualità",     "Televisore con risoluzione incredibile!",    "Cancellazione del rumore incredibile."   ],
        "client":[clienti[0],clienti[0],      clienti[0],clienti[0],       clienti[1],clienti[1],   clienti[1],    clienti[2]    ]

    }

    for i in range(8): #8 recensioni
        rec= Recensione()
        prodotto=Product()
        for k in recensionidict:
            if k =="prodotto":
                prodotto=recensionidict[k][i]
            if k=="valutation":
                rec.valutation=recensionidict[k][i]
            if k=="date":
                rec.date=recensionidict[k][i]
            if k=="description":
                rec.description=recensionidict[k][i]
            if k=="client":
                rec.client=recensionidict[k][i]
            
        rec.save()
        prodotto.recensioni.add(rec)
    
    print("-- Popolo il DB Orders e recensioni --\n")   
    
#Inizializzazione e popolamento tutti i DB
def erase_init_all():

    #Table User
    erase_db_Users() #Cancello DB User
    init_db_Users() #Inizializzo DB User

    #Table Products
    erase_db_Products() #Cancello DB Product
    init_db_Products() #Inizializzo DB Product

    #Table Orders e recensioni
    erase_db_Orders() #Cancello DB Orders
    init_db_Orders() #Inizializzo DB Orders

