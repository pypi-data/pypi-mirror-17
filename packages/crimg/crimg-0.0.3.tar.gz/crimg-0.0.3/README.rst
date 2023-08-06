crimg
=====

crimg uses `Pillow <http://pillow.readthedocs.io/en/latest/>`_
to crop and resize an image as appropriate for web
presentation.
It is a convenience package that allows image
resizing without aspect ratio distortion.

API
---

crimg contains one useful function, ``crimg.crop_resize``.
The function takes three arguments:

    * image: a `PIL image <http://pillow.readthedocs.io/en/latest/reference/Image.html>`_ object
    * size: a 2-tuple of (width,height);  at least one must be specified
    * exact_size: whether to scale up for smaller images  

See ``crimg.crop_resize.__doc__`` for the function
documentation.  ``crop_resize`` returns the cropped and resized PIL image.

Command Line
------------

The command line program, ``crimg``, is included in this python
package.  The help for the program is displayed by running
``crimg`` with no arguments or ``crimg --help``.
