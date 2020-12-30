#! /usr/bin/env python
#
# Trading Technical Indicators (tti) Open Source Python Library
#
# License: MIT

import setuptools

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(name='tti',
    version='0.2.2',
    description='Trading Technical Indicators, python library. Where Traditional Technical Analysis and AI are met.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Office/Business :: Financial'
    ],
    url='https://www.trading-technical-indicators.org/',
    download_url='https://pypi.org/project/tti/#files',
    project_urls={
        'Bug Tracker': 'https://github.com/vsaveris/trading-technical-indicators/issues',
        'Documentation': 'https://www.trading-technical-indicators.org/api-docs',
        'Source Code': 'https://github.com/vsaveris/trading-technical-indicators'
    },
    author='Vasileios Saveris',
    author_email='vsaveris@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['pandas>=1.2.0', 'matplotlib>=3.3.3', 'numpy>=1.19.4', 'statsmodels>=0.12.1'],
    python_requires=">=3.8")
