Ahoyhoy's Objects Hierarchy
===========================

ClientBuilder
-------------

:class:`~ahoyhoy.client.ClientBuilder` serves as the factory for the :class:`~ahoyhoy.client.Client` instance. :class:`~ahoyhoy.client.Client` is an object which allows to delegate HTTP calls through the load balancer and the circuit breaker.

ClientBuilder with session
````````````````````````````

When :meth:`ClientBuilder.with_session() <ahoyhoy.client.ClientBuilder.with_session>` is used, it returns the :class:`~ahoyhoy.endpoints.Endpoint` object which contains passed session. Then all HTTP calls will be delegated to that session but including optional callbacks and retries.

:meth:`ClientBuilder.with_session(my_session) <ahoyhoy.client.ClientBuilder.with_session>` -> :func:`SimpleClient(session=my_session) <ahoyhoy.client.SimpleClient>` -> :func:`SimpleHttpEndpoint(session=my_session) <ahoyhoy.endpoints.SimpleHttpEndpoint>` -> :class:`Endpoint(session=my_session) <ahoyhoy.endpoints.Endpoint>` -> :class:`~requests.Session`

Custom HTTP retry function and headers also can be provided together with the session. For more complex cases it is recommended to equip your custom session with all needed parameters (such as headers, adapters etc.).

*TODO: for now there's no way to provide custom callbacks to the Endpoint*

:class:`~ahoyhoy.endpoints.Endpoint` concept will be described below.

ClientBuilder with load balancer
``````````````````````````````````

:meth:`ClientBuilder.with_lb() <ahoyhoy.client.ClientBuilder.with_lb>` is more complicated case. Tt uses load balancers and it'll still delegate all HTTP calls to the session. But there's no specific session. Every time the call is made, LB resolves the new Host  and the new :class:`~ahoyhoy.endpoints.Endpoint`. That's why such actions like `client.headers.update(...)` are impossible in this case and will throw an `AttributeError`. Only HTTP calls are allowed.

:meth:`ClientBuilder.with_lb(lb) <ahoyhoy.client.ClientBuilder.with_lb>` -> :class:`Client(lb=lb) <ahoyhoy.client.Client>`

:meth:`Client.get('/') <ahoyhoy.client.Client.get>` -> :meth:`client._lb.resolve() resolves Host <ahoyhoy.lb.iloadbalancer.ILoadBalancer.pick>` -> :class:`Endpoint(host=Host) <ahoyhoy.endpoints.Endpoint>` -> :attr:`Endpoint._session=ServiceDiscoveryHttpClient(Host) <ahoyhoy.servicediscovery.ServiceDiscoveryHttpClient>` -> :class:`~ahoyhoy.http.proxy.SessionProxy` -> :class:`~requests.Session`

:class:`~ahoyhoy.servicediscovery.ServiceDiscoveryHttpClient` figures out the protocol by given `Host.addres` and `Host.port` and returns full URL.

:class:`~ahoyhoy.http.proxy.SessionProxy` allows to use callbacks for HTTP calls.

Endpoint
--------

:class:`~ahoyhoy.endpoints.Endpoint` inherits from :class:`~ahoyhoy.circuit.Circuit`. It delegates HTTP calls to the session, but can also keep the state (open or closed) to allow or not allow making further calls to it.

*TODO: add separate thread to update Endpoint's state.*
