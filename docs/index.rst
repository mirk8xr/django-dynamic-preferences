.. django-dynamic-preferences-plus documentation master file, created by
   sphinx-quickstart on Sat Jun 28 13:23:43 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django-dynamic-preferences-plus documentation
=============================================

What is dynamic-preferences-plus ?
**********************************

Dynamic-preferences-plus is a Django app, BSD-licensed, designed to manage your project settings. While most of the time,
a `settings.py` file is sufficient, there are some situations where you need something more flexible,
such as per-user settings and per-site settings.

For per-user settings, you could actually store them in `UserProfile`. However, it means that every time you want to add a new setting, you need to add a new column to the `UserProfile` DB table. Not very efficient.

Dynamic-preferences-plus allow you to register settings (a.k.a. preferences) in a declarative way, for users,
sites and your whole project. Preferences values are serialized before storage in database,
and automatically deserialized when you want to access them.

With dynamic-preferences-plus, you can update settings on the fly, through django's admin or custom forms, without restarting your application.

The project has been tested under Python 2.7 and Django 1.6.

If you're still interessed, head over :doc:`quickstart`.


Contents:

.. toctree::
   :maxdepth: 2

   quickstart
   preferences
   models
   registries
   commands

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

