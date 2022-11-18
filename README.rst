The PayPal API provides simple client for  RESTful APIs

=======
Install
=======

.. code-block:: bash

    pip install paypal_client

=======
Example
=======

.. code-block:: python

    from paypal_client.src.api import PayPal

    APP_CLIENT_ID = 'APP_CLIENT_ID'
    APP_SECRET = 'APP_SECRET'
    paypal = PayPal(APP_CLIENT_ID, APP_SECRET)
    paypal.list_products()
    paypal.list_plans()
    paypal.create_order(UUID, 20)

=======
Donation
=======

.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
  :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YYZQ6ZRZ3EW5C
