.. image:: https://travis-ci.org/mobify/timberjack.svg?branch=master
   :target: https://travis-ci.org/mobify/timberjack
   :alt: Travis CI Status Badge

timberjack
##########

.. image:: http://lakequip.com/wp-content/uploads/2014/05/IMG_3865.jpg
   :alt: Timberjack Tractor


Install
-------

You can install ``timberjack`` directly from the Github repo using::

    $ pip install https://github.com/mobify/timberjack/archive/master.zip


Setup in Django
---------------

TBD.


Setup in Flask
--------------

The timberjack logging tools come with a convenience class that allows the easy
configuration of a Flask application to use logging::

    from timberjack.contrib.flask import Timberjack

    ...

    app = Flask(__name__)
    timberjack = Timberjack(app)

    ...

    log = timberjack.get_logger('my.logger')



License
-------

This code is licensed under the `MIT License`_.

.. _`MIT License`: https://github.com/mobify/timberjack/blob/master/LICENSE
