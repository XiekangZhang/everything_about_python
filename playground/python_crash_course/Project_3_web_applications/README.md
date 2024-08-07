# Getting started with Django
[django query](https://docs.djangoproject.com/en/2.2/topics/db/queries/)
- creating a project in django: _django-admin startproject __name__ ._
- _manage.py_ is a short program that takes in commands --> working with databases and running servers

- _setting.py_: controls how Django interacts with your system and manages your project.
- _url.py_: tells Django which pages to build in response to browser requests.
- _wsgi.py_: helps Django serve the files it creates. (web server gateway interface)
- In Django's authentication system, every template has a _user_ variable available, which always
has an _is_authenticated_ attribute set.

## under app folder
- _models.py_: defines the data
- _admin.py_: register each model
- _views.py_

## Steps for creating Django Webserver
- define your own model in _models.py_ by using `class _class_name_(models.Model):`
- activate your model/app in _settings.py_ by adding ___app_name_ under INSTALLED_APPS__
- make migration by using _python manage.py makemigrations __app_name___
- apply this migration by using _python manage.py migrate_

## Steps for making pages
- defining URLs: adding _path('', include('_app_name_.urls'))_ into _urls.py_
- creating _urls.py_ in app folder with _path_ and _views_ import, and _app_name_ and _urlpatterns_ variables
- writing views: a view function takes in information from a request, prepares the data needed to generate a page,
and then sends the data back to the browser
- writing templates: defines what the page should look like. creating _templates/app_ folder under _app_ folder

## Page inheritance
- template tag: _{% url %}_, _{% extends %}_, _{% block/endblock name %}_
_ _{% for/endfor %}_, _{% empty %}_, _{% if form.errors %}_, _{% endif %}_
- _{% csrf_token %}_: prevent attackers from using the form to gain unauthorized access to the server
- In Django templates, a vertical line (|) represents a template filter -- a function that modifies the value in a 
template variable.
- _{% load bootstrap4 %}_: syntax to load bootstrap


## Create a superuser
- create a superuser by giving _python manage.py createsuperuser_
- register model into admin site under _admin.py_ by adding _admin.site.register(_model_name_)_

## Django Shell
- activate django shell by giving _python manage.py shell_
- access a model by using _from _app_name_.models import _model_name__
- list all information: __model_name_.objects.all()_
- get the specific information __model_name_.objects.get(id=*)_
  - other methods: id__exact, id__iexact, id__contains, id__icontains, id__startswith, id__istartswith, id__endswith, id__iendwith
  - Lookups: __model_name__related_model__attribute/contains/isnull_=*_
- find the related information (related with foreign key) by using __model_name_._model_name_set.all()_
- add a new model: _m=_model_name_(*)_ then _m.save()_
- update a model: _m.attribute=_new_value__ then _m.save()_ --> same for OneToManyField
- ManyToManyField use combination of __model_name_.objects.create(*)_ then __model_name_._mtmField_.add(_model_)_
- support exclude and filter methods: __model_name_.objects.exclude(*)_ and __model_name_.objects.filter(*)_
- support order by: __model_name_.objects.order_by(*)_

## ModelForm
- Any page that lets a user enter and submit information on a web page is a form.
- Create _from.py_ under the folder of _model.py_.
- Implement a class extends from _froms.ModelForm_ class, then define _Meta_ class
- Adjust _urls.py_ to include urlpatterns
- Implement the method in _views.py_ -> _request.method_, _form.is_valid()_, _form.save()_, _redirect()_
- Link to the page

## Others
- html: body --> nav --> main: Here we assign the bootstrap selector _container_, which is a simple way to group
elements on a page.
- a _jumbotron_, which is a large box that stands out from the rest of the page and can contain anything you want.

# Important commands
- _django-admin startproject __name__ ._
- _python manage.py migrate_
- _python manage.py runserver __port___
- _python manage.py startapp __name___: create needing infrastructure for building an app
- _python manage.py makemigrations __app_name___
- _python manage.py createsuperuser_
- _python manage.py shell_
- _python manage.py flush_: to rebuild the database structure. --> No user and no data anymore
- _pip install django-bootstrap4_