import os
import re
import setuptools


with open('README.md', 'r') as rf:
    with open('CHANGELOG.md', 'r') as cf:
        long_description = rf.read() + cf.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()

    return re.search('__version__ = [\'"]([^\'"]+)[\'"]', init_py).group(1)


version = get_version('pxd_massaffect')


setuptools.setup(
    name='px-django-massaffect',
    version=version,
    author='Alex Tkachenko',
    author_email='preusx.dev@gmail.com',
    license='MIT License',
    description='Factory to make modular model multi-configurations.',
    install_requires=(
        'django-nested-admin>=4.0.0,<5.0.0',
        'django-polymorphic>=3.1.0,<4.0.0',
        'px-formula>=0.1.1,<0.2.0',
        'px-settings>=0.1.3,<0.2.0',
        'px-pipeline>=0.1.2,<0.2.0',
    ),
    include_package_data=True,
    extras_require={
        'dev': (
            'psycopg2-binary',
            'pytest>=6.0,<7.0',
            'pytest-watch>=4.2,<5.0',
            'pytest-django>=4.3,<5.0',
            'coverage==6.4.2',
            'django-environ==0.4.5',
            'django-stubs',
            'django==4.1',
            'twine',
        ),
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=(
        'tests', 'tests.*',
        'experiments', 'pilot',
    )),
    python_requires='>=3.6',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',

        'Programming Language :: Python :: 3',

        'Intended Audience :: Developers',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
