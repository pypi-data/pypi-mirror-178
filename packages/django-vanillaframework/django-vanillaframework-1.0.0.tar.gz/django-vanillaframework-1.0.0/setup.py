"""Setup.py file."""
from setuptools import setup
from vanillaframework import __version__

setup(
    name='django-vanillaframework',
    version=__version__,
    packages=["vanillaframework"],
    url='https://github.com/lvoytek/django-vanillaframework',
    license='LGPL v3',
    author='Lena Voytek',
    author_email='lena@voytek.dev',
    description='Vanilla Framework frontend for Django',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'django>=3.2'
    ]
)
