Convert IRkernel Jupyter Notebooks to R Markdown
================================================

Usage
-----

.. code-block:: bash

    # Generate test.rmd
    $ ipynb2rmd test.ipynb

    # Generate test.rmd and run R Markdown to render as pdf
    $ ipynb2rmd test.ipynb --compile

    # Compile an already existing rmd file
    $ ipynb2rmd test.rmd --compile


Chunk Options
-------------

To use rmarkdown chunk options in your Jupyter notebook, start a code cell with `#r <chunk options>`.

Installation
------------

To install ipynb2rmd, simply:

.. code-block:: bash

    $ pip install ipynb2rmd

Requirements
------------

* https://github.com/IRkernel/IRkernel
* https://github.com/rstudio/rmarkdown


