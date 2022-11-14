# Getting started with Django
- creating a project in django: _django-admin startproject __name__ ._
- _manage.py_ is a short program that takes in commands --> working with databases and running servers

- _setting.py_: controls how Django interacts with your system and manages your project.
- _url.py_: tells Django which pages to build in response to browser requests.
- _wsgi.py_: helps Django serve the files it creates. (web server gateway interface)

## under app folder
- _models.py_: defines the data
- _admin.py_
- _views.py_

## Steps for creating Django Webserver
- define your own model in _models.py_ by using `class _class_name_(models.Model):`
- activate your model/app in _settings.py_ by adding ___app_name_ under INSTALLED_APPS__
- make migration by using _python manage.py makemigrations __app_name___
- apply this migration by using _python manage.py migrate_

## Create a superuser
- create a superuser by giving _python manage.py createsuperuser_
- register model into admin site under _admin.py_ by adding _admin.site.register(_model_name_)_

## Django Shell
- activate django shell by giving _python manage.py shell_
- access a model by using _from _app_name_.models import _model_name__
- list all information: __model_name_.objects.all()_
- get the specific information __model_name_.objects.get(id=*)_
- find the related information (related with foreign key) by using __model_name_._model_name_set.all()_

# Important commands
- _django-admin startproject __name__ ._
- _python manage.py migrate_
- _python manage.py runserver __port___
- _python manage.py startapp __name___: create needing infrastructure for building an app
- _python manage.py makemigrations __app_name___
- _python manage.py createsuperuser_
- _python manage.py shell_