Load Balancers
--------------

There are two load balancing algorithms available for now:

 - random
 - round robin

Base class
``````````

.. module:: ahoyhoy.lb.iloadbalancer

.. autoclass:: ILoadBalancer
   :members:

Load blancers algorithms
````````````````````````

.. module:: ahoyhoy.lb

.. autoclass:: RandomLB
    :show-inheritance:
    :members:

.. autoclass:: RoundRobinLB
    :show-inheritance:
    :members:


Load blancers exceptions
````````````````````````

.. module:: ahoyhoy.lb.exceptions

.. autoclass:: NoAvailableEndpointsLbException


Providers
---------

Providers exist to give lists of hosts

Base class
``````````
.. module:: ahoyhoy.lb.providers.iprovider

.. autoclass:: IProvider
   :members:

List Provider
`````````````

.. module:: ahoyhoy.lb.providers

.. autoclass:: ListProvider
    :show-inheritance:
    :members:
