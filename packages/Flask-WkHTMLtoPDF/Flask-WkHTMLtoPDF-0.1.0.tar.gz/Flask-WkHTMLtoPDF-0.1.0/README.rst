Flask-WkHTMLtoPDF
=================

|build status| |doc status|

Flask-WkHTMLtoPDF allows you to easily convert JavaScript dependent
Flask templates into PDFs with wkhtmltopdf. For complete documentation,
please visit
http://flask-wkhtmltopdf.readthedocs.org/en/latest/?badge=latest.

Installation
------------

Install the extension with one of the following commands:

.. code:: sh

    $ easy_install flask-wkhtmltopdf

or alternatively if you have pip installed:

.. code:: sh

    $ pip install flask-wkhtmltopdf

You will also need to install the WkHTMLtoPDF command line library from
http://wkhtmltopdf.org/downloads.html. Alternatively, you can install
from the command line for unix based machines by finding the appropriate
distrubution on http://download.gna.org/wkhtmltopdf/0.12/0.12.2.1/. For
instance, for linux:

.. code:: sh

    $ wget http://download.gna.org/wkhtmltopdf/0.12/0.12.2.1/wkhtmltox-0.12.2.1_linux-precise-amd64.deb
    $ sudo dpkg -i wkhtmltox-0.12.2.1_linux-precise-amd64.deb

Usage
-----

First setup in your main Flask file.

.. code:: python

    from flask_wkhtmltopdf import Wkhtmltopdf

            app = Flask(__name__)
            wkhtmltopdf = Wkhtmltopdf(app)

Then add these to your app's config

.. code:: python


    WKHTMLTOPDF_BIN_PATH = r'C:\Program Files\wkhtmltopdf\bin' #path to your wkhtmltopdf installation.
    PDF_DIR_PATH =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'pdf')

To convert a flask template into a PDF, simply use the
render\_template\_to\_pdf() function.

.. code:: python

    render_template_to_pdf('test.html', download=True, save=False, param='hello')

Contributing
------------

Contributions are more than welcomed. Please follow these steps:

1. Fork this repository
2. Make your changes
3. Test your changes locally: ``$ python setup.py test``
4. Submit a pull request

.. |build status| image:: https://travis-ci.org/chris-griffin/flask-wkhtmltopdf.svg?branch=master
   :target: https://travis-ci.org/chris-griffin/flask-wkhtmltopdf
.. |doc status| image:: http://readthedocs.org/projects/flask-wkhtmltopdf/badge/?version=latest
   :target: http://flask-wkhtmltopdf.readthedocs.org/en/latest/?badge=latest
