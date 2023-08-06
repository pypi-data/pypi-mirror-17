
======================
Implementation Details
======================

For more information about face recognition algorithms, please check :ref:`bob.bio.face <bob.bio.face>` which contains several different algorithms to perform photometric enhancement of facial images are implemented.

Feature extractors
~~~~~~~~~~~~~~~~~~

For the time being, only the VGG face model is supported ( ``'vgg_features'``), but you can use any caffe model that you want by using the package caffe_extractor_


.. _caffe_extractor: http://pythonhosted.org/bob.ip.caffe_extractor/index.html
