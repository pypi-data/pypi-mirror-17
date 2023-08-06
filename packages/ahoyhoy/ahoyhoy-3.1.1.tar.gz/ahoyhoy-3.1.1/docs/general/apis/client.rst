Client
------

Client is a wrapper for HTTP calls which allows to use load balancers, circuit breakers and retries.

.. module:: ahoyhoy.client

.. autoclass:: Client
   :members:

.. autofunction:: SimpleClient


ClientBuilder
-------------

ClientBuilder provides convenient api for creating the specific :class:`~ahoyhoy.client.Client` instance.

.. autoclass:: ClientBuilder
   :members:


Client exceptions
`````````````````

.. module:: ahoyhoy.client.exceptions

.. autoclass:: NoAvailableEndpointsClientException
   :members:

.. autoclass:: AhoyhoyRequestsException
   :members:
