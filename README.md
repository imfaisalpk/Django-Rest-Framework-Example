# Build a Rest API with Django/Python

This is a basic guide on how to build a REST API with Django & Python.


Software
Django 1.11.8
Python 3.6.3
Django Rest Framework 3.7.3
Django Rest Framework JWT 1.11.0



Initial Setup
```
virtualenv -p python3 restapi-basics

# activate it 
# mac: `source bin/activate`
# windows: `.\Scripts\activate`

pip install django==1.11.8 djangorestframework==3.7.3 djangorestframework-jwt==1.11.0

mkdir src && cd src

django-admin startproject cfehome .
django-admin startapp postings

python manage.py runserver

# For API testing

python manage.py test

```



