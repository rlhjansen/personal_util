from distutils.core import setup
import re, io

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
    io.open('personal_util/__init__.py', encoding='utf_8_sig').read()
    ).group(1)
# The beautiful part is, I don't even need to check exceptions here.
# If something messes up, let the build process fail noisy, BEFORE my release!

# The beautiful part is, I don't even need to check exceptions here.
# If something messes up, let the build process fail noisy, BEFORE my release!

setup(
     # Needed to silence warnings (and to be a worthwhile package)
    name='personal_util',
    url='https://github.com/rlhjansen/personal_util',
    author='Reitze Jansen',
    author_email='rlh.jansen@outlook.com',
    # Needed to actually package something
    packages=['personal_util'],
    # Needed for dependencies
    install_requires=[],
    # The license can be anything you like
    license='MIT',
    version=__version__,
    description="""small library for functions I use over and over again.
    Will probably split into different modules in the future""",
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
