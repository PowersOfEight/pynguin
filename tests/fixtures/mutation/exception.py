#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2022 Pynguin Contributors
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#
def foo() -> None:
    alist = [1, 2]
    # Fails on mutation
    assert len(alist) == 2
    return None
