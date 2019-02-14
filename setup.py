import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='materials',
    version='0.0.0',
    author='Matthew Vernacchia',
    author_email='mvernacc@mit.edu',
    description='Material properties database',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mvernacc/material-properties-interchange',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
