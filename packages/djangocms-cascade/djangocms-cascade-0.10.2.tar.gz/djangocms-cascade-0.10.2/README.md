djangocms-cascade
==================================================================================================================================================

[![Build Status](https://travis-ci.org/jrief/djangocms-cascade.png?branch=master)](https://travis-ci.org/jrief/djangocms-cascade)
[![Python versions](https://img.shields.io/pypi/pyversions/djangocms-cascade.svg)](https://pypi.python.org/pypi/djangocms-cascade)
[![Software license](https://img.shields.io/pypi/l/djangocms-cascade.svg)](https://github.com/jrief/djangocms-cascade/blob/master/LICENSE-MIT)
[![Gitter chat room](https://badges.gitter.im/jrief/djangocms-cascade.svg)](https://gitter.im/awesto/djangocms-cascade)
 [![Latest version on PyPI](https://img.shields.io/pypi/v/djangocms-cascade.svg)](https://pypi.python.org/pypi/djangocms-cascade)

**DjangoCMS-Cascade** is the Swiss army knife for working with Django CMS plugins.

Documentation
-------------

Find detailed documentation on [ReadTheDocs](http://djangocms-cascade.readthedocs.io/en/latest/).

Please see the [Release Notes](http://djangocms-cascade.readthedocs.io/en/latest/changelog.html)
before upgrading from an older version.

Currently **DjangoCMS-Cascade** does not work with **djangocms-text-ckeditor** >= 3.1. Please stay with
version 3.0.1 until this issue hase been fixed.


Why Use DjangoCMS-Cascade?
--------------------------

> Add DOM elements to a Django-CMS placeholder

**DjangoCMS-Cascade** is a collection of plugins for DjangoCMS >= 3.3 to add various HTML elements
to any CMS [placeholder](http://docs.django-cms.org/en/develop/getting_started/tutorial.html#creating-templates)
in a hierarchical tree.

It allows web editors to layout their pages, without having to edit Django templates. In most cases,
one template with one single placeholder is enough. The editor then can subdivide that placeholder
into rows and columns, and add additional elements such as buttons, rulers, and much more.

Currently about a dozen components from **Bootstrap-3.x** are available, but **Cascade** makes it
very easy to add additional components, often with less than 20 lines of Python code and without
any database migrations.

Since all plugins share the same database table, it is very easy to build inheritance trees. For
instance, Cascade's own ``LinkPlugin`` inherits from a ``LinkPluginBase``, which also is the parent
of the ``ImagePlugin`` and the ``ButtonPlugin``. This helps to share the common functionality
required for linking.


### It's pluggable

**DjangoCMS-Cascade** is very modular, keeping its CMS modules in functional groups. These groups
have to be activated independently in your ``settings.py``. It also is possible to activate only
certain Plugins out of a group. One such group is ``cmsplugin_cascade.bootstrap3``, but it could be
replaced by a future **Bootstrap-4**, the **Foundation**, **YUI** or whatever other CSS framework
you prefer.


### Configurable individually

Each Cascade Plugin can be styled individually. The site-administrator can specify which CSS styles
and CSS classes can be added to each plugin. Then the page-editor can pick one of the allowed styles
to adopt his elements accordingly.


### Reuse your data

Each Cascade Plugin can be configured by the site-administrator to share some or all of its data
fields. This for instance is handy, to keep references onto external URLs in a central place. Or is
can be used to resize all images sharing a cetrain property in one go.


### Segment the DOM

It is even possible to group plugins into seperate evaluation contexts. This for instance is used to
render different Plugins, depending on whether a user is authenticated or anonymous.


### Responsive Images

In modern web development, images must adopt to the column width in which they are rendered.
Therefore the ``<img ...>`` tag, in addition to the well known ``src`` attribute, also accepts
additional ``srcset``'s, one for each media query. **DjangoCMS-Cascade** calculates the required
widths for each image, depending on the current column layout considering all media breakpoints.


Features
--------

* Use the scaffolding technique from the preferred CSS framework to subdivide a placeholder into a
  [grid system](http://getbootstrap.com/css/#grid).
* Make full usage of responsive techniques, by allowing
  [stacked to horizontal](http://getbootstrap.com/css/#grid-example-basic) classes per element.
* Use styled [buttons](http://getbootstrap.com/css/#buttons) to add links.
* Wrap special content into a [Jumbotron](http://getbootstrap.com/components/#jumbotron) or a
  [Carousel](http://getbootstrap.com/javascript/#carousel).
* Add ``<img>`` and ``<picture>`` elements in a responsive way, so that more than one image URL
  point onto the resized sources, one for each viewport using the ``srcset`` tags or the
  ``<source>`` elements.
* Use segmentation to conditionally render parts of the DOM.
* It is very easy to integrate additional elements from the preferred CSS framework. For instance,
  implementing the Bootstrap Carousel, required only 50 lines of Python code and two simple Django
  templates.
* Since all the data is stored in JSON, no database migration is required if a field is added,
  modified or removed from the plugin.
* Currently **Bootstrap-3.x** is supported, but other CSS frameworks can be easily added in a
  pluggable manner.
* It follows the "batteries included" philosophy, but still remains very modular.

In addition to easily implement any kind of plugin, **DjangoCMS-Cascade** makes it possible to add
reusable helpers. Such a helper enriches a plugin with an additional, configurable functionality:

* By making some of the plugin fields sharable, one can reuse these values for other plugins of the
  same kind. This for instance is handy for the image and picture plugin, so that images always are
  resized to predefined values.
* By allowing extra fields, one can add an optional ``id`` tag, CSS classes and inline styles. This
  is configurable on a plugin and site base.
* It is possible to customize the rendering templates shipped with the plugins.
* Since all data is JSON, you can dump the content of one placeholder and insert it into another one,
  even on a foreign site. This for instance is useful to transfer pages from the staging site to production.


Help needed
-----------

If you like this project, please invest some time and test it with Django-1.8/1.9 and Python-3.4.

If you are a native English speaker, please check the documentation for spelling mistakes and
grammar since English not my mother tongue.
