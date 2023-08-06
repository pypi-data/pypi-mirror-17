
=====
Django translation client
=====

Polls is a simple Django app to conduct Web-based polls. For each
question, visitors can choose between a fixed number of answers.


Requirements
-----------

requests
django-translation-server # Installed in local or remote server

Quick start
-----------

1. Add "translation_client" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'translation_client',
    ]

2. Add the "translation_server" URL like this::

    TRANSLATION_SERVER_URL = u"http://localhost:8001/api/translation"

3. Run `python manage.py sync_translation` to sync the server with the client.
