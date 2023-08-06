============
Growler-Sass
============

|pypi-version| |travis| |coveralls|

A Growler_ middleware package for rendering sass_ files into CSS
to be sent to the browser.

This implementation uses libsass_ as the backend.

Usage
-----

This package provides the SassMiddleware class exposed in ``growler.ext``, as
well as the 'standard' location of ``growler_sass``.
As a middleware class, objects are given to the application object in the order
they should be called after receiving a client's request. This object checks
for the existence of a

Example
~~~~~~~

If you have a sass source files named ``client/style/neat_style.sass`` with contents:

.. code:: sass

    body
      > p
        color: red

And a python script to run a webapp, ``server/app.py``

.. code:: python

    # MUST be called like this! You cannot use import growler.ext.SassMiddleware
    from growler.ext import SassMiddleware
    from growler import App

    app = App("SassExample")

    app.use(SassMiddleware(source="client/style", dest='/styles'))
    ...

    @app.get("/")
    def index(req, res):
       res.send_html("""<!DOCTYPE html>
       <html>
       <head>
         <link href='/styles/neat_style.css' rel='stylesheet'>
         </head>
       <body>
         <p>This text should be red!</p>
         </body>
       </html>""")

    app.create_server_and_run_forever(...)

A request made to ``/styles/neat_style.css`` will return the compiled contents
of ``neat_style.sass``:

.. code:: css

   body > p {
     color: red; }


License
-------

This python package is licensed under the MIT license.


.. _Growler: https://github.com/pyGrowler/Growler
.. _sass: http://sass-lang.com/
.. _libsass: https://hongminhee.org/libsass-python/


.. |pypi-version| image:: https://img.shields.io/pypi/v/growler-sass.svg
                  :target: https://pypi.python.org/pypi/growler-sass/
                  :alt: Latest PyPI version


.. |travis| image:: https://travis-ci.org/pyGrowler/growler-sass.svg?branch=master
            :target: https://travis-ci.org/pyGrowler/growler-sass/branches?branch=master
            :alt: Testing Report (Master Branch)

.. |coveralls| image:: https://coveralls.io/repos/github/pyGrowler/growler-sass/badge.svg?branch=master
               :target: https://coveralls.io/github/pyGrowler/growler-sass?branch=master
               :alt: Coverage Report (Master Branch)
