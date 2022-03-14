#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2022 Pynguin Contributors
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#
import argparse
import importlib
import logging
import os
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock, call

import pytest

import pynguin.configuration as config
from pynguin.cli import (
    _DANGER_ENV,
    _create_argument_parser,
    _expand_arguments_if_necessary,
    _setup_logging,
    main,
)
from pynguin.generator import ReturnCode


def test_main_empty_argv():
    with mock.patch("pynguin.cli.run_pynguin") as generator_mock:
        with mock.patch("pynguin.cli._create_argument_parser") as parser_mock:
            with mock.patch("pynguin.cli._setup_logging"):
                with mock.patch("pynguin.cli._setup_output_path"):
                    with mock.patch.dict(os.environ, {_DANGER_ENV: "foobar"}):
                        generator_mock.return_value = ReturnCode.OK
                        parser = MagicMock()
                        parser_mock.return_value = parser
                        main()
                        assert len(parser.parse_args.call_args[0][0]) > 0


def test_main_with_argv():
    with mock.patch("pynguin.cli.run_pynguin") as generator_mock:
        with mock.patch("pynguin.cli._create_argument_parser") as parser_mock:
            with mock.patch("pynguin.cli._setup_logging"):
                with mock.patch("pynguin.cli._setup_output_path"):
                    with mock.patch.dict(os.environ, {_DANGER_ENV: "foobar"}):
                        generator_mock.return_value = ReturnCode.OK
                        parser = MagicMock()
                        parser_mock.return_value = parser
                        args = ["foo", "--help"]
                        main(args)
                        assert parser.parse_args.call_args == call(args[1:])


def test_main_no_env_marker():
    with mock.patch.dict(os.environ, {}, clear=True):
        assert main([]) == -1


def test__create_argument_parser():
    parser = _create_argument_parser()
    assert isinstance(parser, argparse.ArgumentParser)


def test__setup_logging_standard_with_log_file(tmp_path):
    logging.shutdown()
    importlib.reload(logging)
    _setup_logging(log_file=str(tmp_path / "pynguin-test.log"), verbosity=0)
    logger = logging.getLogger("")
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.WARNING
    assert len(logger.handlers) == 2
    logging.shutdown()
    importlib.reload(logging)


def test__setup_logging_single_verbose_without_log_file():
    logging.shutdown()
    importlib.reload(logging)
    _setup_logging(1)
    logger = logging.getLogger("")
    assert len(logger.handlers) == 1
    assert logger.level == logging.INFO
    logging.shutdown()
    importlib.reload(logging)


def test__setup_logging_double_verbose_without_log_file():
    logging.shutdown()
    importlib.reload(logging)
    _setup_logging(2)
    logger = logging.getLogger("")
    assert len(logger.handlers) == 1
    assert logger.level == logging.DEBUG
    logging.shutdown()
    importlib.reload(logging)


@pytest.mark.parametrize(
    "arguments, expected",
    [
        pytest.param(
            ["--foo", "bar", "--bar", "foo"], ["--foo", "bar", "--bar", "foo"]
        ),
        pytest.param(
            ["--foo", "bar", "--output_variables", "foo,bar,baz", "--bar", "foo"],
            ["--foo", "bar", "--output_variables", "foo", "bar", "baz", "--bar", "foo"],
        ),
        pytest.param(
            ["--foo", "bar", "--output_variables", "baz", "--bar", "foo"],
            ["--foo", "bar", "--output_variables", "baz", "--bar", "foo"],
        ),
        pytest.param(
            ["--foo", "bar", "--output-variables", "foo,bar,baz", "--bar", "foo"],
            ["--foo", "bar", "--output-variables", "foo", "bar", "baz", "--bar", "foo"],
        ),
        pytest.param(
            ["--foo", "bar", "--output-variables", "baz", "--bar", "foo"],
            ["--foo", "bar", "--output-variables", "baz", "--bar", "foo"],
        ),
        pytest.param(
            ["--foo", "bar", "--coverage_metrics", "foo,bar,baz", "--bar", "foo"],
            ["--foo", "bar", "--coverage_metrics", "foo", "bar", "baz", "--bar", "foo"],
        ),
        pytest.param(
            ["--foo", "bar", "--coverage_metrics", "baz", "--bar", "foo"],
            ["--foo", "bar", "--coverage_metrics", "baz", "--bar", "foo"],
        ),
        pytest.param(
            ["--foo", "bar", "--coverage-metrics", "foo,bar,baz", "--bar", "foo"],
            ["--foo", "bar", "--coverage-metrics", "foo", "bar", "baz", "--bar", "foo"],
        ),
        pytest.param(
            ["--foo", "bar", "--coverage-metrics", "baz", "--bar", "foo"],
            ["--foo", "bar", "--coverage-metrics", "baz", "--bar", "foo"],
        ),
        pytest.param(
            [
                "--foo",
                "bar",
                "--coverage_metrics",
                "foo,bar,baz",
                "--output_variables",
                "foo,bar,baz",
                "--bar",
                "foo",
            ],
            [
                "--foo",
                "bar",
                "--coverage_metrics",
                "foo",
                "bar",
                "baz",
                "--output_variables",
                "foo",
                "bar",
                "baz",
                "--bar",
                "foo",
            ],
        ),
        pytest.param(
            [
                "--foo",
                "bar",
                "--output_variables",
                "foo,bar,baz",
                "--coverage_metrics",
                "foo,bar,baz",
                "--bar",
                "foo",
            ],
            [
                "--foo",
                "bar",
                "--output_variables",
                "foo",
                "bar",
                "baz",
                "--coverage_metrics",
                "foo",
                "bar",
                "baz",
                "--bar",
                "foo",
            ],
        ),
        pytest.param(
            [
                "--foo",
                "bar",
                "--coverage-metrics",
                "foo,bar,baz",
                "--output-variables",
                "foo,bar,baz",
                "--bar",
                "foo",
            ],
            [
                "--foo",
                "bar",
                "--coverage-metrics",
                "foo",
                "bar",
                "baz",
                "--output-variables",
                "foo",
                "bar",
                "baz",
                "--bar",
                "foo",
            ],
        ),
        pytest.param(
            [
                "--foo",
                "bar",
                "--output-variables",
                "foo,bar,baz",
                "--coverage-metrics",
                "foo,bar,baz",
                "--bar",
                "foo",
            ],
            [
                "--foo",
                "bar",
                "--output-variables",
                "foo",
                "bar",
                "baz",
                "--coverage-metrics",
                "foo",
                "bar",
                "baz",
                "--bar",
                "foo",
            ],
        ),
    ],
)
def test__expand_arguments_if_necessary(arguments, expected):
    result = _expand_arguments_if_necessary(arguments)
    assert result == expected


@pytest.mark.skip(reason="Need to figure out why this changes")
def test_load_configuration_from_file(tmp_path):
    config_file = Path(".").absolute()
    if config_file.name != "tests":
        config_file /= "tests"  # pragma: no cover
    config_file = config_file / "fixtures" / "test.conf"
    parser = _create_argument_parser()
    parsed = parser.parse_args(
        [
            f"@{config_file}",
            "--module_name",
            "hurz",
            "--project_path",
            str(tmp_path),
            "--output_path",
            str(tmp_path),
            "--budget",
            "50",
        ]
    )
    configuration = parsed.config
    expected = config.Configuration(
        algorithm=config.Algorithm.MOSA,
        module_name="hurz",
        project_path=str(tmp_path),
        test_case_output=config.TestCaseOutputConfiguration(output_path=str(tmp_path)),
    )
    expected.seeding.seed = 42
    expected.stopping.budget = 50
    expected.statistics_output.configuration_id = "merge checker"
    assert configuration == expected
