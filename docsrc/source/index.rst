.. pypi-sphinx-quickstart documentation master file, created by
   pypi-sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python Extends LaTeX documentation!
***********************************************

To get started, look here.

.. toctree::

   tutorial


An overview
===========

.. pyexlatex:: test_name

   section = pl.Section(["woo"], title="First Section")
   pl.Document(section)


Document Types
---------------

.. autosummarynameonly::

      pyexlatex.models.document.Document
      pyexlatex.models.standalone.Standalone
      pyexlatex.presentation.presentation.Presentation

Equations
---------------

.. autosummarynameonly::

      pyexlatex.models.equation.Equation

Sections
--------------

.. autosummarynameonly::

      pyexlatex.models.section.paragraphs.Paragraph
      pyexlatex.models.section.paragraphs.SubParagraph
      pyexlatex.models.section.sections.Section
      pyexlatex.models.section.sections.SubSection
      pyexlatex.models.section.sections.SubSubSection
      pyexlatex.models.section.appendix.Appendix
      pyexlatex.models.page.header.Header

Text
---------------

.. autosummarynameonly::

      pyexlatex.models.format.text.bold.Bold
      pyexlatex.models.format.text.underline.Underline
      pyexlatex.models.format.text.italics.Italics
      pyexlatex.models.sizes.textsizes.TextSize
      pyexlatex.models.format.text.color.main.TextColor
      pyexlatex.models.format.text.monospace.Monospace
      pyexlatex.models.format.text.smallcaps.SmallCaps
      pyexlatex.models.format.raw.Raw
      pyexlatex.models.format.text.Text
      pyexlatex.models.footnote.Footnote
      pyexlatex.models.format.code.python.Python
      pyexlatex.models.page.number.ThisPageNumber
      pyexlatex.models.format.paragraphindent.ParagraphIndent
      pyexlatex.models.latex.LaTeX

Lists
-----------

.. autosummarynameonly::

      pyexlatex.models.lists.unordered.UnorderedList
      pyexlatex.models.lists.unordered.OrderedList

Figures
------------

.. autosummarynameonly::

      pyexlatex.figure.models.figure.Figure
      pyexlatex.figure.models.subfigure.Subfigure
      pyexlatex.figure.models.graphic.Graphic

Tables
-----------

.. autosummarynameonly::

      pyexlatex.table.models.panels.Panel
      pyexlatex.table.models.data.table.DataTable
      pyexlatex.table.models.labels.table.LabelCollection
      pyexlatex.table.models.labels.table.LabelTable
      pyexlatex.table.models.labels.label.Label
      pyexlatex.table.models.table.table.Table
      pyexlatex.table.models.texgen.items.Tabular
      pyexlatex.table.models.data.valuestable.ValuesTable
      pyexlatex.table.models.texgen.alignment.ColumnAlignment
      pyexlatex.table.models.texgen.alignment.ColumnsAlignment
      pyexlatex.table.models.texgen.lines.TopRule
      pyexlatex.table.models.texgen.lines.MidRule
      pyexlatex.table.models.texgen.lines.BottomRule
      pyexlatex.table.models.texgen.lines.TableLineSegment
      pyexlatex.table.models.labels.multicolumnlabel.MultiColumnLabel
      pyexlatex.models.format.breaks.TableLineBreak
      pyexlatex.table.models.texgen.tabularstar.TabularStar

Layouts and Spacing
---------------------

.. autosummarynameonly::

      pyexlatex.models.format.centering.Center
      pyexlatex.models.control.newpage.PageBreak
      pyexlatex.models.format.fills.VFill
      pyexlatex.models.format.fills.HFill
      pyexlatex.models.format.vspace.VSpace
      pyexlatex.models.format.hspace.HSpace
      pyexlatex.models.format.hline.HLine
      pyexlatex.models.format.breaks.OutputLineBreak
      pyexlatex.models.format.nopagebreak.NoPageBreak
      pyexlatex.models.format.nolinebreak.NoLineBreak
      pyexlatex.models.format.paragraph.justifying.Justifying
      pyexlatex.models.control.group.Group
      pyexlatex.layouts.grid.CellLayout
      pyexlatex.layouts.grid.GridLayout
      pyexlatex.layouts.multicol.MultiCol
      pyexlatex.layouts.spaced.VerticallySpaced
      pyexlatex.layouts.spaced.HorizontallySpaced
      pyexlatex.models.format.paragraph.multicol.MultiColumn

References
------------

.. autosummarynameonly::

      pyexlatex.models.ref.Ref
      pyexlatex.models.ref.NameRef
      pyexlatex.models.label.Label
      pyexlatex.models.hyperlinks.Hyperlink

Citations
---------------

.. autosummarynameonly::

      pyexlatex.models.references.bibtex.article.BibTexArticle
      pyexlatex.models.references.bibtex.misc.BibTexMisc
      pyexlatex.models.references.bibtex.manual.BibTexManual
      pyexlatex.models.references.bibliography.Bibliography
      pyexlatex.models.references.citations.Cite
      pyexlatex.models.references.citations.CiteP
      pyexlatex.models.references.citations.CiteT

Presentations
---------------

.. autosummarynameonly::

      pyexlatex.presentation.presentation.Presentation
      pyexlatex.presentation.beamer.frame.frame.Frame
      pyexlatex.presentation.beamer.block.Block
      pyexlatex.presentation.beamer.block.AlertBlock
      pyexlatex.presentation.beamer.block.ExamplesBlock
      pyexlatex.logic.format.sizing.adjust_to_full_size_and_center
      pyexlatex.presentation.beamer.templates.frames.grid.GridFrame
      pyexlatex.presentation.beamer.templates.lists.dim_reveal_items.DimAndRevealListItem
      pyexlatex.presentation.beamer.templates.lists.dim_reveal_items.DimAndRevealListItems
      pyexlatex.presentation.beamer.templates.frames.two_col.TwoColumnGraphicDimRevealFrame
      pyexlatex.presentation.beamer.templates.frames.two_col.TwoColumnGraphicFrame
      pyexlatex.presentation.beamer.templates.frames.two_col.BasicTwoColumnGraphicFrame
      pyexlatex.presentation.beamer.templates.frames.two_col.BasicTwoColumnFrame
      pyexlatex.presentation.beamer.templates.frames.two_col.TwoColumnFrame
      pyexlatex.presentation.beamer.templates.frames.dim_reveal.DimRevealListFrame
      pyexlatex.presentation.beamer.templates.frames.graphic.GraphicFrame
      pyexlatex.presentation.beamer.templates.frames.graphic.MultiGraphicFrame
      pyexlatex.presentation.beamer.overlay.overlay.Overlay
      pyexlatex.presentation.beamer.overlay.range.Range
      pyexlatex.presentation.beamer.overlay.next.NextWithIncrement
      pyexlatex.presentation.beamer.overlay.next.NextWithoutIncrement
      pyexlatex.presentation.beamer.overlay.until_end.UntilEnd
      pyexlatex.presentation.beamer.templates.presentationappendix.PresentationAppendix

Colors
--------

.. autosummarynameonly::

      pyexlatex.models.format.text.color.deftypes.rgb.RGB
      pyexlatex.models.format.text.color.deftypes.hex.Hex

Template-Driven
-----------------------

.. autosummarynameonly::

      pyexlatex.models.template.Template
      pyexlatex.models.environmenttemplate.EnvironmentTemplate
      pyexlatex.models.jinja.JinjaEnvironment
      pyexlatex.models.jinja.JinjaTemplate
      pyexlatex.models.model.Model

LaTeX Package Management
----------------------------

.. autosummarynameonly::

      pyexlatex.models.package.Package


API Documentation
------------------

A full list of modules

.. toctree:: api/modules
   :maxdepth: 3

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
