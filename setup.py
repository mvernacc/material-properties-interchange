"""Standard python setup script for materials."""
import setuptools

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

with open('LICENSE.md', 'r') as fh:
    LICENSE = fh.read()

setuptools.setup(
    name='materials',
    version='0.0.0',
    author='Matthew Vernacchia',
    author_email='mvernacc@mit.edu',
    description='Material properties database',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/mvernacc/material-properties-interchange',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=['scipy', 'numpy', 'pyyaml'],
    keywords='material analysis-script engineering material-properties mmpds',
    license=LICENSE
)
