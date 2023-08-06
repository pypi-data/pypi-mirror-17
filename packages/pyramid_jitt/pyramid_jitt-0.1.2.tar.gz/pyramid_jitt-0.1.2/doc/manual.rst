======================================
Pyramid Just-In-Time Templating Manual
======================================


Overview
========

Pyramid JITT helps Pyramid applications assemble, pre-compile,
package, cache, and access-control the delivery of templates to
clients. Typically, these are JavaScript-based templates (such as
Handlebars_ or Mustache_) that are used in rich internet applications
running in browsers.

In essence, Pyramid-JITT is just a wrapper around the `jstc`_
JavaScript template compiler that adds automation, segregation into
multiple and access-controlled delivery channels, and some basic
JavaScript routines to implement on-the-wire communication.

Conceptually, Pyramid JITT groups templates into **realms**, where
each realm is typically associated with a particular client-side
application.  For example, if the Pyramid application has a "user" and
an "admin" web page, with a different set of templates, then there
could be the corresponding "user" and "admin" JITT realms.

Within each realm, the templates are divided into
**channels**. Although in theory the number and names of channels is
undefined, the current the JITT system makes many assumptions around
the existence of the following channels:

* the ``inline`` channel: the set of templates delivered in the
  base HTML page;

* the ``deferred`` channel: the templates loaded asynchronously
  after the base HTML page is loaded;

* the ``protected`` channel: the templates loaded asynchronously
  after the user has been authenticated; and

* the ``jit`` channel: a rarely-used channel whereby each template
  is delivered asynchronously on-demand.

See the `Channels`_ section for details.


Channels
========

A "channel" is a grouping of the templates within a realm. In the
current Pyramid JITT system, the below defined channels exist and have
the specified delivery rules. In future releases, the naming and
restrictions of each channel may be extended and/or enhanced.


Channel ``inline``
------------------

This channel comprises the templates that are delivered along with,
i.e. they are inlined within, the base HTML page. As such, they are
the set that need to be present immediately at initial page load and
are not access-controlled, i.e. they are viewed as being publicly
accessible.


Channel ``deferred``
--------------------

This channel comprises the templates that are delivered
asynchronously to the base HTML page, immediately after the HTML has
been delivered to the client. This channel typically contains the
majority of templates required for the application, but not for the
initial rendering. It channel is not access-controlled.


Channel ``protected``
---------------------

This channel comprises the deferred templates that should not be
delivered to the public; they are loaded asynchronously after the
application authenticates the user.


Channel ``jit``
---------------

This is a special channel that, unlike the other channels, is not a
grouping of templates, but instead is the just-in-time delivery of a
single template. This channel requires deep integration with the
client-side templating engine and as a result is not very commonly
used.


Templates
=========

Pyramid JITT places very few requirements and/or restrictions on how
templates are organized, formatted, or structured. There are, however,
some conventions that exist that help in this regard. This section
details them.


Template Discovery
------------------

The ``{REALM}.assets`` configuration specifies the files that will be
used to find the templates. Easiest is to use a dedicated file
extension for client-side templates, e.g. ``.hbs`` for `Handlebars`_
templates; then, the asset specification ``mypackage:**.hbs`` will
find all the filenames that end with ``.hbs`` in the `mypackage`
Python package.


Name Transformation
-------------------

The ``{REALM}.roots`` configuration specifies how a filename should be
translated to a template name. By default, the roots uses an
"automagic" translation mechanism as follows: if the asset uses a
recursive wildcard glob pattern (i.e. ``/**``), then the portion that
matches the wildcard will be used as the template name. Otherwise, the
filename within the package, without the extension, is used.

For example, given the glob pattern ``mypackage:static/**.hbs``, then
the file ``mypackage:static/foo/bar.hbs`` will be given the template
name ``foo/bar``. On the other hand, if ``{REALM}.roots`` had been
specified as ``static/foo``, then the name would have been ``bar``.
The ``{REALM}.name_transform`` can be used if an alternate naming
scheme is needed.

Note that the special token ``__here__`` is removed from the template
name. For example, the filename ``foo/bar/__here__.hbs`` will be, by
default, transformed to the template name ``foo/bar``. This allows
sub-directories to contain a template named after the parent's
directory.


Comments
--------

Within each template file, any line that starts with the comment
sequence which by default is ``##`` will be stripped out before being
sent to the client. This allows templates to contain content that
will not be exposed to the public. Example:

.. code:: html

  <div>
    Hello, world!
    ## TODO: we should **really** customize this greeting
    ##       in the next release!!! ARGH!
  </div>


Multi-Template Files
--------------------

Each file can optionally contain a set of templates instead of just a
one-to-one mapping. Any file that starts with the multi-template
token, which defaults to ``##!``, will be split into multiple
templates. The file content will be split at every line that starts
with the multi-template token, and the rest of the line is used to
specify the template name and optionally any attributes. The final
template name is constructed by appending the name specified to the
file's evaluated template name, removing any ``__here__`` tokens
(similar to the normal filename-to-templatename translation).

For example, given the following file ``hello.hbs``:

.. code::

  ##! __here__

    <div>Hello, world!</div>

  ##! name

    <div>Hello, {{name}}!</div>

  ##! string; type: text/x-mustache; locale: en-us; protected

    Hello, {{name}}!


This file will be split into three templates named ``hello``,
``hello/name``, and ``hello/string``, with the last one overriding the
default *type* and *locale* attributes and setting the *protected*
flag.


Attributes
----------

Each template can specify, or override, a set of attributes using the
`Multi-Template Files`_ mechanism. Some of the attributes are used by
the `jstc`_ system, and some are used by Pyramid JITT. The following
are the attributes (see the `jstc`_ package for details) that are
commonly used:

* ``type``: the template engine type
* ``trim``: flag to control dedenting and stripping of template content
* ``precompile``: flag to control server-side pre-compile the template
* ``inline``: flag to control inclusion in the ``inline`` channel
* ``protected``: flag to control inclusion in the ``protected`` channel


Delivery
========

Almost all of the mechanisms used to deliver the template channels to
the client can be customized, but the default configuration expects
you to use the JITT loader.

The JITT loader is normally included in the initial construction of
the initial HTML base page. It then exposes a `.ready` JavaScript
function that is used to specify a callback that is invoked when the
``inline`` and ``deferred`` (if any) templates have been loaded. Here
is a `Mako`_ example of how to add the JITT loader to your "webapp"
HTML application and how to hook into it with a callback:

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


If you do not wish to use asynchronous loading, you can force inlining
with the following:

.. code:: mako

  ${request.registry.jitt.render('webapp', force_inline=True)|n}


Protected Templates
-------------------

The ``protected`` channel templates will not have been delivered when
the `.ready()` callback is called; instead, you must explicitly
request the delivery of the protected templates after authentication
has occurred. The following JavaScript can be used for that purpose:

.. code:: js

  $('#Templates').data('jitt').load('protected').then(function() {
    // do things that use the protected templates
  }, function(error) {
    alert('OOPS! Could not load the templates: ' + error.error);
  });


Deferred Endpoints
------------------

The Pyramid JITT implementation defers the loading of templates by
loading them asynchronously. In order for that to work, Pyramid JITT
exposes a set of URL endpoints that are, by default, mounted at
``/jitt/``. Specifically, all groups of templates are made available
at ``/jitt/{REALM}/{CHANNEL}``.

The presence and location of these endpoints can be customized via the
configuration options:

* ``{REALM}.mount-host``
* ``{REALM}.mount-path``


Non-jQuery Clients
------------------

The default Pyramid JITT framework expects `jQuery`_ to be pre-loaded
in the HTML page. If this is not the case and you wish to use an
alternative deferred-loading mechanism, the following configurations
can be used to customize the rendering:

* ``{REALM}.loader.always``
* ``{REALM}.deferred-html``
* ``{REALM}.deferred-js``


Configuration
=============

Pyramid JITT configurations are loaded from your application settings,
typically from the active ``.ini`` file.

Each configuration name is prefixed with ``jitt.``, optionally
followed by an ``@`` and the realm name that it applies to, then
followed by a specific parameter. If no realm name is specified, it is
applied to the ``default`` realm: all other realms inherit from the
default realm.

For example, the parameter ``jitt.compiler`` sets the "default"
realm's "compiler" value, and the parameter ``jitt.@foobar.compiler``
then overrides the "foobar" realm's "compiler" value. All parameters
can be defaulted and overriden on a per-realm basis in this manner.

The following parameters are supported:

* ``{REALM}.id`` : str, default: Templates

  Specifies the "id" attribute of the top-level HTML element that
  contains the JavaScript templates.

* ``{REALM}.style`` : yaml, default: (see documentation)

  Specifies the "style" attribute (as a YAML dictionary) of the
  top-level HTML element that contains the JavaScript templates.  The
  default sets a series of CSS values that intend to hide the element
  from display as much as possible. This includes such settings as
  `display` to "none", `visibility` to "hidden", and `opacity` to 0.

* ``{REALM}.compiler`` : asset-spec, default: "jstc:Compiler"

  Specifies the `jstc` compiler path that will be used to actually
  compile the JS templates.

* ``{REALM}.assets`` : asset-spec | list(asset-spec)

  Specifies a list of globre asset-spec's of which assets to include
  in the realm. For example, the following will recursively search for
  all files that end in ``.mustache`` in the ``static/common`` and
  ``static/webapp`` directories of the ``myapp`` package for the
  ``webapp`` realm:

  .. code:: ini

    jitt.@webapp.assets =
      myapp:static/common/**.mustache
      myapp:static/webapp/**.mustache


  See `{REALM}.roots` for details on how to map an asset name to a
  template name.

* ``{REALM}.roots`` : str | list(str)

  Specifies a list of prefixes to be chopped from an asset name to
  arrive at the template name that it contains. For example, if
  an asset's name is ``static/common/segment/filename.hbs`` and the
  respective root is ``static/common``, then the name will be
  interpreted as ``segment/filename``.

  See `{REALM}.name_transform` for greater control than simple
  prefix-chopping.

* ``{REALM}.cache-region`` : str, default: pyramid_jitt

  Sets the `beaker` cache region to use for this realm. To disable
  caching (bad idea!) set this to an empty string.

* ``{REALM}.asset_filter`` : asset-spec

  Sets the `jstc.render_assets` `asset_filter` parameter, see
  the `Callbacks`_ section for details.

* ``{REALM}.name_transform`` : asset-spec

  Sets the `jstc.render_assets` `name_transform` parameter, see
  the `Callbacks`_ section for details.

* ``{REALM}.template_transform`` : asset-spec

  Sets the `jstc.render_assets` `template_transform` parameter, see
  the `Callbacks`_ section for details.

* ``{REALM}.template_filter`` : asset-spec

  Sets the `jstc.render_assets` `template_filter` parameter, see the
  `Callbacks`_ section for details.

* ``{REALM}.script_wrapper`` : asset-spec

  Sets the `jstc.render_assets` `script_wrapper` parameter, see the
  `Callbacks`_ section for details.

* ``{REALM}.defaults.{ATTRIBUTE}`` : yaml

  Sets a default value for a template attribute that will be passed to
  the `defaults` parameter of the jstc.Compiler constructor. For
  example, to disable the default whitespace trimming and
  pre-compilation that jstc does, add:

  .. code:: ini

    jitt.defaults.trim       = false
    jitt.defaults.precompile = false


  See the `jstc`_ package for a full listing of supported template
  attributes.

* ``{REALM}.overrides.{ATTRIBUTE}`` : yaml

  Sets an override value for a template attribute that will be passed
  to the `overrides` parameter of the jstc.Compiler constructor. For
  example, to force all templates to be inlined and trimmed, but
  force "admin" templates to not be trimmed, add:

  .. code:: ini

    jitt.overrides.trim        = true
    jitt.overrides.inline      = true
    jitt.@admin.overrides.trim = true


  See the `jstc`_ package for a full listing of supported template
  attributes.

* ``{REALM}.mount-path`` : str, default: "/jitt"

  The root of the URL-accessible content generated by pyramid_jitt.
  To disable serving of this content, set the `mount-path` to null.
  Note that this is required for deferred and restricted content
  delivery.

* ``{REALM}.mount-host`` : str, default: null

  The fully-qualified scheme and hostname
  (e.g. ``"https://content.example.com"``) where the `mount-path` is
  accessible. Note that this is only necessary if jitt content is
  being served in a non-WSGI context, as otherwise the REQUEST_HOST
  environment variable is used.

* ``{REALM}.loader.always`` : bool, default: true

  Sets whether or not the JavaScript JIT loader is always inserted
  into the rendered output, or only when required (i.e. when there are
  no non-inlined templates, the JIT loader isn't technically
  necessary).


Callbacks
=========

The callbacks called by `pyramid_jitt` have the same parameters as
their respective `jstc` callbacks with the addition of two parameters,
`realm` and `channel`, which are prefixed as the first two positional
parameters.

.. IMPORTANT::

  Please note that the impact of the callbacks (asset_filter,
  name_transform, template_transform, template_filter) should be
  consistent for a given `cache-region` since the cache key will be
  dependent on ``cache-region + realm + channel`` only.


A More Involved Example
=======================

Here is a more complex configuration example, with multiple realms
with different caching rules, asset locations, etc:

.. code:: ini

  # pyramid_beaker caching configuration
  cache.type                    = memory
  cache.regions                 = jitt-webapp jitt-admin
  cache.jitt-webapp.expire      = 3600
  cache.jitt-admin.expire       = 300

  # pyramid_jitt "default" realm parameters
  jitt.style                    = {display: none}
  jitt.defaults.trim            = true
  jitt.defaults.precompile      = false
  jitt.overrides.inline         = true

  # pyramid_jitt "webapp" realm parameters
  jitt.@webapp.cache-region     = jitt-webapp
  jitt.@webapp.assets           =
    myapp:static/scripts/common/**.hbs
    myapp:static/scripts/webapp/**.hbs
  jitt.@webapp.roots            =
    static/scripts
    static/scripts/webapp

  # pyramid_jitt "admin" realm parameters
  jitt.@admin.cache-region      = jitt-admin
  jitt.@admin.assets            =
    myapp:static/scripts/common/**.hbs
    myapp:static/scripts/admin/**.hbs
  jitt.@admin.roots             =
    static/scripts
    static/scripts/admin



.. _jstc: https://pypi.python.org/pypi/jstc
.. _pyramid_beaker: https://pypi.python.org/pypi/pyramid_beaker
.. _Mako: http://www.makotemplates.org/
.. _jQuery: http://jquery.com/
