import os
import setuptools

import asoke

with open(os.path.join(os.path.dirname(__file__), 'README')) as f:
    _long_description = f.read()

setuptools.setup(
    name         = 'asoke',
    version      = asoke.__version__,
    author       = 'AXY',
    author_email = 'axy@declassed.art',
    description  = 'A simple class-based dispatcher for ASGI apps and a quickstart wrapper',

    long_description = _long_description,
    long_description_content_type = 'text/x-rst',

    url = 'https://declassed.art/repository/asoke',

    packages = [
        'asoke'
    ],

    install_requires=[
        'hypercorn',
        'starlette',
        'uvloop'
    ],

    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Topic :: Internet :: WWW/HTTP'
    ],

    python_requires = '>=3.6',
)
