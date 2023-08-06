=========
django-suuze-upload
=========

|Build Status|

django-suuze-upload is a simple app that allows you to get suuze private file upload services
uptoken. Using this uptoken you can easily upload file with js-sdk in your project.

============
Requirements
============

* `Django <https://www.djangoproject.com/>`_ (1.9+)
* `requests <http://docs.python-requests.org/en/master/>`_ (2.11.1+)

============
Installation
============

* Install ``django-suuze-upload`` (or `download from PyPI <>`_):

.. code-block:: python

    pip install django-suuze-upload -i http://p.int.cdnzz.net:19883/simple/

* Add ``django_suuze_upload`` to ``INSTALLED_APPS`` in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = (
        # other apps
        "django_suuze_upload",
    )

* Configure your queues in django's ``settings.py``

.. code-block:: python

    SUUZE_UPLOAD_CONFIG = {
        # domain provide upload file service
        'domain': 'http://upload-file.cdnzz.com',
        # web app namn
        'app': 'upload-file-demo',
        # direction where holds uploaded file
        'path': 'app/upload',
        # access_key to generate uptoken
        'access_key': 'xxxxxxxx',
        # optional, in second, default is 1800
        # 'expire': 1800,
    }


=====
Usage
=====

Fetch uptoken in your project
-------------------------

`django-suuze-upload` allows you to upload file to suuze file store easily.

.. code-block:: python

    from django.views import View
    from django_suuze_upload import fetch_uptoken
    from django_suuze_upload import is_uptoken_expire
    from django_suuze_upload import upload_file

    class Dome(View):

        def post(self, request):
            ...
            uptoken = fetch_uptoken()['uptoken']
            ....
            # some logic to process upload file .etc
            # check uptoken is expire or not
            # is_uptoken_expire(uptoken)

            file_object = request.FILES['filw']
            rv = upload_file(uptoken, file_object)
            ....
