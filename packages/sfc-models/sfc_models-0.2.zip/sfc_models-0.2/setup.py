from setuptools import setup

with open('README.rst', 'r') as f:
    long_desc = f.read()

setup(
    name='sfc_models',
    packages=['sfc_models', 'sfc_models.gl_book'],
    version='0.2',
    description='Stock-Flow Consistent (SFC) model generation',
    long_description=long_desc,
    author='Brian Romanchuk',
    author_email='brianr747@gmail.com',
    keywords=['economics', 'SFC models'],
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: Apache Software License',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.0',
                 'Programming Language :: Python :: 3.1',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Other/Nonlisted Topic'
    ],
    url='https://github.com/brianr747/SFC_models',
)