from setuptools import setup

setup(
    name='PackageName',
    version='0.1.0',
    author='Adam Watkins',
    author_email='cadamrun@gmail.com',
    packages=['fastapi_crudrouter'],
    url='http://pypi.python.org/pypi/PackageName/',
    license='LICENSE.txt',
    description='An awesome package that does something',
    long_description=open('README.txt').read(),
    install_requires=[
       "Django >= 1.1.1",
       "pytest",
    ],
)