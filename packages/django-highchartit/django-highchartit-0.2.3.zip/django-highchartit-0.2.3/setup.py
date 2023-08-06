import codecs
import re
from os import path
from setuptools import setup, find_packages


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def get_version(*file_paths):
    """Get the django-highchartit version without importing the module."""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-highchartit',
    version=get_version('chartit', '__init__.py'),
    packages=find_packages(exclude=["chartit_tests.*", "demoproject.*",
                                    "chartit_tests", "demoproject",
                                    "docs.*", "docs"]),
    description=("A Django app to plot charts and pivot charts directly from "
                 "the models. Uses HighCharts and jQuery JavaScript libraries "
                 "to render the charts on the webpage."),
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
    ],
    platforms='any',
    install_requires=[
        'simplejson',
    ],
    keywords='django charts',
    author='Hongsonggao',
    author_email='gmaclinuxer@gmail.com',
    maintainer='Hongsonggao',
    maintainer_email='gmaclinuxer@gmail.com',
    url='https://github.com/gmaclinuxer/django-highcharts.git',
    license='BSD',
    include_package_data=True,
    zip_safe=False,
)
