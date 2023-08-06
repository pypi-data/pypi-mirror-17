======
TODO's
======


* Figure out the "more correct" way of providing the
  `request.registry.jitt` service...

* Auto-detect if the jitt caching regions have been configured, and if
  not, issue warning and disable caching

* Add awareness that a set of template names should default to
  inlined, eg:

    DEFAULT_AUTOINLINE         = ('loading', 'application', 'error')

* Add support for template attributes:

  - jit | lazyload
