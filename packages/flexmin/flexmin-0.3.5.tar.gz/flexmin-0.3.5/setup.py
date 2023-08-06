import subprocess
import re
from setuptools import setup


def get_version():
    regex = re.compile("__version__\s*\=\s*['\"](?P<version>.+?)['\"]")
    return regex.findall(open("flexmin/__init__.py").read())[0]


setup(
    name="flexmin",
    version=get_version(),
    url="https://creativeedgedigital.co.uk/flexmin",
    license="BSD",
    author="Richard Cooke",
    author_email="contact_flexmin_pypi@creativeedgedigital.co.uk",
    maintainer="Richard Cooke",
    maintainer_email="contact_flexmin_pypi@creativeedgedigital.co.uk",
    description="A flexible system admin web portal",
    long_description="""
    Flexmin is a web administration interface for system administartors.
    
    It includes a service that runs in the background as root, and a 
    web application (based on PY4WEB) that provides a user friendly
    interface for common administration tasks.
    
    This can be useful for developers to manage a web development server
    or those managing a small network.
    """,
    packages=["flexmin", "flexmin.utils"],
    package_data={"flexmin": ["assets/*"],},
    install_requires=[
        "py4web",
        "click",
        "pyyaml"
    ],
    entry_points={"console_scripts": ["flexmin=flexmin.flexmin_cli:cli"],},
    zip_safe=False,
    platforms="linux",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Systems Administration",
    ],
)
