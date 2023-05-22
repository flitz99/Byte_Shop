# Byte_Shop
Progetto di tecnologie Web realizzato da Filippo Reggiani, Matricola 148084

## Libraries

```
pipenv, version 2022.1.8
Django v.4.0.5 
bootstrap v.5.3.0
Chart.js: v.4.2.1
```

## Preparing the environment

```
git clone https://github.com/flitz99/Byte_Shop.git
cd Byte_Shop
pipenv install -r requirements.txt && pipenv shell
```

## Apply and create migrations

```
python manage.py makemigrations
python manage.py migrate
```

## Initialize the DB with some data

```
Uncomment the method erase_init_all() in Ecommerce/urls.py
```

## Run project

```
python manage.py runserver
```

## Do test

```
python manage.py test
```

