Ahoyhoy's Objects Hierarchy
===========================

ClientBuilder
-------------

:class:`~ahoyhoy.client.ClientBuilder` serves as the factory for the :class:`~ahoyhoy.client.Client` instance. :class:`~ahoyhoy.client.Client` is an object which makes HTTP calls using the load balancer and circuit breaker.

ClientBuilder with session
``````````````````````````

In the simple case, load balancing isn't used. When :meth:`ClientBuilder.with_session() <ahoyhoy.client.ClientBuilder.with_session>` is used, it returns an :class:`~ahoyhoy.endpoints.Endpoint` object which contains the session passed to it. All HTTP calls will then be delegated to that session, including optional callbacks and retries.

:meth:`ClientBuilder.with_session(my_session) <ahoyhoy.client.ClientBuilder.with_session>` -> :func:`SimpleClient(session=my_session) <ahoyhoy.client.SimpleClient>` -> :func:`SimpleHttpEndpoint(session=my_session) <ahoyhoy.endpoints.SimpleHttpEndpoint>` -> :class:`Endpoint(session=my_session) <ahoyhoy.endpoints.Endpoint>` -> :class:`~requests.Session`

Custom HTTP Retry objects, and custom HTTP headers can also be provided to the session. For complex cases it is recommended to create a custom Session with any needed parameters (such as headers, adapters etc.).

*TODO: for now there's no way to provide custom callbacks to the Endpoint*

An :class:`~ahoyhoy.endpoints.Endpoint` is described below.

ClientBuilder with load balancers
`````````````````````````````````

:meth:`ClientBuilder.with_lb() <ahoyhoy.client.ClientBuilder.with_lb>` on the otherhand uses load balancing, and still delegates HTTP calls to the Session. With each call, the LB resolves a new Host and :class:`~ahoyhoy.endpoints.Endpoint`, and the Endpoint is given the original Session. Actions such as `client.headers.update(...)` are impossible (the Session was created upfront) in this case and will throw an `AttributeError`. Only HTTP calls are allowed, but no other Session modifications are possible.

:meth:`ClientBuilder.with_lb(lb) <ahoyhoy.client.ClientBuilder.with_lb>` -> :class:`Client(lb=lb) <ahoyhoy.client.Client>`

:meth:`Client.get('/') <ahoyhoy.client.Client.get>` -> :meth:`client._lb.resolve() resolves Host <ahoyhoy.lb.iloadbalancer.ILoadBalancer.pick>` -> :class:`Endpoint(host=Host) <ahoyhoy.endpoints.Endpoint>` -> :attr:`Endpoint._session=ServiceDiscoveryHttpClient(Host) <ahoyhoy.servicediscovery.ServiceDiscoveryHttpClient>` -> :class:`~ahoyhoy.http.proxy.SessionProxy` -> :class:`~requests.Session`

:class:`~ahoyhoy.servicediscovery.ServiceDiscoveryHttpClient` uses `Host.address` and `Host.port` to calculate the full URL.

:class:`~ahoyhoy.http.proxy.SessionProxy` allows the use of callbacks with Requests HTTP calls.

Endpoint
--------

:class:`~ahoyhoy.endpoints.Endpoint` inherits from :class:`~ahoyhoy.circuit.Circuit`. It delegates HTTP calls to the Session, while maintaining circuit breaking state (open or closed), which allows or prevents further HTTP calls from being made.

*TODO: add separate thread to update Endpoint's state.*
