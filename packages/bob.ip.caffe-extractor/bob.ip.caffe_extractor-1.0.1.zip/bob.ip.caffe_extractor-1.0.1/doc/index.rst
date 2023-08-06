.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. Fri 17 Jul 02:49:53 2016 CEST

.. _bob.ip.caffe_extractor:

=================================================
 Bob interface for feature extraction using Caffe
=================================================

This package contains functionality to extract features from CNNs trained with caffe http://caffe.berkeleyvision.org/.


.. note::
   Please make sure that caffe is installed and the PYTHONPATH is set to caffe. This package does not handle this dependency.
   
      
   
The code below is one option to make caffe visible inside this package:

.. code-block:: sh

   $ export PYTHONPATH=$PYTHONPATH:/<CAFFE-DIR>/python


This package also wrapps the VGG face model trained by Oxford (http://www.robots.ox.ac.uk/~vgg/software/vgg_face/).
To automatically download the model, please run the script below. More details on how to use it, please go to the reference manual.

.. code-block:: sh

   $ ./bin/download_VGG.py download


===========
 User guide
===========

Using as a feature extractor
----------------------------

In this example we take the output of the layer `fc7` as features.

.. doctest::
   >>> import bob.ip.caffe_extractor
   >>> img = bob.io.base.load(bob.io.base.test_utils.datafile('8821.hdf5', 'bob.ip.caffe_extractor')) # doctest: +SKIP
   >>> caffe_extractor = bob.ip.caffe_extractor.VGGFace("fc7")
   >>> print caffe_extractor(img)[0:5] # Printing the 5 first features
   [ -0.55280662  12.35865593  -1.54516721 -13.75179291   2.49704742]


Using as a convolutional filter
-------------------------------

In this example we plot some outputs of the convolutional layer `conv2_1`.

.. plot:: plot/convolve.py
   :include-source: False


===========
 Python API
===========

.. toctree::
   :maxdepth: 2

   py_api
