Advanced Usage Recipes
======================


Load Balancer & Circuit Breaker
-------------------------------

General case
````````````

The example below shows how request can be made with load balancer and circuit breaker for the static list of hosts:

    >>> from ahoyhoy.utils import Host
    >>> host1, host2, host3 = Host('badhost2.bla', 80), Host('google.com', 80), Host('badhost3.bla', 80)
    >>>
    >>> from ahoyhoy.lb.providers import ListProvider
    >>> provider = ListProvider(host1, host2, host3)
    >>>
    >>> from ahoyhoy.lb import RoundRobinLB
    >>> rrlb = RoundRobinLB(provider)
    >>>
    >>> from ahoyhoy.client import ClientBuilder
    >>> client = ClientBuilder.with_lb(rrlb)
    >>> client.get('/')
    <Response [200]>
    >>> client.get('/')
    <Response [200]>
    >>> client.get('/')
    <Response [200]>

Let's walk through this example step by step.

    >>> from ahoyhoy.utils import Host
    >>> host1, host2, host3 = Host('badhost2.bla', 80), Host('google.com', 80), Host('badhost3.bla', 80)

All the hosts passed to the load balancer have to be named tuples with `address` and `port` parameters. By default protocol will be calculated automatically by the :meth:`service discovery adapter's method <ahoyhoy.servicediscovery.servicediscovery.ServiceDiscoveryAdapter.calculate_protocol>`. Later we'll show an example of how the protocol can be specified explicitly.

    >>> from ahoyhoy.lb.providers import ListProvider
    >>> provider = ListProvider(host1, host2, host3)

`Provider` is an interface for providing list of hosts to the load balancer. Custom providers have to be instantiated from the :class:`~ahoyhoy.lb.providers.iprovider.IProvider` class.

In our example we use :class:`~ahoyhoy.lb.providers.ListProvider`. All it does is returns the list of given earlier hosts.

Now it's time to create the load balancer instance and pass the provider into it. We're using round robin algorithm for this example.

    >>> from ahoyhoy.lb import RoundRobinLB
    >>> rrlb = RoundRobinLB(provider)

And finally the last step is to create a client, which will use our load balancer. 

    >>> from ahoyhoy.client import ClientBuilder
    >>> client = ClientBuilder.with_lb(rrlb)
    >>> client.get('/')
    <Response [200]>
    >>> client.get('/')
    <Response [200]>
    >>> client.get('/')
    <Response [200]>

Client has built-in circuit breaker algorithm, so if there's a *bad* host, it'll be marked as unavailable and won't be used for the further requests.


Another example with random load balancer
`````````````````````````````````````````
Here is another example with load balancer, but using random algorithm:

    >>> from ahoyhoy.utils import Host
    >>> host1, host2 = Host('badhost2.bla', 80), Host('google.com', 80)
    >>> from ahoyhoy.lb.providers import ListProvider
    >>> provider = ListProvider(host1, host2)
    >>> from ahoyhoy.lb import RandomLB
    >>> rrlb = RandomLB(provider)
    >>> from ahoyhoy.client import ClientBuilder
    >>> client = ClientBuilder.with_lb(rrlb)
    >>> client.get('/')
    <Response [200]>


Custom Retries
--------------

By default :class:`~ahoyhoy.client.ClientBuilder` with load balancer uses :func:`ahoyhoy.retries.Retry` function with 3 tries.
Custom retry function can be aslo passed to the :class:`~ahoyhoy.client.ClientBuilder`, for example:

    >>> from requests.exceptions import ConnectTimeout
    >>> from ahoyhoy.retries import Retry
    >>> retry = Retry(exceptions=ConnectTimeout, tries=2, delay=0, max_delay=None, backoff=2, jitter=1)
    >>> client = ClientBuilder.with_lb(rrlb, retry_http_call=retry)
    >>> client.get('/')
    <Response [200]>