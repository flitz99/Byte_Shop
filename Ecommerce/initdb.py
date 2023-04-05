from products.models import *
from authentication.models import *
from django.db import connection

def erase_db():
    print("-- Cancello il DB --\n")
    Product.objects.all().delete() #Cancello oggetti table products

    cursor = connection.cursor()
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_product'; ''') #Resetta ID table products_product
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_smartphone'; ''') #Resetta ID table products_smartphone
    cursor.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='products_computer'; ''') #Resetta ID table products_computer

    

category = (
    ('computer'),
    ('smartphone')

)

def init_db():

    if len(Product.objects.all()) != 0:
        return

    #Se vuoto lo inizializzo

    #Lista prodotti
    productdict = {
        "image" : ["Apple_Iphone_13.jpg","Macbook_pro_M1Pro.jpg","Acer_aspire.jpg","Apple_Iphone_11.jpg","Macbook_air_2022.jpg","Acer_Predator_helios.jpg"],
        "name" : ["Iphone 13","Macbook Pro 14","Acer Aspire","Iphone 11","Macbook Air 2022","Acer Predator Helios 300"],
        "type" : [category[1],category[0],category[0],category[1],category[0],category[0]],
        "product_code" : ["172081","172534","183359","172013","176212","164300"  ],
        "productor" : ["Apple","Apple","Acer","Apple","Apple","Acer"  ],
        "color" : ["Black","Gray","Silver","Black","Gray","Black"  ],
        "size" : ["7x14x0.7","31.2x1.5x22","36.3x1.79x23.8","7.5x15x0.8","30.4x1.1x21.5","39.8x2.6x27.5"  ],
        "price" : [789.99,2499.99,799.99,549.99,1249.99,1599.99  ],
        "available" : [True,True,True,False,True,True  ],
        "quantity" : [13,7,5,0,4,2 ],
        "supplier_id" : [1,1,1,1,1,1  ],
        "weight" : [0.17,1.71,1.9,0.19,1.24,2.9  ],
    }

    computerdict = {
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
        "cpu":["A15 Bionic","A13 Bionic"],
        "ram":[4,4],
        "disk_size":[128,128],
        "operating_system":["IOS","IOS"],
        "battery_autonomy":[15,12],
        "camera":[12,12],
        "additional_function":["Doppia fotocamera","Display LCD"],
        "display_size":[6.1,6.1]

    }

    admin_1=User.objects.get(id=1) #Acquisisco oggetto amministratore 1

    lista_prodotti =[] #Creo lista contenente i prodotti per smistarli in base alla categoria dopo

    #Aggiungo prodotti
    for i in range(6): # 6 prodotti
        p = Product() #Oggetto prodotto
        for k in productdict:
            if k =="image":
                p.image=productdict[k][i]
            if k=="name":
                p.name=productdict[k][i]
            if k =="type":
                p.type=productdict[k][i] 
            if k=="product_code":
                p.product_code=productdict[k][i]
            if k=="productor":
                p.productor=productdict[k][i]
            if k=="color":
                p.color=productdict[k][i]
            if k =="size":
                p.size=productdict[k][i]
            if k=="price":
                p.price=productdict[k][i]
            if k =="available":
                p.available=productdict[k][i] 
            if k=="quantity":
                p.quantity=productdict[k][i]
            if k=="supplier_id":
                p.supplier=admin_1
            if k=="weight":
                p.weight=productdict[k][i]

        lista_prodotti.append(p)
        p.save() #Salvo prodotti nel DB


    c_computer=0   #Contatore per dizionario computer
    c_smartphone=0  #Contatore per dizionario smartphone

    for z in lista_prodotti:
        if z.type==category[1]:
            s =Smartphone() #Oggetto smartphone
            for k in smartphonedict:
                if k =="cpu":
                    s.cpu=smartphonedict[k][c_smartphone]
                if k =="ram":
                    s.ram=smartphonedict[k][c_smartphone]
                if k =="disk_size":
                    s.disk_size=smartphonedict[k][c_smartphone]
                if k =="battery_autonomy":
                    s.battery_autonomy=smartphonedict[k][c_smartphone]
                if k =="operating_system":
                    s.operating_system=smartphonedict[k][c_smartphone]
                if k =="camera":
                    s.camera=smartphonedict[k][c_smartphone]
                if k =="additional_function":
                    s.additional_function=smartphonedict[k][c_smartphone]
                if k =="display_size":
                    s.display_size=smartphonedict[k][c_smartphone]

            s.product=z #Assegno prodotto 
            c_smartphone=c_smartphone+1
            s.save()

        if z.type==category[0]:
            c =Computer() #Oggetto computer
            for k in computerdict:
                if k =="display_resolution":
                    c.display_resolution=computerdict[k][c_computer]
                if k=="cpu":
                    c.cpu=computerdict[k][c_computer]
                if k=="ram":
                    c.ram=computerdict[k][c_computer]
                if k=="disk_size":
                    c.disk_size=computerdict[k][c_computer]
                if k=="disk_type":
                    c.disk_type=computerdict[k][c_computer]
                if k=="operating_system":
                    c.operating_system=computerdict[k][c_computer]
                if k=="graphic_card":
                    c.graphic_card=computerdict[k][c_computer]
                if k=="battery_autonomy":
                    c.battery_autonomy=computerdict[k][c_computer]
                if k=="additional_function":
                    c.additional_function=computerdict[k][c_computer]
                if k=="display_size":
                    c.display_size=computerdict[k][c_computer]

            c.product=z #Assegno il prodotto
            c_computer=c_computer+1
            c.save()

    print("-- Popolo il DB --\n")


