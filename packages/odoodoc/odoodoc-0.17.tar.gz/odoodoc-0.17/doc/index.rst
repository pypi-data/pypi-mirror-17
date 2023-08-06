OdooDoc documentation
=====================

Installation
------------

This extension requires the following packages:

- Sphinx >= 1.2
- erppeek
- path.py

Use ``pip`` to install this extension straight from the Python Package Index::

   pip install odoodoc


Configuration
-------------

In order to use odoodoc you should add it to the list of extensions in conf.py::

   extensions = ['sphinxcontrib.odoodoc']

Usage
-----

OdooDoc adds the following set of directives to be used in the docs:

Field
~~~~~

You can refer to any field with the following directive:

::

   .. field:: model/field

which will print the given field name inside an *span* with the class
*odoodocfield*. You can change this default class with the configuration option
*odoodoc_fieldclass*.

Optionally the ``:help:`` flag can be added. See the following example:

::

   .. field:: res.partner/street
      :help:

It will print the help text of field despite of the field name (if the field
doesn't have help text it will print a message advertising it.

It also have the optional option ``:class: CLASSLIST``.

Menu
~~~~

You can refer to any menu entry with the **menu** directive.

::

   .. menu:: module/menu_XML_ID

The following code shows the menu name:

::

   .. menu:: account/periodical_processing_journal_entries_validation

which will output *Administration / Draft Entries*.

Like field directive, it will output the text inside an *span* tag with the
class *odoodocmenu*. This default class could be changed with the configuration
option *odoodoc_menuclass*. And if you want to add another classes to an specific
entry you could use the ``:class: CLASSLIST`` option.


Inline usage
~~~~~~~~~~~~

Inline usage is also available either using Sphinx's replace mechanism. As it
uses the directive it has all options and the same behaviour than directives:

::

   This is a reference to field |partner_street|.

   .. |partner_street| field:: res.partner/street

or one provided by odoodoc, which is shorter (but it doesn't put the text inside
and *span* tag and it doesn't support any option):

::

   This is a reference to a field @field:res.partner/street@.

In this shorter syntax, options are added at the end, separated by colons. For example::

   @field:res.partner/street:help@
   @menuaccount/periodical_processing_journal_entries_validation:nameonly@


FA Icon
~~~~~~~

You can insert any FontAwesome Icon using the **faicon** role.

::

   :faicon:`envelope`

This role simply inserts the following HTML (only for html writers)

.. code:: html

   <i class="fa fa-{}" aria-hidden="true"></i>

where {} is the content of the role.

