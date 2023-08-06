Advanced Usage Recipes
======================


Load Balancer & Circuit Breaker
-------------------------------

General case
````````````

The following example shows how a request can be made using a load balancer and circuit breaker with a static list of hosts:

    >>> from ahoyhoy.utils import Host
    >>> host1, host2, host3 = Host('badhost2.bla', 80), Host('google.com', 80), Host('badhost3.bla', 80)
    >>>
    >>> from ahoyhoy.lb.providers import ListProvider
    >>> provider = ListProvider(host1, host2, host3)
    >>>
    >>> from ahoyhoy.lb import RoundRobinLB
    >>> rrlb = RoundRobinLB(provider)
    >>>
    >>> from ahoyhoy.client import LBClientBuilder
    >>> client = LBClientBuilder().add_lb(rrlb).build()
    >>> client.get('/')
    <Response [200]>
    >>> client.get('/')
    <Response [200]>
    >>> client.get('/')
    <Response [200]>


Let's walk through this example step by step.

    >>> from ahoyhoy.utils import Host
    >>> host1, host2, host3 = Host('badhost2.bla', 80), Host('google.com', 80), Host('badhost3.bla', 80)

All hosts passed to the load balancer should be `Host` named tuples containing `address` and `port` fields. The default protocol (http or https) will be calculated automatically by the :meth:`service discovery adapter's method <ahoyhoy.servicediscovery.servicediscovery.ServiceDiscoveryAdapter.calculate_protocol>`.

    >>> from ahoyhoy.lb.providers import ListProvider
    >>> provider = ListProvider(host1, host2, host3)

`Provider` is an interface for providing list of hosts to the load balancer. Custom providers should be derived from the :class:`~ahoyhoy.lb.providers.iprovider.IProvider` class.

In this example we use :class:`~ahoyhoy.lb.providers.ListProvider`. It simply returns the list of hosts from before.

Now we create the load balancer instance and give it the provider. We use a round robin algorithm for this example.

    >>> from ahoyhoy.lb import RoundRobinLB
    >>> rrlb = RoundRobinLB(provider)

And finally we create a client, using our load balancer.

    >>> from ahoyhoy.client import LBClientBuilder
    >>> client = LBClientBuilder().add_lb(rrlb).build()
    >>> client.get('/')
    <Response [200]>
    >>> client.get('/')
    <Response [200]>
    >>> client.get('/')
    <Response [200]>

Client has built-in circuit breaker algorithm, so if there's a *bad* host, it'll be marked as unavailable and won't be used for further requests.


Another load balancer example
`````````````````````````````
Here's another load balancer example, using the random algorithm:

    >>> from ahoyhoy.utils import Host
    >>> host1, host2 = Host('badhost2.bla', 80), Host('google.com', 80)
    >>> from ahoyhoy.lb.providers import ListProvider
    >>> provider = ListProvider(host1, host2)
    >>> from ahoyhoy.lb import RandomLB
    >>> rrlb = RandomLB(provider)
    >>> from ahoyhoy.client import LBClientBuilder
    >>> client = LBClientBuilder().add_lb(rrlb).build()
    >>> client.get('/')
    <Response [200]>


Custom Retries
--------------

By default a :class:`~ahoyhoy.client.LBClientBuilder`'s load balancer uses a :func:`ahoyhoy.retries.Retry` object set to do 3 tries.

Custom `Retry` objects may be passed to :class:`~ahoyhoy.client.LBClientBuilder` like so:

    >>> from requests.exceptions import ConnectTimeout
    >>> from ahoyhoy.retries import Retry
    >>> retry = Retry(exceptions=ConnectTimeout, tries=2, delay=0, max_delay=None, backoff=2, jitter=1)
    >>> client = LBClientBuilder().add_lb(rrlb).add_retries(retry).build()
    >>> client.get('/')
    <Response [200]>

Setting the protocol (http or https)
------------------------------------

Http is used by default. To use Https, simply make sure that your `Host` uses port 443.

    >>> host1 = Host('api.service.com', 443)
