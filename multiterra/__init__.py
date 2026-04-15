from multiterra.storage.bucket import GeneralizedBucket, GeneralizedBucketArgs

from .generalized_cr import Deployment, GeneralizedCR
from .network import (
    GeneralizedSubnet,
    GeneralizedSubnetArgs,
    GeneralizedVPC,
    GeneralizedVPCArgs,
)
from .vm import GeneralizedImage, GeneralizedImageArgs, GeneralizedVM, GeneralizedVMArgs

__all__ = [
    "Deployment",
    "GeneralizedCR",
    "GeneralizedVPC",
    "GeneralizedVPCArgs",
    "GeneralizedSubnet",
    "GeneralizedSubnetArgs",
    "GeneralizedImage",
    "GeneralizedImageArgs",
    "GeneralizedVM",
    "GeneralizedVMArgs",
    "GeneralizedBucket",
    "GeneralizedBucketArgs",
]
