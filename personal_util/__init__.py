from pkg_resources import get_distribution

from .my_stuff import make_requirements, lprint

__version__ = get_distribution('personal_util').version
print(__version__)
print("100% yeet")
input()
