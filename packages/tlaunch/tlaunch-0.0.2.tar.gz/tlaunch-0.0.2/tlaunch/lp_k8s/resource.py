from typing import NamedTuple, Optional, Tuple, Union


class ResourceRange(NamedTuple):
  requests: Optional[str]
  limits: Optional[str]


R = Union[ResourceRange, Tuple[str, Optional[str]], str, int, None]


class Resource:
  def __init__(self,
               cpu: R = None,
               memory: R = None,
               nvidia_gpu: R = None,
               nvidia_gpu_memory: R = None,
               nvidia_gpu_cores: R = None) -> None:
    self.resources = {
        'cpu': cpu,
        'memory': memory,
        'nvidia.com/gpu': nvidia_gpu,
        'nvidia.com/gpumem': nvidia_gpu_memory,
        'nvidia.com/gpucores': nvidia_gpu_cores
    }
    self.requests = {
        k: v if isinstance(v, str) else v[0] if isinstance(v, tuple) or isinstance(v, list) else v
        for k, v in self.resources.items() if v is not None
    }
    self.limits = {
        k: v if isinstance(v, str) else v[1] if isinstance(v, tuple) or isinstance(v, list) else v
        for k, v in self.resources.items() if v is not None
    }
