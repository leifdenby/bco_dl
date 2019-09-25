from setuptools import setup

setup(
    name='bco_dl',
    version='0.1.0',
    author='Leif Denby',
    author_email='l.c.denby@leeds.ac.uk',
    description='Simple download interface for Barbados Cloud Observatory',
    long_description='',
    zip_safe=False,
    install_requires=open('requirements.txt').readlines(),
    packages=["bco_dl", ],
)
