import glob
import os.path
import platform
import sys
import warnings

from setuptools import Extension, setup

NAME = 'implicit'
VERSION = '0.1.3'
SRC_ROOT = 'implicit'


try:
    from Cython.Build import cythonize
    has_cython = True
except ImportError:
    has_cython = False

is_dev = 'dev' in VERSION
use_cython = is_dev or '--cython' in sys.argv or '--with-cython' in sys.argv
if '--no-cython' in sys.argv:
    use_cython = False
    sys.argv.remove('--no-cython')
if '--without-cython' in sys.argv:
    use_cython = False
    sys.argv.remove('--without-cython')
if '--cython' in sys.argv:
    sys.argv.remove('--cython')
if '--with-cython' in sys.argv:
    sys.argv.remove('--with-cython')


if use_cython and not has_cython:
    if is_dev:
        raise RuntimeError('Cython required to build dev version of %s.' % NAME)
    warnings.warn('Cython not installed. Building without Cython.')
    use_cython = False


def find_files(dir_path, extension):
    for root, _, files in os.walk(dir_path):
        for name in files:
            if name.endswith(extension):
                yield os.path.join(root, name)


def import_string_from_path(path):
    return os.path.splitext(path)[0].replace('/', '.')


def define_extensions(use_cython=False):
    compile_args = ['-Wno-unused-function', '-O3', '-fopenmp', '-ffast-math']
    link_args = ['-fopenmp']

    if 'anaconda' not in sys.version.lower():
        compile_args.append('-march=native')

    src_ext = '.pyx' if use_cython else '.c'

    modules = [
        Extension(import_string_from_path(filepath), [filepath], language='c',
                  extra_compile_args=compile_args, extra_link_args=link_args)
        for filepath in find_files(SRC_ROOT, src_ext)
    ]

    if use_cython:
        return cythonize(modules)
    else:
        return modules


# set_gcc copied from glove-python project
# https://github.com/maciejkula/glove-python

def set_gcc():
    """
    Try to find and use GCC on OSX for OpenMP support.
    """
    # For macports and homebrew
    patterns = ['/opt/local/bin/gcc-mp-[0-9].[0-9]',
                '/opt/local/bin/gcc-mp-[0-9]',
                '/usr/local/bin/gcc-[0-9].[0-9]',
                '/usr/local/bin/gcc-[0-9]']

    if 'darwin' in platform.platform().lower():
        gcc_binaries = []
        for pattern in patterns:
            gcc_binaries += glob.glob(pattern)
        gcc_binaries.sort()

        if gcc_binaries:
            _, gcc = os.path.split(gcc_binaries[-1])
            os.environ["CC"] = gcc

        else:
            raise Exception('No GCC available. Install gcc from Homebrew '
                            'using brew install gcc.')


set_gcc()


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description='Collaborative Filtering for Implicit Datasets',
    long_description=long_description,
    url='http://github.com/benfred/implicit/',
    author='Ben Frederickson',
    author_email='ben@benfrederickson.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Cython',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'],

    keywords='Matrix Factorization, Implicit Alternating Least Squares, '
             'Collaborative Filtering, Recommender Systems',

    packages=[SRC_ROOT],
    install_requires=['numpy', 'scipy>=0.16'],
    setup_requires=["Cython >= 0.19"],
    ext_modules=define_extensions(use_cython),
    test_suite="tests",
)
