Changelog
=========

2.2.0 (2023-01-16)
------------------

- Add support for Python 3.7, 3.8, 3.9, 3.10, and 3.11.

- Drop suppport for Python 2.7, 3.4, 3.5 and 3.6.

- Add Github Actions workflow running unit tests / coverage for PRs.

2.1 (2016-06-03)
----------------

- Add support for Python 3.4, 3.5 and PyPy3.

- Drop support for Python 2.6 and 3.2.

- Add support for testing under Travis.

2.0 (2013-06-26)
----------------

- Avoid swallowing the original exception while aborting the transaction
  in middleware.  See PR #3.

2.0b1 (2013-04-05)
------------------

- Middleware is now a generator, to deal appropriately with application
  iterators which are themselves not lists.

- Convert use of deprecated failIf/failUnless to assertFalse/assertTrue.

- Add support for testing under supported Pythons using Tox.

- Add explicit support for Python 3.2 ad 3.3.

- Drop support for Python 2.4, 2.5.

1.0 (2012-03-24)
----------------

- Run OOTB under Python 2.4 / 2.5 (pin 'transaction' dependency to
  a supported version when running under 2.4 / 2.5).

1.0b2 (2011-07-18)
------------------

- A new header ``X-Tm`` is now honored by the ``default_commit_veto`` commit
  veto hook.  If this header exists in the headerlist, its value must be a
  string.  If its value is ``commit``, the transaction will be committed
  regardless of the status code or the value of ``X-Tm-Abort``.  If the value
  of the ``X-Tm`` header is ``abort`` (or any other string value except
  ``commit``), the transaction will be aborted regardless of the status code
  or the value of ``X-Tm-Abort``.

- Use of the ``X-Tm-Abort`` header is now deprecated.  Instead use the
  ``X-Tm`` header with a value of ``abort`` instead.

- Add API docs section.

1.0b1 (2011-01-19)
------------------

- Added ``repoze.tm.default_commit_veto`` commit veto hook.  This commit veto
  hook aborts for 4XX and 5XX response codes, or if there's a header named
  ``X-Tm-Abort`` in the headerlist and allows a commit otherwise.

- Documented commit veto hook.

1.0a5 (2009-09-07)
------------------

- Don't commit after aborting if the transaction was doomed or if the
  commit veto aborted.

- Don't use "real" transaction module in tests.

- 100% test coverage.

1.0a4 (2009-01-06)
------------------

- RESTify CHANGES, move docs in README.txt into Sphinx.

- Remove ``setup.cfg`` (all dependencies available via PyPI).

- Synchronization point with ``repoze.tm`` (0.9).

1.0a3 (2008-08-03)
------------------

Allow ``commit_veto`` hook to be specified within Paste config, ala::

   [filter:tm]
   use = repoze.tm:make_tm
   commit_veto = some.package:myfunction

``myfunction`` should take three args: environ, status, headers and
should return True if the txn should be aborted, False if it should be
committed.

Initial PyPI release.

1.0a2 (2008-07-15)
------------------

- Provide "commit_veto" hook point (contributed by Alberto Valverde).

- Point easy_install at http://dist.repoze.org/tm2/dev/simple via setup.cfg.
 
1.0a1 (2008-01-09)
------------------

- Fork point: we've created repoze.tm2, which is repoze.tm that has a
  dependency only on the 'transaction' package instead of all of ZODB.

- Better documentation for non-Zope usage in README.txt.

0.8 (2007-10-11)
----------------

- Relaxed requirement for ZODB 3.7.2, since we might need to use the
  package with other verions.  Note that the tests which depend on
  transaction having "doom" semantics don't work with 3.7.2, anyway.

0.7 (2007-09-25)
----------------

- Depend on PyPI release of ZODB 3.7.2.  Upgrade to this by doing
  bin/easy_install -U 'ZODB3 >= 3.7.1, < 3.8.0a' if necessary.

0.6 (2007-09-21)
----------------

 - after_end.register and after_end.unregister must now be passed a
   transaction object rather than a WSGI environment to avoid the
   possibility that the WSGI environment used by a child participating
   in transaction management won't be the same one used by the
   repoze.tm package.

 - repoze.tm now inserts a key into the WSGI environment
   (``repoze.tm.active``) if it's active in the WSGI pipeline.  An API
   function, repoze.tm:isActive can be called with a single argument,
   the WSGI environment, to check if the middleware is active.

0.5 (2007-09-18)
----------------

- Depend on rerolled ZODB 3.7.1 instead of zopelib.

- Add license and copyright, change trove classifiers.

0.4 (2007-09-17)
----------------

- Depend on zopelib rather than ZODB 3.8.0b3 distribution, because the
  ZODB distribution pulls in various packages (zope.interface and ZEO
  most notably) that are incompatible with stock Zope 2.10.4 apps and
  older sandboxes.  We'll need to revisit this.

0.3 (2007-09-14)
----------------

- Provide limited compatibility for older transaction package versions
  which don't support the 'transaction.isDoomed' API.

0.2 (2007-09-13)
----------------

- Provide after_end API for registering callbacks at transaction end.

0.1 (2007-09-10)
----------------

- Initial Release
