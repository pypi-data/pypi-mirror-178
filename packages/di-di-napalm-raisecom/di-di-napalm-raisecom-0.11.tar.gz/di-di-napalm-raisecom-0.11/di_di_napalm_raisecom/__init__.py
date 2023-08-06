"""napalm_ros package."""

# Import stdlib
import pkg_resources

# Import local modules
from di_di_napalm_raisecom.raisecom import NapalmRaisecomDriver

try:
    __version__ = pkg_resources.get_distribution('napalm-raisecom').version
except pkg_resources.DistributionNotFound:
    __version__ = "Not installed"

__all__ = ('NapalmRaisecomDriver', )
