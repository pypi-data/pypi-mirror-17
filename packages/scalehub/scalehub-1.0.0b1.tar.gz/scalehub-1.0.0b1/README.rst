ScaleHub
=================
Python test automation framework
---------------------------------

.. image:: https://travis-ci.org/pyscale/scalehub.svg?branch=master
    :target: https://travis-ci.org/pyscale/scalehub

Usage
^^^^^

::

  import time
  from scalehub.hub import ScaleHub

  config = {
    'workers': [
        {
            'id': 'worker01',
            'driver_class': ClassName,
            'driver_config': {
                'any_attribute': 'any_value'
            }
        },
    ],
  }

  hub = ScaleHub(config)
  hub.go()

  while not hub.is_test_completed():
    print hub.collect_results()
    time.sleep(1)

Where ``config`` must contain ``workers`` array. Each worker config must contain the next attributes:

* ``id`` - worker unique identifier
* ``driver`` - worker driver class full path

Into ``driver_config`` attribute you may put any configuration your worker need.

Method ``go()`` just calls ``init_workers()`` and then ``start_test()``. You can call these methods manually.
