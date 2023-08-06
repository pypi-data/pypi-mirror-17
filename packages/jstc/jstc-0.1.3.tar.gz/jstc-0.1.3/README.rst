============================
JavaScript Template Compiler
============================

The `jstc` Python package compiles and packages JavaScript templates
for delivery to browsers for client-side evaluation.

Currently, only `handlebars`_ and `mustache`_ template formats are
supported natively, however this is easily extended via jstc's plugin
mechanism.


Project
=======

* Homepage: https://github.com/canaryhealth/jstc
* Bugs: https://github.com/canaryhealth/jstc/issues


Installation
============

.. code:: bash

  # install jstc
  $ pip install jstc

Optionally, the handlebars pre-compiler can be installed to
pre-compile JavaScript templates for faster client-side rendering:

.. code:: bash

  # OPTIONAL: install handlebars pre-compiler
  $ npm install handlebars
  $ export PATH="`pwd`/node_modules/.bin:$PATH"


Usage
=====

Given that the following files exist in the Python package `myapp`:

File ``static/templates/common/hello.hbs``::

  Hello, {{name}}!


File ``static/templates/common/inputs.hbs``::

  ##! text

    <input type="text" name="{{name}}" value="{{value}}"/>

  ##! checkbox

    <input type="checkbox" name="{{name}}" value="1" {{#value}}checked="checked"{{/value}}/>


Then, the Python code (`inline` and `precompile` attributes used for
output simplicity):

.. code:: python

  import jstc
  jstc.render(
    'myapp:static/templates/common/**.hbs', 'static/templates',
    inline=True, precompile=False)


Outputs the HTML (whitespace and newlines added for clarity):

.. code:: html

  <div id="Templates" style="display:none;height:0;opacity:0;visibility:hidden;width:0;">

    <script type="text/x-handlebars" data-name="common/hello">
      Hello, {{name}}!
    </script>

    <script type="text/x-handlebars" data-name="common/inputs/text">
      <input type="text" name="{{name}}" value="{{value}}"/>
    </script>

    <script type="text/x-handlebars" data-name="common/inputs/checkbox">
      <input type="checkbox" name="{{name}}" value="1" {{#if value}}checked="checked"{{/if}}/>
    </script>

  </div>


Some Assumptions
================

The `jstc` package makes the following assumptions that cannot be
easily changed:

* Template names use a ``/`` hierarchical delimiter, e.g.
  ``components/widgets/textform`` would be a typical template name.

* Templates are named by their containing filenames with any extension
  removed, e.g. the template in ``"path/to/foo.hbs"`` will be named
  ``"path/to/foo"``.


Adding Template Formats
=======================

Let us assume that you want to add support for a new templating
engine, with a mime-type of ``text/x-easytpl``, file extension
``.et``, without pre-compilation support, and all within the Python
package ``myapp``.

Create module ``myapp/easytpl.py``:

.. code:: python

  import jstc
  import asset

  @asset.plugin('jstc.engines.plugins', 'text/x-easytpl')
  class EasyTemplateEngine(jstc.engines.base.Engine):
    mimetype    = 'text/x-handlebars'
    extensions  = ('.et',)
    precompile  = jstc.PrecompilerUnavailable


And then in your myapp's ``setup.py``, add the following parameter
to your `setup` call:

.. code:: python

  setup(
    ...
    entry_points = {
      'jstc.engines.plugins' : [
        'text/x-easytpl = myapp.easytpl:EasyTemplateEngine'
      ]
    }
  )


Et voilà, soufflé!

If you also want to support pre-compilation (i.e. server-side template
tokenization for faster client-side runtime evaluation), then take a
look at the `handlebars implementation
<https://github.com/canaryhealth/jstc/blob/master/jstc/engines/handlebars.py>`_.


.. _handlebars: http://handlebarsjs.com/
.. _mustache: http://mustache.github.io/
