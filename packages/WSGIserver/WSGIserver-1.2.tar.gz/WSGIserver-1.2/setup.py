from setuptools import setup
from wsgiserver import __version__ as version

setup(name='WSGIserver',
      version=version,
      description='A high-speed, production ready, thread pooled, generic WSGI server with SSL support',
      author='Florent Gallaire',
      author_email='fgallaire@gmail.com',
      url='http://fgallaire.github.io/wsgiserver',
      license='GNU LGPLv3+',
      keywords='wsgi server',
      classifiers=[
          "Development Status :: 6 - Mature",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
          "Topic :: Internet :: WWW/HTTP :: WSGI",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.1",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
      ],
      py_modules=['wsgiserver'],
      )
