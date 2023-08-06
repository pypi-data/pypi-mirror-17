======
TODO's
======


* Figure out the "more correct" way of providing the
  `request.registry.jitt` service...

* Auto-detect if the jitt caching regions have been configured, and if
  not, issue warning and disable caching

* Add controller support for:

  - /jitt/admin/inline
  - /jitt/admin/public | deferred
  - /jitt/admin/private | protected
  - /jitt/admin/jit/{PATH}

* Add support for template attributes:

  - jit | lazyload
