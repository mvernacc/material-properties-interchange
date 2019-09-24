"""Standard python setup script for materials."""
import setuptools

INSTALL_REQUIRES = [
    'numpy',
    'scipy',
    'pyyaml',
    'asteval',
    ]
TEST_REQUIRES = [
    'pytest',
    'coverage',
    'pytest-cov',
    'matplotlib',
    ]
DOCS_REQUIRES = [
    'sphinx',
    'sphinx_rtd_theme',
    'sphinxcontrib-napoleon',
    ]

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
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'test': TEST_REQUIRES + INSTALL_REQUIRES,
        'docs': DOCS_REQUIRES + INSTALL_REQUIRES,
        },
    keywords='material analysis-script engineering material-properties mmpds',
    license=LICENSE,
    include_package_data=True,
)
