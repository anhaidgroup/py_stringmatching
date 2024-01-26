import subprocess
import sys
import os

# check if pip is installed. If not, raise an ImportError
PIP_INSTALLED = True

try:
    import pip
except ImportError:
    PIP_INSTALLED = False

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        if not PIP_INSTALLED:
            raise ImportError('pip is not installed.')
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

# check if setuptools is installed. If not, install setuptools
# automatically using pip.
install_and_import('setuptools')

from setuptools.command.build_ext import build_ext as _build_ext

class build_ext(_build_ext):
    def build_extensions(self):
        import pkg_resources                                                            
        numpy_incl = pkg_resources.resource_filename('numpy', 'core/include')

        for ext in self.extensions:
            if (hasattr(ext, 'include_dirs') and
                    not numpy_incl in ext.include_dirs):
                ext.include_dirs.append(numpy_incl)
        _build_ext.build_extensions(self)

def generate_cython():
    cwd = os.path.abspath(os.path.dirname(__file__))
    print("Cythonizing sources")
    p = subprocess.call([sys.executable, os.path.join(cwd,
                                                      'build_tools',
                                                      'cythonize.py'),
                         'py_stringmatching'],
                        cwd=cwd)
    if p != 0:
        raise RuntimeError("Running cythonize failed!")


cmdclass = {"build_ext": build_ext}


if __name__ == "__main__":

    no_frills = (len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
                                         sys.argv[1] in ('--help-commands',
                                                         'egg_info', '--version',
                                                         'clean')))

    cwd = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(cwd, 'PKG-INFO')) and not no_frills:
        # Generate Cython sources, unless building from source release
        generate_cython()

    # specify extensions that need to be compiled
    extensions = [setuptools.Extension("py_stringmatching.similarity_measure.cython.cython_levenshtein",
                                       ["py_stringmatching/similarity_measure/cython/cython_levenshtein.c"],
                                       include_dirs=[]),
                  setuptools.Extension("py_stringmatching.similarity_measure.cython.cython_jaro",
                                       ["py_stringmatching/similarity_measure/cython/cython_jaro.c"],
                                       include_dirs=[]),
                  setuptools.Extension("py_stringmatching.similarity_measure.cython.cython_jaro_winkler",
                                       ["py_stringmatching/similarity_measure/cython/cython_jaro_winkler.c"],
                                       include_dirs=[]),
                  setuptools.Extension("py_stringmatching.similarity_measure.cython.cython_utils",
                                       ["py_stringmatching/similarity_measure/cython/cython_utils.c"],
                                       include_dirs=[]),
                  setuptools.Extension("py_stringmatching.similarity_measure.cython.cython_needleman_wunsch",
                                       ["py_stringmatching/similarity_measure/cython/cython_needleman_wunsch.c"],
                                       include_dirs=[]),
                  setuptools.Extension("py_stringmatching.similarity_measure.cython.cython_smith_waterman",
                                       ["py_stringmatching/similarity_measure/cython/cython_smith_waterman.c"],
                                       include_dirs=[]),
                  setuptools.Extension("py_stringmatching.similarity_measure.cython.cython_affine",
                                       ["py_stringmatching/similarity_measure/cython/cython_affine.c"],
                                       include_dirs=[])

                  ]
 
    # find packages to be included. exclude benchmarks.
    packages = setuptools.find_packages(exclude=["benchmarks", "benchmarks.custom_benchmarks"])

    with open('README.rst') as f:
        LONG_DESCRIPTION = f.read()

    setuptools.setup(
        name='py_stringmatching',
        version='0.4.3',
        description='Python library for string matching.',
        long_description=LONG_DESCRIPTION,
        url='https://sites.google.com/site/anhaidgroup/projects/magellan/py_stringmatching',
        author='UW Magellan Team',
        author_email='uwmagellan@gmail.com',
        license='BSD',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Education',
            'License :: OSI Approved :: BSD License',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Topic :: Scientific/Engineering',
            'Topic :: Utilities',
            'Topic :: Software Development :: Libraries',
        ],
        packages=packages,
        install_requires=[
            'numpy >= 1.7.0',
            'six'
        ],
        setup_requires=[
            'numpy >= 1.7.0'                                                   
        ],
        ext_modules=extensions,
        cmdclass=cmdclass,
        include_package_data=True,
        zip_safe=False
    )
