.. currentmodule:: abjad.tools.systemtools

TestCase
========

.. autoclass:: TestCase

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [background=transparent,
              bgcolor=transparent,
              color=lightslategrey,
              fontname=Arial,
              outputorder=edgesfirst,
              overlap=prism,
              penwidth=2,
              rankdir=LR,
              root="__builtin__.object",
              splines=spline,
              style="dotted, rounded",
              truecolor=true];
          node [colorscheme=pastel19,
              fontname=Arial,
              fontsize=12,
              penwidth=2,
              style="filled, rounded"];
          edge [color=lightsteelblue2,
              penwidth=2];
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.TestCase.TestCase" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>TestCase</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
          }
          subgraph cluster_unittest {
              graph [label=unittest];
              "unittest.case.TestCase" [color=3,
                  group=2,
                  label=TestCase,
                  shape=box];
          }
          "builtins.object" -> "unittest.case.TestCase";
          "unittest.case.TestCase" -> "abjad.tools.systemtools.TestCase.TestCase";
      }

Bases
-----

- :py:class:`unittest.case.TestCase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.systemtools.TestCase.TestCase.addCleanup
      ~abjad.tools.systemtools.TestCase.TestCase.addTypeEqualityFunc
      ~abjad.tools.systemtools.TestCase.TestCase.assertAlmostEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertAlmostEquals
      ~abjad.tools.systemtools.TestCase.TestCase.assertCountEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertDictContainsSubset
      ~abjad.tools.systemtools.TestCase.TestCase.assertDictEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertEquals
      ~abjad.tools.systemtools.TestCase.TestCase.assertFalse
      ~abjad.tools.systemtools.TestCase.TestCase.assertGreater
      ~abjad.tools.systemtools.TestCase.TestCase.assertGreaterEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertIn
      ~abjad.tools.systemtools.TestCase.TestCase.assertIs
      ~abjad.tools.systemtools.TestCase.TestCase.assertIsInstance
      ~abjad.tools.systemtools.TestCase.TestCase.assertIsNone
      ~abjad.tools.systemtools.TestCase.TestCase.assertIsNot
      ~abjad.tools.systemtools.TestCase.TestCase.assertIsNotNone
      ~abjad.tools.systemtools.TestCase.TestCase.assertLess
      ~abjad.tools.systemtools.TestCase.TestCase.assertLessEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertListEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertLogs
      ~abjad.tools.systemtools.TestCase.TestCase.assertMultiLineEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertNotAlmostEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertNotAlmostEquals
      ~abjad.tools.systemtools.TestCase.TestCase.assertNotEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertNotEquals
      ~abjad.tools.systemtools.TestCase.TestCase.assertNotIn
      ~abjad.tools.systemtools.TestCase.TestCase.assertNotIsInstance
      ~abjad.tools.systemtools.TestCase.TestCase.assertNotRegex
      ~abjad.tools.systemtools.TestCase.TestCase.assertNotRegexpMatches
      ~abjad.tools.systemtools.TestCase.TestCase.assertRaises
      ~abjad.tools.systemtools.TestCase.TestCase.assertRaisesRegex
      ~abjad.tools.systemtools.TestCase.TestCase.assertRaisesRegexp
      ~abjad.tools.systemtools.TestCase.TestCase.assertRegex
      ~abjad.tools.systemtools.TestCase.TestCase.assertRegexpMatches
      ~abjad.tools.systemtools.TestCase.TestCase.assertSequenceEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertSetEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertTrue
      ~abjad.tools.systemtools.TestCase.TestCase.assertTupleEqual
      ~abjad.tools.systemtools.TestCase.TestCase.assertWarns
      ~abjad.tools.systemtools.TestCase.TestCase.assertWarnsRegex
      ~abjad.tools.systemtools.TestCase.TestCase.assert_
      ~abjad.tools.systemtools.TestCase.TestCase.compare_captured_output
      ~abjad.tools.systemtools.TestCase.TestCase.compare_file_contents
      ~abjad.tools.systemtools.TestCase.TestCase.compare_lilypond_contents
      ~abjad.tools.systemtools.TestCase.TestCase.compare_path_contents
      ~abjad.tools.systemtools.TestCase.TestCase.compare_strings
      ~abjad.tools.systemtools.TestCase.TestCase.countTestCases
      ~abjad.tools.systemtools.TestCase.TestCase.debug
      ~abjad.tools.systemtools.TestCase.TestCase.defaultTestResult
      ~abjad.tools.systemtools.TestCase.TestCase.doCleanups
      ~abjad.tools.systemtools.TestCase.TestCase.fail
      ~abjad.tools.systemtools.TestCase.TestCase.failIf
      ~abjad.tools.systemtools.TestCase.TestCase.failIfAlmostEqual
      ~abjad.tools.systemtools.TestCase.TestCase.failIfEqual
      ~abjad.tools.systemtools.TestCase.TestCase.failUnless
      ~abjad.tools.systemtools.TestCase.TestCase.failUnlessAlmostEqual
      ~abjad.tools.systemtools.TestCase.TestCase.failUnlessEqual
      ~abjad.tools.systemtools.TestCase.TestCase.failUnlessRaises
      ~abjad.tools.systemtools.TestCase.TestCase.id
      ~abjad.tools.systemtools.TestCase.TestCase.normalize
      ~abjad.tools.systemtools.TestCase.TestCase.reset_string_io
      ~abjad.tools.systemtools.TestCase.TestCase.run
      ~abjad.tools.systemtools.TestCase.TestCase.setUp
      ~abjad.tools.systemtools.TestCase.TestCase.setUpClass
      ~abjad.tools.systemtools.TestCase.TestCase.shortDescription
      ~abjad.tools.systemtools.TestCase.TestCase.skipTest
      ~abjad.tools.systemtools.TestCase.TestCase.subTest
      ~abjad.tools.systemtools.TestCase.TestCase.tearDown
      ~abjad.tools.systemtools.TestCase.TestCase.tearDownClass
      ~abjad.tools.systemtools.TestCase.TestCase.test_path
      ~abjad.tools.systemtools.TestCase.TestCase.__call__
      ~abjad.tools.systemtools.TestCase.TestCase.__eq__
      ~abjad.tools.systemtools.TestCase.TestCase.__hash__
      ~abjad.tools.systemtools.TestCase.TestCase.__repr__
      ~abjad.tools.systemtools.TestCase.TestCase.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.TestCase.TestCase.test_path

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.addCleanup

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.addTypeEqualityFunc

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertAlmostEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertAlmostEquals

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertCountEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertDictContainsSubset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertDictEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertEquals

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertFalse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertGreater

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertGreaterEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertIn

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertIs

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertIsInstance

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertIsNone

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertIsNot

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertIsNotNone

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertLess

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertLessEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertListEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertLogs

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertMultiLineEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertNotAlmostEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertNotAlmostEquals

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertNotEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertNotEquals

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertNotIn

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertNotIsInstance

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertNotRegex

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertNotRegexpMatches

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertRaises

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertRaisesRegex

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertRaisesRegexp

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertRegex

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertRegexpMatches

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertSequenceEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertSetEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertTrue

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertTupleEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertWarns

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assertWarnsRegex

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.assert_

.. automethod:: abjad.tools.systemtools.TestCase.TestCase.compare_captured_output

.. automethod:: abjad.tools.systemtools.TestCase.TestCase.compare_file_contents

.. automethod:: abjad.tools.systemtools.TestCase.TestCase.compare_lilypond_contents

.. automethod:: abjad.tools.systemtools.TestCase.TestCase.compare_path_contents

.. automethod:: abjad.tools.systemtools.TestCase.TestCase.compare_strings

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.countTestCases

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.debug

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.defaultTestResult

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.doCleanups

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.fail

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.failIf

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.failIfAlmostEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.failIfEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.failUnless

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.failUnlessAlmostEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.failUnlessEqual

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.failUnlessRaises

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.id

.. automethod:: abjad.tools.systemtools.TestCase.TestCase.normalize

.. automethod:: abjad.tools.systemtools.TestCase.TestCase.reset_string_io

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.run

.. automethod:: abjad.tools.systemtools.TestCase.TestCase.setUp

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.shortDescription

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.skipTest

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.subTest

.. automethod:: abjad.tools.systemtools.TestCase.TestCase.tearDown

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.setUpClass

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.tearDownClass

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestCase.TestCase.__str__
