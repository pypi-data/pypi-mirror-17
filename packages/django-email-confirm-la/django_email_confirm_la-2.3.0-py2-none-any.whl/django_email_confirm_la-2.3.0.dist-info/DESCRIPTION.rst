Copyright (c) 2014 Vinta

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Description: django-email-confirm-la
        =======================
        
        .. image:: http://img.shields.io/travis/vinta/django-email-confirm-la/master.svg?style=flat-square
            :target: https://travis-ci.org/vinta/django-email-confirm-la
        
        .. image:: https://img.shields.io/coveralls/vinta/django-email-confirm-la/master.svg?style=flat-square
            :target: https://coveralls.io/github/vinta/django-email-confirm-la
        
        .. image:: http://img.shields.io/pypi/v/django-email-confirm-la.svg?style=flat-square
            :target: https://pypi.python.org/pypi/django-email-confirm-la
        
        Django email confirmation for any Model and any Field.
        
        Requirements
        ============
        
        - Python (2.6, 2.7, 3.3, 3.4, 3.5)
        - Django (1.5, 1.6, 1.7, 1.8, 1.9)
        
        Installation
        ============
        
        .. code-block:: bash
        
            $ pip install django-email-confirm-la
        
        
        In your ``settings.py``:
        
        Add the ``email_confirm_la`` app (put it *after* your apps) and set the required settings:
        
        .. code-block:: python
        
            INSTALLED_APPS = (
                ...
                'your_app',
                'email_confirm_la',
                ...
            )
        
            EMAIL_CONFIRM_LA_HTTP_PROTOCOL = 'https'
            EMAIL_CONFIRM_LA_DOMAIN = 'vinta.ws'
            EMAIL_CONFIRM_LA_AUTOLOGIN = True
            EMAIL_CONFIRM_LA_TEMPLATE_CONTEXT = {
                'THE_ANSWER': 42,
            }
        
        If you are using the `sites <https://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_ framework, then ``EMAIL_CONFIRM_LA_DOMAIN`` can be omitted and ``Site.objects.get_current().domain`` will be used.
        
        In your ``urls.py``:
        
        .. code-block:: python
        
            urlpatterns = [
                ...
                url(r'^email_confirmation/', include('email_confirm_la.urls', namespace='email_confirm_la')),
                ...
            ]
        
        then run
        
        .. code-block:: bash
        
            $ python manage.py migrate
        
        Models
        ======
        
        For User Model
        ==============
        
        .. code-block:: python
        
            from django.contrib.auth.models import User
            from email_confirm_la.models import EmailConfirmation
        
            user = User.objects.get(username='vinta')
            email = 'vinta.chen@gmail.com'
            EmailConfirmation.objects.verify_email_for_object(email, user)
        
        For Any Model And Any Field
        ===========================
        
        Assumed you have a model:
        
        .. code-block:: python
        
            from django.db import models
            from django.contrib.contenttypes.fields import GenericRelation  # Django 1.7+
            from django.contrib.contenttypes.generic import GenericRelation
        
            class YourModel(models.Model):
                ...
                customer_support_email = models.EmailField(max_length=255, null=True, blank=True)
                marketing_email = models.EmailField(max_length=255, null=True, blank=True)
                ...
        
                # optional, but recommended when you want to perform cascade-deletions
                email_confirmations = GenericRelation('email_confirm_la.EmailConfirmation', content_type_field='content_type', object_id_field='object_id')
        
        And you want to verify some emails:
        
        .. code-block:: python
        
            from your_app.models import YourModel
            from email_confirm_la.models import EmailConfirmation
        
            some_model_instance = YourModel.objects.get(id=42)
        
            EmailConfirmation.objects.verify_email_for_object(
                email='marvin@therestaurantattheendoftheuniverse.com',
                content_object=some_model_instance,
                email_field_name='customer_support_email'
            )
        
            EmailConfirmation.objects.verify_email_for_object(
                email='arthur.dent@therestaurantattheendoftheuniverse.com',
                content_object=some_model_instance,
                email_field_name='marketing_email'
            )
        
        Signals
        =======
        
        - ``post_email_confirmation_send``
        - ``post_email_confirmation_confirm``
        
        In your ``models.py``:
        
        .. code-block:: python
        
            from django.dispatch import receiver
            from email_confirm_la.signals import post_email_confirmation_confirm
        
            @receiver(post_email_confirmation_confirm)
            def post_email_confirmation_confirm_callback(sender, confirmation, **kwargs):
                model_instace = confirmation.content_object
                email = confirmation.email
                old_email = kwargs['old_email']
        
                do_your_stuff()
        
        Commands
        ========
        
        .. code-block:: bash
        
            $ python manage.py clear_expired_email_confirmations
        
        Templates
        =========
        
        You will want to override the project's email message and confirmation pages.
        
        Ensure the ``email_confirm_la`` app in ``INSTALLED_APPS`` is after the app that you will place the customized templates in so that the `django.template.loaders.app_directories.Loader <https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.app_directories.Loader>`_ finds *your* templates first.
        
        There are following template that you can override:
        
        * ``email_confirm_la/email/email_confirmation_subject.txt``: Produces the subject line of the email.
        * ``email_confirm_la/email/email_confirmation_message.html``: The HTML body of the email.
        * ``email_confirm_la/email_confirmation_success.html``: What the user sees after clicking a confirmation link (on success).
        * ``email_confirm_la/email_confirmation_fail.html:`` What the user sees after clicking a invalid confirmation link.
        * ``email_confirm_la/email_confirmation_expiration.html:`` What the user sees after clicking an expired confirmation link.
        
        Settings
        ========
        
        Default values of app settings:
        
        .. code-block:: python
        
            EMAIL_CONFIRM_LA_HTTP_PROTOCOL = 'http'
            EMAIL_CONFIRM_LA_DOMAIN = 'example.com'
            EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC = 60 * 60 * 24 * 1  # 1 day
            EMAIL_CONFIRM_LA_CONFIRM_URL_REVERSE_NAME = 'email_confirm_la:confirm_email'
            EMAIL_CONFIRM_LA_TEMPLATE_CONTEXT = {}
            EMAIL_CONFIRM_LA_AUTOLOGIN = False
        
        Run Tests
        =========
        
        .. code-block:: bash
        
            $ pip install -r requirements_test.txt
            $ python setup.py test
        
            # or
        
            $ docker build -t email_confirm_la .
            $ docker run --rm=true -v `pwd`:/app email_confirm_la
        
        
        Changes
        =======
        
        2.3.0 (2016-09-09)
        ++++++++++++++++++
        
        - Support automatically login after email confirmation via `EMAIL_CONFIRM_LA_AUTOLOGIN` setting
        - Use `uuid.uuid4()` to generate confirmation key
        
        
        2.2.0 (2016-07-25)
        ++++++++++++++++++
        
        - Fix migration dependencies
        - New parameter ``old_email`` in `post_email_confirmation_confirm` signal
        
        
        2.1.0 (2016-07-25)
        ++++++++++++++++++
        
        - Reset migration
        - Fix ``EmailConfirmationValidator``
        
        
        2.0.0 (2016-07-22)
        ++++++++++++++++++
        
        - **v2.0.0 is a BACKWARD-INCOMPATIBLE release!**
        - Full refactoring
        - Drop support for Django 1.4
        
        
        0.2.3 (2015-03-08)
        ++++++++++++++++++
        
        - Fix `#14 <https://github.com/vinta/django-email-confirm-la/issues/14>`_ Admin raises an `AttributeError` when `content_object` doesn't exist
        
        
        0.2.2 (2014-11-13)
        ++++++++++++++++++
        
        - New admin action: Re-send confirmation email
        - New setting: ``EMAIL_CONFIRM_LA_EMAIL_BACKEND``
        - Change ``EMAIL_CONFIRM_LA_DOMAIN`` default value to ``''``, fail fast
        - Fix circular import
        
        
        0.2.1 (2014-11-09)
        ++++++++++++++++++
        
        - Django 1.6 compatibility: ``transaction.atomic``
        - Django 1.4 compatibility: ``update_fields``
        
        
        0.2.0 (2014-11-08)
        ++++++++++++++++++
        
        - Django 1.7 compatibility: ``migrations``
        
        
        0.1.0 (2014-10-31)
        ++++++++++++++++++
        
        - Initial release
        
Keywords: django,email,mail,confirm,confirmation,content type
Platform: UNKNOWN
Classifier: Development Status :: 4 - Beta
Classifier: Environment :: Web Environment
Classifier: Framework :: Django
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Operating System :: OS Independent
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.6
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Topic :: Communications :: Email
Classifier: Topic :: Internet
Classifier: Topic :: Software Development :: Libraries
Classifier: Topic :: Software Development :: Libraries :: Python Modules
Classifier: Topic :: Utilities
