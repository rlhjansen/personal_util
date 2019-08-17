from distutils.core import setup

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
    version=0.1,
    description="""small library for functions I use over and over again.
    Will probably split into different modules in the future""",
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
