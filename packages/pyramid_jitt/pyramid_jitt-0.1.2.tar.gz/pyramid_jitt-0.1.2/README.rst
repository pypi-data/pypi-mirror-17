===============================
Pyramid Just-In-Time Templating
===============================

The `pyramid_jitt` package is a wrapper around the `jstc`_ JavaScript
template compiler that allows client-side templates to be defined in
disparate server-side files and be assembled, pre-compiled, packaged,
cached, and access-controlled for inline, deferred, and restricted
delivery.

.. IMPORTANT::

  As of 2016/10/09, "restricted" delivery (i.e. access-controlled
  delivery control of all or a subset of the templates) and
  per-template JIT rendering is not yet available.


Currently, `jQuery`_ (v1.9.1+) is required for non-inline template
delivery.


Project
=======

* Homepage: https://github.com/canaryhealth/pyramid_jitt
* Bugs: https://github.com/canaryhealth/pyramid_jitt/issues


Installation
============

.. code:: bash

  $ pip install pyramid_jitt


Usage
=====

Enable the package either in your INI file via:

.. code:: ini

  pyramid.includes =
    pyramid_beaker
    pyramid_jitt


(it is highly recommended to use `pyramid_beaker`_ for caching of
rendered templates) or in code in your package's application
initialization via:

.. code:: python

  def main(global_config, **settings):
    # ...
    config.include('pyramid_beaker')
    config.include('pyramid_jitt')
    # ...


Configure pyramid_jitt's behaviour by setting the various options in
your INI file (see the `Manual`_ for details), for example:

.. code:: ini

  # use pyramid_beaker for caching!
  cache.type                        = memory
  cache.regions                     = pyramid_jitt
  cache.pyramid_jitt.expire         = 3600

  # override all template attributes to disable deferred loading
  jitt.overrides.inline             = true

  # define where the "webapp" templates (Handlebars, in this case) are
  # located and disable pre-compilation (only for "webapp" templates)
  jitt.@webapp.assets               = myapp:static/scripts/**.hbs
  jitt.@webapp.overrides.precompile = false


Then, add the delivery payload to your HTML file, here a `Mako`_
example:

.. code:: mako

  <html>
    <body>

      ${request.registry.jitt.render('webapp')|n}

      <script type="text/javascript">
        // NOTE: this must come **after** the `jitt.render` call!
        $(function() {
          $('#Templates').data('jitt').ready(function() {
            // start your client-side app that uses your templates here!...
          });
        });
      </script>

    </body>
  </html>


More Documentation
==================

More documentation can be found in the `Manual`_.


.. _jstc: https://pypi.python.org/pypi/jstc
.. _pyramid_beaker: https://pypi.python.org/pypi/pyramid_beaker
.. _Mako: http://www.makotemplates.org/
.. _jQuery: http://jquery.com/

.. TODO .. move the manual to pythonhosted.org...

.. _Manual: https://github.com/canaryhealth/pyramid_jitt/blob/master/pyramid_jitt/doc/manual.py
