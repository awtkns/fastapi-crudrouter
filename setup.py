from setuptools import setup, find_packages
from distutils.util import convert_path


def get_version():
    ver_path = convert_path("fastapi_crudrouter/_version.py")
    with open(ver_path) as ver_file:
        main_ns = {}
        exec(ver_file.read(), main_ns)
        return main_ns["__version__"]


setup(
    name="fastapi-crudrouter",
    version=get_version(),
    author="Adam Watkins",
    author_email="hello@awtkns.com",
    packages=find_packages(exclude=("tests.*", "tests")),
    url="https://github.com/awtkns/fastapi-crudrouter",
    documentation="https://fastapi-crudrouter.awtkns.com/",
    license="MIT",
    description="A dynamic FastAPI router that automatically creates CRUD routes for your models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["fastapi"],
    python_requires=">=3.7",
    keywords=["fastapi", "crud", "restful", "routing", "generator", "crudrouter"],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
