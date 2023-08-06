.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. Fri 17 Jul 02:49:53 2016 CEST

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.ip.caffe_extractor/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bob/bob.ip.caffe_extractor/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.bio.base/badges/master/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.ip.caffe_extractor/commits/master
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.ip.caffe_extractor
.. image:: http://img.shields.io/pypi/v/bob.ip.caffe_extractor.png
   :target: https://pypi.python.org/pypi/bob.ip.caffe_extractor
.. image:: http://img.shields.io/pypi/dm/bob.ip.caffe_extractor.png
   :target: https://pypi.python.org/pypi/bob.ip.caffe_extractor


=================================================
 Bob interface for feature extraction using Caffe
=================================================

This package contains functionality to extract features from CNNs trained with caffe http://caffe.berkeleyvision.org/


Installation
------------
To install this package -- alone or together with other `Packages of Bob <https://github.com/idiap/bob/wiki/Packages>`_ -- please read the `Installation Instructions <https://github.com/idiap/bob/wiki/Installation>`_.
For Bob_ to be able to work properly, some dependent packages are required to be installed.
Please make sure that you have read the `Dependencies <https://github.com/idiap/bob/wiki/Dependencies>`_ for your operating system.

Documentation
-------------
For further documentation on this package, please read the `Latest Version <https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.ip.caffe_extractor/master/index.html>`_ of the documentation.


.. warning::    

  For this package it is assumed that you followed ALL the installation instructions for the package caffe (http://caffe.berkeleyvision.org/installation.html).  
  The code below is one option to make caffe visible inside this python package:

.. code-block:: sh

   $ export PYTHONPATH=$PYTHONPATH:/<CAFFE-DIR>/python


This package also wrapps the VGG face model trained by Oxford (http://www.robots.ox.ac.uk/~vgg/software/vgg_face/).
To automatically download the model, please run the script below. More details on how to use it, please go to the reference manual.

.. code-block:: sh

   $ ./bin/download_VGG.py download
  
  
  
.. warning::
  For pycaffe, if you are at IDIAP, I recommend to install all the caffe python dependencies in a virtualenv or with miniconda.



.. _bob: https://www.idiap.ch/software/bob
