mezzanine\_pubsubhubbub\_pub
============================

|Build Status|

| Publisher support of pubsubhubbub for mezzanine's blog
| Inspired by `brutasse/django-push: PubSubHubbub support for
  Django <https://github.com/brutasse/django-push>`__, this package is
  created.

Requirements
------------

-  mezzanine
-  requests
-  mock (for test)

Installation
------------

.. code:: console

    pip install mezzanine_pubsubhubbub_pub

Usage
=====

add aplication to settings.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    INSTALLED_APPS = (
        "mezzanine_pubsubhubbub_pub",
        "mezzanine.boot",
        "mezzanine.conf",
        "mezzanine.generic",
    ......

add feed urlpatterns to urls.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from mezzanine_pubsubhubbub_pub import get_feed_url_patterns
    urlpatterns += get_feed_url_patterns()

add PUSH\_HUB to settings.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| PUSH\_HUB is hub server to be notified
| There can be multiple URL set in the Taple.
| Default : ``("https://pubsubhubbub.appspot.com/",)``
| This setting will not be editable via the admin.

add PUSH\_URL\_PROTOCOL to settings.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Set the protocol of the Feed URL to be notified .
| HTTP\_ONLY, a HTTPS\_ONLY, BOTH can be set ,
| BOTH is done the notification in the HTTP / HTTPS both the Feed URL.
| Default : ``HTTP_ONLY``
| This setting will be editable via the admin.

TODO
====

-  Support for the lower version

-  Flexible feed URL setting

-  Create batch jobs

.. |Build Status| image:: https://travis-ci.org/kemsakurai/mezzanine-pubsubhubbub-pub.svg?branch=master
   :target: https://travis-ci.org/kemsakurai/mezzanine-pubsubhubbub-pub
