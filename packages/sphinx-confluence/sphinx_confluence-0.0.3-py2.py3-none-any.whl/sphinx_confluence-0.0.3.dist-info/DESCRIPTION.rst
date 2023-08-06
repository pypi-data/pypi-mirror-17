Sphinx Confluence Plugin
========================

|Build Status|

Sphinx extension for making the documentation compatible with the
`Confluence Storage
Format <https://confluence.atlassian.com/display/DOC/Confluence+Storage+Format>`__.

Features:

-  base HTML elements
-  images (image, figure)
-  code blocks (::) and includes (literalinclude)
-  referencing downloadable files (:download:)
-  the TOC tree (.. toctree::)
-  internal links (:ref: ``<label>``; .. \_)
-  Inline and table Jira Issues
-  Reference for Confluence User
-  Info, Tip, Note, and Warning Macros

Why?
----

This extension is written as part of our Documentation Toolkit which we
use in our job daily. The main idea of toolkit is to make a process of
creating and updating documentation able to be automated

Other parts of our toolkit is:

-  `py2swagger <https://github.com/Arello-Mobile/py2swagger>`__
-  `swagger2rst <https://github.com/Arello-Mobile/swagger2rst>`__
-  `sphinx-confluence <https://github.com/Arello-Mobile/sphinx-confluence>`__
-  `confluence-publisher <https://github.com/Arello-Mobile/confluence-publisher>`__

Install
=======

Install Sphinx Confluence Plugin from
`PyPI <https://pypi.python.org/pypi/sphinx-confluence>`__ with

::

    $ pip install sphinx-confluence

How use it
----------

First of all, after installation, you must enable this plugin in your
`build configuration
file <http://www.sphinx-doc.org/en/stable/config.html#confval-extensions>`__
``conf.py`` by adding ``sphinx_confluence`` into ``extensions`` list.
This should looks like a:

::

    ...
    extensions = ['sphinx_confluence']
    ...

Then you can build you documentation into ``html`` or ``json`` formats,
either by using `sphinx build
command <http://www.sphinx-doc.org/en/stable/tutorial.html#running-the-build>`__
or if you uses ``sphinx-quickstart`` script by following commands: -
``make html`` - ``make singlehtml`` - ``make json``

After that, the results must be in Confluence Storage Format. You can
use
`confluence-publisher <https://github.com/Arello-Mobile/confluence-publisher>`__
for publish them to your Confluence.

Additional Markup Constructs
----------------------------

Sphinx Confluence Plugin adds few new directives to standard reST
markup.

Jira Issues
~~~~~~~~~~~

**Inline**

.. code:: rst

    Lorem ipsum dolor sit amet, :jira_issue:`PROJECT-123` consectetur adipiscing elit

**Table View**

*Markup:*

.. code:: rst

    .. jira_issues:: <JQL query>
       :anonymous: 'true'|'false' (default: 'false')
       :server_id: 'string' (default: '')
       :baseurl: 'string' (default: '')
       :columns: A list of JIRA column names, separated by semi-colons (;)
       :count: 'true'|'false' (default: 'false')
       :height: int (default: 480)
       :title: 'string' (default: '')
       :render_mode: 'static'|'dynamic' (default: 'static')
       :url: 'string' (default: '')
       :width: '{x}px' | '{x}%' (default: '100%')
       :maximum_issues: int (default: 20)

*Example:*

.. code:: rst

    .. jira_issues:: project = PROJ AND issuetype = Epic AND resolution = Unresolved
       :title: Unresolved project epics
       :columns: type;key;summary;status;created;
       :width: 80%

Jira Users
~~~~~~~~~~

.. code:: rst

    Lorem ipsum dolor sit amet, :jira_user:`username` consectetur adipiscing elit

.. |Build Status| image:: https://travis-ci.org/Arello-Mobile/sphinx-confluence.svg?branch=master
   :target: https://travis-ci.org/Arello-Mobile/sphinx-confluence


