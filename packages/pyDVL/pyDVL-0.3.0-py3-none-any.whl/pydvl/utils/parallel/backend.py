import os
from dataclasses import asdict
from typing import Any, Iterable, List, Optional, Tuple, TypeVar, Union

import ray
from ray import ObjectRef
from ray.remote_function import RemoteFunction

from ..config import ParallelConfig

__all__ = [
    "init_parallel_backend",
    "available_cpus",
]

T = TypeVar("T")

_PARALLEL_BACKEND: Optional["RayParallelBackend"] = None


class RayParallelBackend:
    """Class used to wrap ray to make it transparent to algorithms. It shouldn't
    be initialized directly. You should instead call `init_parallel_backend`.

    :param config: instance of :class:`~pydvl.utils.config.ParallelConfig` with
        cluster address, number of cpus, etc.

    :Example:

    >>> from pydvl.utils.parallel.backend import RayParallelBackend
    >>> from pydvl.utils.config import ParallelConfig
    >>> config = ParallelConfig(backend="ray")
    >>> parallel_backend = RayParallelBackend(config)
    >>> parallel_backend
    <RayParallelBackend: {'address': None, 'num_cpus': None}>

    """

    def __init__(self, config: ParallelConfig):
        config_dict = asdict(config)
        config_dict.pop("backend")
        config_dict["num_cpus"] = config_dict.pop("num_workers")
        self.config = config_dict
        ray.init(**self.config)

    def get(
        self,
        v: Union[ObjectRef, Iterable[ObjectRef], T],
        *,
        timeout: Optional[float] = None,
    ) -> Union[T, Any]:
        if isinstance(v, ObjectRef):
            return ray.get(v, timeout=timeout)
        elif isinstance(v, Iterable):
            return [self.get(x, timeout=timeout) for x in v]
        else:
            return v

    def put(self, x: Any, **kwargs) -> ObjectRef:
        return ray.put(x, **kwargs)  # type: ignore

    def wrap(self, *args, **kwargs) -> RemoteFunction:
        return ray.remote(*args, **kwargs)  # type: ignore

    def wait(
        self,
        object_refs: List["ray.ObjectRef"],
        *,
        num_returns: int = 1,
        timeout: Optional[float] = None,
    ) -> Tuple[List[ObjectRef], List[ObjectRef]]:
        return ray.wait(  # type: ignore
            object_refs,
            num_returns=num_returns,
            timeout=timeout,
        )

    def effective_n_jobs(self, n_jobs: Optional[int]) -> int:
        if n_jobs == 0:
            raise ValueError("n_jobs == 0 in Parallel has no meaning")
        elif n_jobs is None or n_jobs < 0:
            ray_cpus = int(ray._private.state.cluster_resources()["CPU"])  # type: ignore
            eff_n_jobs = ray_cpus
        else:
            eff_n_jobs = n_jobs
        return eff_n_jobs

    def __repr__(self) -> str:
        return f"<RayParallelBackend: {self.config}>"


def init_parallel_backend(config: ParallelConfig) -> "RayParallelBackend":
    """Initializes the parallel backend and returns an instance of it.

    :param config: instance of :class:`~pydvl.utils.config.ParallelConfig` with cluster address, number of cpus, etc.

    :Example:

    >>> from pydvl.utils.parallel.backend import init_parallel_backend
    >>> from pydvl.utils.config import ParallelConfig
    >>> config = ParallelConfig(backend="ray")
    >>> parallel_backend = init_parallel_backend(config)
    >>> parallel_backend
    <RayParallelBackend: {'address': None, 'num_cpus': None}>

    """
    global _PARALLEL_BACKEND
    if _PARALLEL_BACKEND is None:
        if config.backend == "ray":
            _PARALLEL_BACKEND = RayParallelBackend(config)
        else:
            raise NotImplementedError(f"Unexpected parallel type {config.backend}")
    return _PARALLEL_BACKEND


def available_cpus() -> int:
    """Platform-independent count of available cores.

    FIXME: do we really need this or is `os.cpu_count` enough? Is this portable?
    :return: Number of cores, or 1 if it is not possible to determine.
    """
    from platform import system

    if system() != "Linux":
        return os.cpu_count() or 1
    return len(os.sched_getaffinity(0))
