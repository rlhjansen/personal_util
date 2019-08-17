from setuptools import setup

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
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description="""small library for functions I use over and over again.
    Will probably split into different modules in the future""",
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
