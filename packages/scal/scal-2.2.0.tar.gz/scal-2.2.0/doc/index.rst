Welcome to `scal`'s documentation!
==================================

I use this program about once a year to print a one-page school-year
calendar. But it can be used to represent any calendar.

It is heavily inspired by the simple yet powerful Robert Krause's `calendar
<http://www.texample.net/tikz/examples/a-calender-for-doublesided-din-a4/>`_,
itself using the complex yet powerful Till Tantau's `TikZ
<http://www.ctan.org/pkg/pgf>`_ LaTeX package.

.. contents:: Table of Contents
   :depth: 1
   :local:

Examples
--------

- French school year:

  - 2022-2023:
    :download:`zone A <examples/fr_20222023_A.pdf>` (:download:`source <examples/fr_20222023_A.scl>`),
    :download:`zone B <examples/fr_20222023_B.pdf>` (:download:`source <examples/fr_20222023_B.scl>`),
    :download:`zone C <examples/fr_20222023_C.pdf>` (:download:`source <examples/fr_20222023_C.scl>`)

- Weekly planners:

  - 2022-2023:
    :download:`French <examples/weekly-fr-2223.pdf>` (:download:`source <examples/weekly-fr-2223.scl>`),
    :download:`English <examples/weekly-en-2223.pdf>` (:download:`source <examples/weekly-en-2223.scl>`)
  - 2023-2024:
    :download:`French <examples/weekly-fr-2324.pdf>` (:download:`source <examples/weekly-fr-2324.scl>`),
    :download:`English <examples/weekly-en-2324.pdf>` (:download:`source <examples/weekly-en-2324.scl>`)

  .. admonition:: How to print those planners?
     :class: dropdown

     #. `Impose <https://en.wikipedia.org/wiki/Imposition>`__ the file you just downloaded above. This can be done using tool `pdfimpose <https://pypi.org/p/pdfimpose>`__ with the following command line:

        .. code-block:: bash

           pdfimpose perfect --group 3 weekly-en-2324.pdf

        You get the files :
        :download:`French 2022-2023 <examples/weekly-fr-2223-impose.pdf>`,
        :download:`French 2023-2024 <examples/weekly-fr-2324-impose.pdf>`,
        :download:`English 2022-2023 <examples/weekly-en-2223-impose.pdf>`,
        :download:`English 2023-2024 <examples/weekly-en-2324-impose.pdf>`.

     #. Print them, two-sided, not reversed.
     #. Fold the sheets, that is:

        #. Take the stack of sheets in front of you, the title page being visible, not upside-down, in the bottom right corner of the sheet.
        #. Take the first three sheets of paper, and fold them (together, as if they were one single thick sheet):

           - first vertically: fold the top half of the sheets behind the bottom half;
           - then horizontally: fold the left half of the sheets behin the right half.

           You get a tiny, incomplete book (called a `signature <https://en.wikipedia.org/wiki/Section_(bookbinding)>`__), which cannot be opened yet because of folds. Set it aside.
        #. Repeat the previous step as many times as necessary to fold the whole stack of paper.

     #. Bind the several signatures you got, maybe add a cover.
     #. *Voilà!*

Download and install
--------------------

See the `main project page <http://git.framasoft.org/spalax/scal>`_ for
instructions, and `changelog
<https://git.framasoft.org/spalax/scal/blob/main/CHANGELOG.md>`_.

Usage
-----

Note that `scal` only produce the LuaLaTeX code corresponding to the calendar. To get the `pdf` calendar, save the code as a :file:`.tex` file, or pipe the output through ``lualatex``:

.. code-block:: bash

    scal FILE | lualatex

The list of built-in templates is returned by command:

.. code-block:: bash

   scal templates list

Here are the main command line options for `scal`.

.. argparse::
    :module: scal.__main__
    :func: argument_parser
    :prog: scal

Configuration file
------------------

The YAML UTF8-encoded file given in argument contains the information about the calendar.
Here is, for example, the file corresponding to a school year calendar.

.. literalinclude:: examples/fr_20172018_B.scl

An annotated configuration file (with default values and examples) is available for each template.
For instance, to get this configuration file for template `weekly.tex`, use:

.. code-block:: bash

   scal templates config weekly.tex

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
