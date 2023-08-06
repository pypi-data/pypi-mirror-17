=====================
web.dispatch.resource
=====================

    © 2009-2016 Alice Bevan-McGregor and contributors.

..

    https://github.com/marrow/web.dispatch.resource

..

    |latestversion| |ghtag| |masterstatus| |mastercover| |masterreq| |ghwatch| |ghstar|



Introduction
============

Dispatch is the process of taking some starting point and a path, then resolving the object that path refers to. This
process is common to almost every web application framework (transforming URLs into controllers), RPC system, and even
filesystem shell. Other terms for this process include: "traversal", "routing", or "lookup".

Resource dispatch utilizes the HTTP verb (provided as the ``HTTP_METHOD`` WSGI environment variable) to determine which
method to call.

This package speaks a standardized `dispatch protocol <https://github.com/marrow/WebCore/wiki/Dispatch-Protocol>`__
and is not entirely intended for direct use by most developers. The target audience is instead the authors of
frameworks that may require such modular dispatch for use by their own users.


Installation
============

Installing ``web.dispatch.resource`` is easy, just execute the following in a terminal::

    pip install web.dispatch.resource

**Note:** We *strongly* recommend always using a container, virtualization, or sandboxing environment of some kind when
developing using Python; installing things system-wide is yucky (for a variety of reasons) nine times out of ten.  We
prefer light-weight `virtualenv <https://virtualenv.pypa.io/en/latest/virtualenv.html>`__, others prefer solutions as
robust as `Vagrant <http://www.vagrantup.com>`__.

If you add ``web.dispatch.resource`` to the ``install_requires`` argument of the call to ``setup()`` in your
application's ``setup.py`` file, this dispatcher will be automatically installed and made available when your own
application or library is installed.  We recommend using "less than" version numbers to ensure there are no
unintentional side-effects when updating.  Use ``web.dispatch.resource<2.1`` to get all bugfixes for the current
release, and ``web.dispatch.resource<3.0`` to get bugfixes and feature updates while ensuring that large breaking
changes are not installed.


Development Version
-------------------

    |developstatus| |developcover| |ghsince| |issuecount| |ghfork|

Development takes place on `GitHub <https://github.com/>`__ in the 
`web.dispatch.resource <https://github.com/marrow/web.dispatch.resource/>`__ project.  Issue tracking, documentation,
and downloads are provided there.

Installing the current development version requires `Git <http://git-scm.com/>`_, a distributed source code management
system.  If you have Git you can run the following to download and *link* the development version into your Python
runtime::

    git clone https://github.com/marrow/web.dispatch.resource.git
    pip install -e web.dispatch.resource

You can then upgrade to the latest version at any time::

    cd web.dispatch.resource
    git pull
    pip install -U -e .

If you would like to make changes and contribute them back to the project, fork the GitHub project, make your changes,
and submit a pull request.  This process is beyond the scope of this documentation; for more information see
`GitHub's documentation <http://help.github.com/>`_.


Usage
=====

This section is split to cover framework authors who will need to integrate the overall protocol into their systems,
and the object interactions this form of dispatch provides for end users.


Dispatchable Objects
--------------------

This form of dispatch relies on having an object whose attributes, named after HTTP verbs, are callable. Typically
classes with methods are used for this purpose. A basic example, using the ``web.dispatch.resource:Resource`` helper
class, would be::

    class Potato(Resource):
        def get(self):
            return "This is a marvellous potato."


This represents a resource (thus the name) with two different endpoints based on the HTTP verb in the request. Fairly
basic so far. To define a collection of resources, however, things get a little more complex::

    class Field(Collection):
        __resource__ = Potato
        
        potatoes = 10
        
        def get(self):
            return str(self.potatoes) + " potatoes in the field."
        
        def post(self):
            Field.potatoes += 1
            return "There are now " + str(Field.potatoes) + " potatoes in the field."
        
        def delete(self):
            Field.potatoes = 0
            return "You monster."
        
        def __getitem__(self, index):
            try:
                index = int(index)
            except ValueError:
                raise KeyError()
            
            if index <= 0 or index > self.potatoes:
                raise KeyError()
            
            return index

This defines a resource (since colections are also resources) with a few standard operations on it, plus this strange
double underscore method. This is a standard Python feature that lets you define that instances of your class can be
accessed using mapping subscripts, like a dictionary. This is how resource dispatch looks up individual items out of
collections.

If a KeyError is raised in ``__getitem__``, then that identifier is assumed to not exist.

The result of this lookup (using the next path element being dispatched against) is passed positionally to the
constructor of the class pointed to by the ``__resource__`` attribute of the ``Collection`` subclass, as is a
reference to the collection that spawned it.

We can now update our initial example resource to behave as part of a collection::

    class Potato(Resource):
        def get(self):
            return "One of " + str(self._collection.potatoes) + " beautiful potatoes."
        
        def delete(self):
            self._collection.potatoes -= 1
            return "You monster."

The text result of a ``GET`` request to ``/`` will be ``10 potatoes in the field.``  You can probably infer the
remaining behaviour.


Further Descent
~~~~~~~~~~~~~~~

Custom verbs may be defined as additional methods. Any method whose name is not prefixed with an underscore is treated
as an HTTP verb. Lastly, if there are remaining path elements, and the next matches an attribute whose value is a
class, then that class will be instantiated and yielded as the next step of dispatch.


Framework Authors
-----------------

To get started using resource dispatch to route requests in your web application, you're going to need to instantiate
the dispatcher::

    from web.dispatch.resource import ResourceDispatch
    
    dispatch = ResourceDispatch()  # There is currently no configuration.

Once you have that, you'll need a WSGI environment in some form of attribute access object used as the context. Our
examples here will use WebOb to provide a mock environment for us::

    from webob import Request, Response
    req = Request.objects.blank('/', method="delete")
    context = Context(environ=req.environ, request=req, response=Response())

Now that we have a prepared dispatcher, and prepared context, we'll need to prepare the path according to the
protocol::

    path = req.path_info.split('/')  # Initial path from the request's PATH_INFO.
    path = path[1:]  # Skip singular leading slashes; see the API specification.
    path = deque(path)  # Provide the path as a deque instance, allowing popleft.

The above doesn't need to be split apart exaclty like that, but you get the idea of the processing steps that need to
be completed prior to calling the dispatcher. The above might happen only once for the entire duration of a request
within a web framework, for example.

We can now call the dispatcher and iterate dispatch events::

    for segment, handler, endpoint, *meta in dispatch(context, some_object, path):
        print(segment, handler, endpoint)  # Do something with this information.

When a context is provided, it is passed as the first argument to any instantiated classes. After completing iteration,
check the final ``endpoint``.  If it is ``True`` then the path was successfully mapped to the object referenced by the
``handler`` variable, otherwise it represents the deepest object that was able to be found.

You can always just skip straight to the answer if you so chooose::

    segment, handler, endpoint, *meta = list(dispatch(context, some_object, path))[-1]

However, providing some mechanism for callbacks or notifications of dispatch is often far more generally useful

**Note:** It is entirely permissable or dispatchers to return ``None`` as a processed path segment. Resource dispatch
will, under most circumstances not involving attributes who are classes, will use ``None`` in this way.

Python 2 & 3 Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~

The dispatch protocol is designed to be extendable in the future by using ``namedtuple`` subclasses, however this has
an impact on usage as you may have noticed the ``*meta`` in there. This syntax, introduced in Python 3, will gather any
extraneous tuple elements into a separate list. If you actually care about the metadata, do not unpack the tuple this
way. Instead::

    for meta in dispatch(None, some_object, path):
        segment, handler, endpoint = step[:3]  # Unpack, but preserve.
        print(segment, handler, endpoint, meta)  # Do something with this information.

This document is written from the perspective of modern Python 3, and throwing away the metadata within the ``for``
statement itself provides more compact examples. The above method of unpacking the first three values is the truly
portable way to do this across versions.


Version History
===============

Version 2.0
-----------

* Extract of the resource dispatch mechanism from WebCore.
* Updated to utilize the standardized dispatch protocol.

Version 1.x
-----------

* Process fully integrated in the WebCore web framework as the "RESTful dialect".


License
=======

web.dispatch.resource has been released under the MIT Open Source license.

The MIT License
---------------

Copyright © 2009-2016 Alice Bevan-McGregor and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


.. |ghwatch| image:: https://img.shields.io/github/watchers/marrow/web.dispatch.resource.svg?style=social&label=Watch
    :target: https://github.com/marrow/web.dispatch.resource/subscription
    :alt: Subscribe to project activity on Github.

.. |ghstar| image:: https://img.shields.io/github/stars/marrow/web.dispatch.resource.svg?style=social&label=Star
    :target: https://github.com/marrow/web.dispatch.obresourceject/subscription
    :alt: Star this project on Github.

.. |ghfork| image:: https://img.shields.io/github/forks/marrow/web.dispatch.resource.svg?style=social&label=Fork
    :target: https://github.com/marrow/web.dispatch.resource/fork
    :alt: Fork this project on Github.

.. |masterstatus| image:: http://img.shields.io/travis/marrow/web.dispatch.resource/master.svg?style=flat
    :target: https://travis-ci.org/marrow/web.dispatch.resource/branches
    :alt: Release build status.

.. |mastercover| image:: http://img.shields.io/codecov/c/github/marrow/web.dispatch.resource/master.svg?style=flat
    :target: https://codecov.io/github/marrow/web.dispatch.resource?branch=master
    :alt: Release test coverage.

.. |masterreq| image:: https://img.shields.io/requires/github/marrow/web.dispatch.resource.svg
    :target: https://requires.io/github/marrow/web.dispatch.resource/requirements/?branch=master
    :alt: Status of release dependencies.

.. |developstatus| image:: http://img.shields.io/travis/marrow/web.dispatch.resource/develop.svg?style=flat
    :target: https://travis-ci.org/marrow/web.dispatch.resource/branches
    :alt: Development build status.

.. |developcover| image:: http://img.shields.io/codecov/c/github/marrow/web.dispatch.resource/develop.svg?style=flat
    :target: https://codecov.io/github/marrow/web.dispatch.resource?branch=develop
    :alt: Development test coverage.

.. |developreq| image:: https://img.shields.io/requires/github/marrow/web.dispatch.resource.svg
    :target: https://requires.io/github/marrow/web.dispatch.resource/requirements/?branch=develop
    :alt: Status of development dependencies.

.. |issuecount| image:: http://img.shields.io/github/issues-raw/marrow/web.dispatch.resource.svg?style=flat
    :target: https://github.com/marrow/web.dispatch.resource/issues
    :alt: Github Issues

.. |ghsince| image:: https://img.shields.io/github/commits-since/marrow/web.dispatch.resource/2.0.0.svg
    :target: https://github.com/marrow/web.dispatch.resource/commits/develop
    :alt: Changes since last release.

.. |ghtag| image:: https://img.shields.io/github/tag/marrow/web.dispatch.resource.svg
    :target: https://github.com/marrow/web.dispatch.resource/tree/2.0.0
    :alt: Latest Github tagged release.

.. |latestversion| image:: http://img.shields.io/pypi/v/web.dispatch.resource.svg?style=flat
    :target: https://pypi.python.org/pypi/web.dispatch.resource
    :alt: Latest released version.

.. |cake| image:: http://img.shields.io/badge/cake-lie-1b87fb.svg?style=flat
