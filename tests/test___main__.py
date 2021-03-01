#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2021 Pynguin Contributors
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#
import runpy
from unittest import mock

import pytest


@mock.patch("pynguin.cli.main")
def test___main__(main):
    main.return_value = 42
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        runpy.run_module("pynguin", run_name="__main__")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 42
