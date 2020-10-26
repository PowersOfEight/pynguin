#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2020 Pynguin Contributors
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#
from pynguin.generation.export.unittestexporter import UnitTestExporter


def test_export_sequence(exportable_test_case, tmp_path):
    path = tmp_path / "generated.py"
    exporter = UnitTestExporter()
    exporter.export_sequences(str(path), [exportable_test_case, exportable_test_case])
    assert (
        path.read_text()
        == """# Automatically generated by Pynguin.
import unittest
import tests.fixtures.accessibles.accessible as module0


class GeneratedTestSuite(unittest.TestCase):

    def test_case_0(self):
        var0 = 5
        var1 = module0.SomeType(var0)
        assert var1 == 5

    def test_case_1(self):
        var0 = 5
        var1 = module0.SomeType(var0)
        assert var1 == 5
"""
    )
