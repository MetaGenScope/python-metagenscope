"""
MetaGenScope-CLI is used to upload data sets to the MetaGenScope web platform.
"""
from setuptools import find_packages, setup

dependencies = ['click', 'requests', 'configparser']

setup(
    name='metagenscope',
    version='0.1.1',
    url='https://github.com/bchrobot/python-metagenscope',
    license='MIT',
    author='Benjamin Chrobot',
    author_email='benjamin.chrobot@alum.mit.edu',
    description='MetaGenScope-CLI is used to upload data sets to the MetaGenScope web platform.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'metagenscope = metagenscope_cli.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
