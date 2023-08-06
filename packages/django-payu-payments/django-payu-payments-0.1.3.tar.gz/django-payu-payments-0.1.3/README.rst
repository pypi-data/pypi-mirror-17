.. image:: https://codeclimate.com/github/michalwerner/django-payu-payments/badges/gpa.svg
   :target: https://codeclimate.com/github/michalwerner/django-payu-payments

.. image:: https://img.shields.io/pypi/v/django-payu-payments.svg
   :target: https://pypi.python.org/pypi/django-payu-payments

.. image:: https://img.shields.io/pypi/dm/django-payu-payments.svg
   :target: https://pypi.python.org/pypi/django-payu-payments

.. image:: https://img.shields.io/pypi/l/django-payu-payments.svg
   :target: https://pypi.python.org/pypi/django-payu-payments

Installation
============

1. Install via pip: ::

    pip install django-payu-payments

2. Add ``payu`` to INSTALLED_APPS: ::

    INSTALLED_APPS = [
        ...
        'payu',
        ...
    ]

3. Add URLs to URLConf: ::

    url(r'^payments/', include('payu.urls', namespace='payu')),


4. Run migrations: ::

    python manage.py migrate

Configuration
=============

Configuration is done via Django's ``settins.py`` file.

- ``PAYU_POS_ID``

    Your POS ID. If not provided the test payment value will be used.

- ``PAYU_MD5_KEY``

    Your MD5 key. If not provided the test payment value will be used.

- ``PAYU_SECOND_MD5_KEY``

    Your second MD5 key. If not provided the test payment value will be used.

- ``PAYU_CONTINUE_PATH``

    Specifies path on your website, where user should be redirected after payment (successful, or not).
    May be absolute path, like ``/some-page/`` or ``reverse('some:thing')``.
    This view should handle GET parameters ``error=501`` in case of failed payment and
    ``no_payment=1`` in case of payment with total equals 0, which is registered, but actually sent to PayU.

- ``PAYU_VALIDITY_TIME``

    Payment validity time (in seconds), after which it's canceled, if user did not take action.
    If not provided ``600`` will be used.

Create payment
==============

To create payment object you have to call ``Payment.create`` method: ::

    from payu.models import Payment


    description = 'Some stuff'
    products = [
        {
            'name': 'Some product',
            'unitPrice': 14.99,
            'quantity': 1
        },
        {
            'name': 'Some other product',
            'unitPrice': 3.19,
            'quantity': 4
        }
    ]
    buyer = {
        'email': 'john.doe@domain.com',
        'firstName': 'John',
        'lastName': 'Doe'
    }
    notes = 'This client is important for us, we should prioritize him.'

    payment = Payment.create(request, description, products, buyer, validity_time=300, notes)

``request`` is just Django HTTP request object, we need it to get buyer IP, and absolute URLs.

``validity_time`` is optional and overrides ``PAYU_VALIDITY_TIME`` setting.

``notes`` is optional, and used for storing internal information about payment.

``Payment.create`` will return two-key dictionary, containing ``Payment`` object and URL where buyer should be redirected, or ``False`` if not successful. ::

    {
        'object': <Payment object>,
        'redirect_url': 'https://...'
    }

Fetch payment's data
====================

To get data associated with payment you just need to retrieve ``Payment`` object: ::

    Payment.objects.get(...)

There are also few helpful methods, which you can call on ``Payment`` object:

- ``get_total_display()``

    Returns pretty formatted ``total`` value.

- ``get_products_table()``

    Returns pretty formatted table of products associated with payment.

- ``is_successful()``

    For ``status`` equal ``COMPLETED`` returns ``True``, otherwise ``False``.

- ``is_not_successful()``

    For ``status`` equal ``CANCELED`` or ``REJECTED`` returns ``True``, otherwise ``False``.


Changelog
=========

0.1.3
-----
- PEP8 fixes

0.1.2
-----
- changelog added
- ``get_total_display()``,  ``get_products_table()``, ``is_successful()`` and ``is_not_successful()`` methods added
- JSONField is not Postgres-only anymore
- ``Payment.create()`` now returns two-key dictionary instead of just redirect URL
- ``Payment`` objects are now ordered from newest to oldest, by default
- compiled translation is now included in package
- settings moved to ``settings.py``
- settings is not dictionary anymore
- validity time added

JSONField and ordering related changes requires you to take some action when upgrading.

1) run migrations: ``python manage.py migrate payu``.

2) run following code, using Django shell (``python manage.py shell``): ::

    import json
    from payu.models import Payment


    for p in Payment.objects.all():
        if isinstance(p.products, str):
             p.products = json.loads(p.products)
             p.save()

0.1.1
-----
- sum added to products table

0.1.0
-----
- initial version
