from io import open

from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='django4-bootstrap-daterangepicker',
    version='1.0.7',

    description='A Django form field and widget wrapper for bootstrap-daterangepicker',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/jckw/django-bootstrap-daterangepicker/',

    author='Yuri Malinov, Jack Weatherilt, D',
    author_email='yurik.m@gmail.com, jackweatherilt@outlook.com, protasov.d.51@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django :: 4.0',
    ],

    keywords='daterangepicker django4 django daterange datetime date bootstrap picker',
    packages=['bootstrap_daterangepicker'],
    install_requires=[
        'django',
        'python-dateutil',
        'six'
    ],
    include_package_data=True,
)
