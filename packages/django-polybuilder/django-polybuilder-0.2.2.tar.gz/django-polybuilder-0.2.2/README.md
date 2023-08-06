Django Polybuilder
==================

Django Polybuilder let you create your own Web Componets easily from Django admin.

Quick start
-----------

1. Add "polybuilder" to INSTALLED_APPS:

    INSTALLED_APPS = {
        ...
        'polybuilder'
    }

2. Include the myblog URLconf in urls.py:

    url(r'^', include('polybuilder.urls'))

3. Run `python manage.py migrate` to create myblog's models.

4. Run the development server and access http://127.0.0.1:8000/ to manage blog posts.

