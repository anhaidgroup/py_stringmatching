============
Installation
============
 
Requirements
------------
    * Python 3.7-3.11
    * C or C++ compiler (parts of the package are in Cython for efficiency reasons, and you need C or C++ compiler to compile these parts)

Platforms
------------
py_stringmatching has been tested on Linux (Ubuntu 22.04), OS X (Monterey 12), and Windows 10.

Dependencies
------------
    * numpy 1.7.0 or higher
    * six

.. note::

     The py_stringmatching installer will automatically install the above required packages.

C Compiler Required
-------------------
Before installing this package, you need to make sure that you have a C compiler installed. This is necessary because this package contains Cython files. Go `here <https://sites.google.com/site/anhaidgroup/projects/magellan/issues>`_ for more information about how to check whether you already have a C compiler and how to install a C compiler.

After you have confirmed that you have a C compiler installed, you are ready to install the package. There are two ways to install py_stringmatching package: using pip or source distribution.

Installing Using pip
--------------------
The easiest way to install the package is to use pip, which will retrieve py_stringmatching from PyPI then install it::

    pip install py_stringmatching
    
Installing from Source Distribution
-------------------------------------
Step 1: Download the py_stringmatching package from `here
<https://sites.google.com/site/anhaidgroup/projects/py_stringmatching>`_.

Step 2: Unzip the package and execute the following command from the package root::

    python setup.py install
    
.. note::

    The above command will try to install py_stringmatching into the defaul Python directory on your machine. If you do not have installation permission for that directory then you can install the package in your home directory as follows::

        python setup.py install --user

    For more information see the StackOverflow `link
    <http://stackoverflow.com/questions/14179941/how-to-install-python-packages-without-root-privileges>`_.

.. note::

    Building C files from source requires Cython version 0.29.23 or higher::
    
        pip install Cython>=0.29.23

