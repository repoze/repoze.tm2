
import os
from setuptools import setup, find_packages
import sys

if sys.version_info < (2, 6):
    install_requires = ['transaction<1.2dev']
else:
    install_requires = ['transaction']

testing_extras = install_requires + ['nose', 'coverage']

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

setup(name='repoze.tm2',
      version='1.0',
      description='Zope-like transaction manager via WSGI middleware',
      long_description=README + "\n\n" + CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        ],
      keywords='web application server wsgi zope repoze',
      author="Agendaless Consulting",
      author_email="repoze-dev@lists.repoze.org",
      url="http://www.repoze.org",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['repoze'],
      zip_safe=False,
      install_requires=install_requires,
      tests_require=install_requires,
      test_suite = "repoze.tm.tests",
      entry_points="""
      [paste.filter_app_factory]
      tm = repoze.tm:make_tm
      """,
      extras_require = {
        'testing': testing_extras,
      }
)

