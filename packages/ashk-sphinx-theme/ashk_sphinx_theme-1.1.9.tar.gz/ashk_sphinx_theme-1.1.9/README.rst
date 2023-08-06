**************************
Readme
**************************
this is a rtl theme for Sphinx_.
i use `Read the Docs`_ as a base. and change it .

.. _Sphinx: http://www.sphinx-doc.org
.. _Read the Docs: http://www.readthedocs.org

Installation
================================

This theme is distributed on PyPI_ and can be installed with ``pip``:

.. code:: console

   $ pip install ashk-sphinx-theme

To use the theme in your Sphinx project, you will need to edit
your ``conf.py`` file's ``html_theme`` setting:

.. code:: python

    html_theme = "sphinx_rtd_theme"


.. _PyPI: https://pypi.python.org/pypi/sphinx_rtd_theme

Development:
================================

for development first read `configuring the theme`_ .

tip: for upgrade and upload to pypi remember to change the version in both files: setup.cfg & setup.py



use python3.10

make a venv:

.. code:: bash

    python3.10 -m venv vevn
    source venv/bin/activate
    pip install -e '.[dev]'

if there was a problem with installation use you may want to use this:

.. code:: bash

    npm install webpack webpack-dev-server webpack-cli --save-dev
    webpack-dev-server --open --config webpack.dev.js
    python -m pip install build twine


.. code:: bash

    npm install
    npm run build
    python setup.py sdist bdist_wheel


.. _configuring the theme: https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html


Releasing the theme
================================
for release the theme use:

.. code:: bash

    rm -rf dist/
    python setup.py sdist bdist_wheel
    twine upload -r pypi --verbose dist/*