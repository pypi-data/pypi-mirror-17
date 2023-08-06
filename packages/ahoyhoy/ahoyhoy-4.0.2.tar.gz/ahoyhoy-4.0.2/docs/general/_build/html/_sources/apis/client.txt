Client
------

Client is a wrapper for HTTP calls which allows to use load balancers, circuit breakers and retries.

.. module:: ahoyhoy.client

.. autoclass:: Client
   :members:

.. autofunction:: SimpleClient


Client Builders
---------------

ClientBuilder provides convenient api for creating the specific :class:`~ahoyhoy.client.Client` instance.

Abstract class:
```````````````

.. module:: ahoyhoy.client.builder

.. autoclass:: IClientBuilder
   :members:

.. module:: ahoyhoy.client

.. autoclass:: LBClientBuilder
   :show-inheritance:
   :members:

.. autoclass:: SessionClientBuilder
   :show-inheritance:
   :members:


Client exceptions
`````````````````

.. module:: ahoyhoy.client.exceptions

.. autoclass:: NoAvailableEndpointsClientException
   :members:

.. autoclass:: AhoyhoyRequestsException
   :members:
