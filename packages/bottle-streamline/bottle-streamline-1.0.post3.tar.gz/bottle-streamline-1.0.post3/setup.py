import os
from setuptools import setup, find_packages


def read(fname):
        """ Return content of specified file """
        return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='bottle-streamline',
    description='Python module writing class-based route handlers in bottle.',
    keywords='bottle route class',
    version='1.0.post3',
    author='Outernet Inc',
    author_email='apps@outernet.is',
    license='BSD',
    url='https://github.com/Outernet-Project/bottle-streamline',
    long_description=read('README.rst'),
    packages=find_packages(),
    install_requires=['bottle'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)
