.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
experimental.nodtml
==============================================================================

Patch DocumentTemplate to not return any content.


Features
--------

DTML documents have been deprecated for several years, at least within
the Plone community.  So you should not use them.  But still Plone
ships with DTML documents.  And these may contain security issues,
especially for Cross Site Scripting (CSS).  So this package patches
the Document Templates to not return any content.


Options
-------

The package looks for a few environment variables.

``SHOW_ORIGINAL_DTML``
    When this is set, the original DTML value is printed in the zope instance log.

``DEBUG_DTML_VALUE``
    When this is set, the given value is return as content of the DTML.


Installation
------------

Install experimental.nodtml by adding it to your buildout::

    [buildout]
    ...
    eggs =
        experimental.nodtml

and then running ``bin/buildout``

No zcml is needed.


Contribute
----------

- Issue Tracker: https://github.com/collective/experimental.nodtml/issues
- Source Code: https://github.com/collective/experimental.nodtml


License
-------

The project is licensed under the GPLv2.
