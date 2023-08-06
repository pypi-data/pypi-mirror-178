from dataclasses import dataclass, field
from typing import Iterable, Optional, Tuple, Union

from pymemcache.serde import PickleSerde

from .types import unpackable

PICKLE_VERSION = 5  # python >= 3.8

__all__ = ["ParallelConfig", "MemcachedClientConfig", "MemcachedConfig"]


@dataclass
class ParallelConfig:
    """Configuration for parallel computation backend.

    :param backend: Type of backend to use. For now only 'ray' is supported.
    :param address: Address of existing remote or local cluster to use.
    :param num_workers: Number of workers (CPUs) to use.
    """

    backend: str = "ray"
    address: Optional[Union[str, Tuple[str, int]]] = None
    num_workers: Optional[int] = None


@unpackable
@dataclass
class MemcachedClientConfig:
    """Configuration for the connection to the memcached server.

    :param server: tuple of (server, port).
    :param connect_timeout: seconds to wait for a connection to memcached.
    :param timeout: seconds to wait for send or recv calls on the socket
        connected to memcached.
    :param no_delay: set the `TCP_NODELAY` flag, which may help with performance
        in some cases.
    :param serde: a serializer / deserializer ("serde"). The default
        `PickleSerde` should work in most cases. See `pymemcached's
        documentation
        <https://pymemcache.readthedocs.io/en/latest/apidoc/pymemcache.client.base.html#pymemcache.client.base.Client>`_
        for details.
    """

    server: Tuple[str, int] = ("localhost", 11211)
    connect_timeout: float = 1.0
    timeout: float = 1.0
    no_delay: bool = True
    serde: PickleSerde = PickleSerde(pickle_version=PICKLE_VERSION)


@unpackable
@dataclass
class MemcachedConfig:
    """Configuration for :func:`~pydvl.utils.caching.memcached`, providing
    memoization of function calls.

    Instances of this class are typically used as arguments for the construction
    of a :class:`~pydvl.utils.utility.Utility`.

    :param client_config: Configuration for the connection to the memcached
        server.
    :param time_threshold: computations taking less time than this many seconds
        are not cached.
    :param allow_repeated_evaluations: If `True`, repeated calls to a function
        with the same arguments will be allowed and outputs averaged until the
        running standard deviation of the mean stabilises below
        `rtol_stderr * mean`.
    :param rtol_stderr: relative tolerance for repeated evaluations. More
        precisely, :func:`~pydvl.utils.caching.memcached` will stop evaluating
        the function once the standard deviation of the mean is smaller than
        `rtol_stderr * mean`.
    :param min_repetitions: minimum number of times that a function evaluation
        on the same arguments is repeated before returning cached values. Useful
        for stochastic functions only. If the model training is very noisy, set
        this number to higher values to reduce variance.
    :param ignore_args: Do not take these keyword arguments into account when
        hashing the wrapped function for usage as key in memcached.
    """

    client_config: MemcachedClientConfig = field(default_factory=MemcachedClientConfig)
    time_threshold: float = 0.3
    allow_repeated_evaluations: bool = True
    rtol_stderr: float = 0.1
    min_repetitions: int = 3
    ignore_args: Optional[Iterable[str]] = None
