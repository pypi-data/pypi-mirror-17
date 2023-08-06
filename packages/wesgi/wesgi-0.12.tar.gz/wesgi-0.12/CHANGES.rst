CHANGES
=======

0.12 (2016-10-06)
----------------

Fixes
+++++

- fix dictionary changed size during iteration errors on Python 3

0.11 (2016-05-25)
----------------

Features
++++++++

- Configuration via paste, rescued from missing 0.9 release.

0.10 (2016-05-25)
----------------

Features
++++++++

- Python 3 support, drop Python 2.5 support.
- Request header forwarding by default.
- Turn relative links in <esi:include into absolute links before
  including.

0.8 (2011-07-07)
----------------

Features
++++++++

- A ``max_object_size`` option for ``wesgi.LRUCache`` to limit the maximum size
  of objects stored.

0.7 (2011-07-06)
----------------

Features
++++++++

- Major refactoring to use ``httplib2`` as the backend to get ESI includes. This
  brings along HTTP Caching.
- A memory based implementation of the LRU caching algoritm at ``wesgi.LRUCache``.
- Handle ESI comments.

Bugfixes
++++++++

- Fix bug where regular expression to find ``src:includes`` could take a long time.

0.5 (2011-07-04)
----------------

- Initial release.
