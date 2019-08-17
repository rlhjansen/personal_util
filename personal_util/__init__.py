from pkg_resources import get_distribution

from .my_stuff import make_requirements, lprint

__version__ = get_distribution('personal_util').version
