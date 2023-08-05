import os
from setuptools import setup


def read(file_name: str):
    """Utility function to read the README file.
    Args:
    :param file_name: (str) Name of file to open"""
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


# implementation
setup(
    name='jam65st_distributions',
    version='0.1.2',
    author='Jaime Alexander Mendez Medina',
    author_email='jam65st@gmail.com',
    description='Gaussian distributions',
    license='MIT',
    keywords='udacity AWS machine learning foundations',
    packages=['jam65st_distributions', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console :: Curses',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Education :: Testing',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities'
    ],
    zip_safe=False
)
