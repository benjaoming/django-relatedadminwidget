import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


template_patterns = [
    'templates/*.html',
    'templates/*/*.html',
    'templates/*/*/*.html',
    'static/*.js',
    'static/*.css',
    'static/*/*.js',
    'static/*/*.css',
    'static/*/*/*.js',
    'static/*/*/*.css',
]

packages = find_packages()

package_data = dict(
    (package_name, template_patterns)
    for package_name in packages
)

setup(
    name = "django-relatedadminwidget",
    version = "0.0.1",
    author = "Benjamin Bach",
    author_email = "benjamin@overtag.dk",
    description = ("Get edit and delete links in your django admin. A utility class to let your model admins inherit from."),
    license = "BSD",
    keywords = "django admin",
    packages=find_packages(),
    long_description=read('README.md'),
    zip_safe = False,
    install_requires=[
        'Django>=1.4',
      ],
    classifiers=[
    'Development Status :: 4 - Beta',
    'Topic :: Utilities',
    'License :: OSI Approved :: BSD License',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    ],
    include_package_data=True,
    package_data=package_data,
)
