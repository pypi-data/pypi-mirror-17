Endpoint
--------

Endpoint is a derivative class from the :class:`~ahoyhoy.circuit.Circuit`. It delegates all HTTP calls ot the session (which is one of the Endpoint's attributes), but can also keep a state. If Endpoint was called and request failed, it'll change its state from closed to open.

Another feature of Endpoint is callbacks. It accepts pre-, post- and exception- callbacks, which allows to do corresponding actions with request, response and exceptions handling.

.. module:: ahoyhoy.endpoints

.. autoclass:: Endpoint
    :show-inheritance:

    .. automethod:: get

    .. automethod:: post

    .. automethod:: put

    .. automethod:: head

    .. automethod:: patch

    .. automethod:: delete

    .. autoattribute:: host

    .. autoattribute:: state

    .. automethod:: set_headers

    .. automethod:: set_retry


.. autofunction:: SimpleHttpEndpoint