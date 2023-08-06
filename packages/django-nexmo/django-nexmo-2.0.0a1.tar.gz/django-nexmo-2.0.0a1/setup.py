import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-nexmo',
    version='2.0.0-alpha1',
    packages=['djexmo'],
    include_package_data=True,
    license='MIT',
    description='A simple Django app to send text messages using the Nexmo api.',
    long_description=README,
    url='https://github.com/thibault/django-nexmo',
    author='Thibault Jouannic',
    author_email='thibault@miximum.fr',
    setup_requires=('setuptools'),
    install_requires=[
        'nexmo',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
