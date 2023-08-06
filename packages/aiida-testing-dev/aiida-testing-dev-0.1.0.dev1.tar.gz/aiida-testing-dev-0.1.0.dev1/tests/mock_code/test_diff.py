# -*- coding: utf-8 -*-
"""
Test basic usage of the mock code on examples using aiida-diff.
"""

import shutil
import os
import tempfile
from pathlib import Path

import pytest

from aiida import orm
from aiida.engine import run_get_node
from aiida.plugins import CalculationFactory, DataFactory

CALC_ENTRY_POINT = 'diff'

TEST_DATA_DIR = Path(__file__).resolve().parent / 'data'


@pytest.fixture
def generate_diff_inputs(datadir):
    """
    Generates inputs for the diff calculation.
    """

    def _generate_diff_inputs():
        with open(datadir / 'file1.txt', 'rb') as f1_obj:
            file1 = orm.SinglefileData(file=f1_obj)
        with open(datadir / 'file2.txt', 'rb') as f2_obj:
            file2 = orm.SinglefileData(file=f2_obj)

        inputs = {
            "file1": file1,
            "file2": file2,
            "metadata": {
                "options": {
                    "withmpi": False,
                    "resources": {
                        "num_machines": 1,
                        "num_mpiprocs_per_machine": 1
                    }
                }
            },
            "parameters": DataFactory("diff")(dict={
                "ignore-case": False
            })
        }
        return inputs

    return _generate_diff_inputs


def check_diff_output(result):
    """
    Checks the result from a diff calculation against a reference.
    """
    diff_res_lines = tuple(
        line.strip() for line in result['diff'].get_content().splitlines() if line.strip()
    )
    assert diff_res_lines == (
        "1,2c1", "< Lorem ipsum dolor..", "<", "---",
        "> Please report to the ministry of silly walks."
    )


@pytest.fixture(scope='function')
def relative_code(testing_config):
    """
    Temporarily copy the diff executable into the test folder
    """
    shutil.copy('/usr/bin/diff', os.fspath(testing_config.file_path.parent))
    try:
        yield
    finally:
        os.remove(testing_config.file_path.parent / 'diff')


def test_basic(mock_code_factory, generate_diff_inputs):  # pylint: disable=redefined-outer-name
    """
    Check that mock code takes data from cache, if inputs are recognized.
    """
    mock_code = mock_code_factory(
        label='diff',
        data_dir_abspath=TEST_DATA_DIR,
        entry_point=CALC_ENTRY_POINT,
        ignore_paths=('_aiidasubmit.sh', 'file*txt')
    )

    res, node = run_get_node(
        CalculationFactory(CALC_ENTRY_POINT), code=mock_code, **generate_diff_inputs()
    )
    assert node.exit_status == 0, f"diff calculation failed with exit status {node.exit_status}"
    assert node.is_finished_ok
    check_diff_output(res)


def test_inexistent_data(mock_code_factory, generate_diff_inputs):  # pylint: disable=redefined-outer-name
    """
    Check that the mock code runs external executable if there is no existing data.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        mock_code = mock_code_factory(
            label='diff',
            data_dir_abspath=temp_dir,
            entry_point=CALC_ENTRY_POINT,
            ignore_paths=('_aiidasubmit.sh', 'file*txt')
        )

        res, node = run_get_node(
            CalculationFactory(CALC_ENTRY_POINT), code=mock_code, **generate_diff_inputs()
        )
        assert node.is_finished_ok
        check_diff_output(res)


def test_broken_code(mock_code_factory, generate_diff_inputs):  # pylint: disable=redefined-outer-name
    """
    Check that the mock code works also when no executable is given, if the result exists already.
    """
    mock_code = mock_code_factory(
        label='diff-broken',
        data_dir_abspath=TEST_DATA_DIR,
        entry_point=CALC_ENTRY_POINT,
        ignore_paths=('_aiidasubmit.sh', 'file?.txt')
    )

    res, node = run_get_node(
        CalculationFactory(CALC_ENTRY_POINT), code=mock_code, **generate_diff_inputs()
    )
    assert node.is_finished_ok
    check_diff_output(res)


def test_broken_code_require(mock_code_factory):
    """
    Check that the mock code raises, if executable path is required but not provided.
    """

    with pytest.raises(ValueError):
        mock_code_factory(
            label='diff-broken',
            data_dir_abspath=TEST_DATA_DIR,
            entry_point=CALC_ENTRY_POINT,
            ignore_paths=('_aiidasubmit.sh', 'file?.txt'),
            _config_action='require',
        )


def test_broken_code_generate(mock_code_factory, testing_config):
    """
    Check that mock code adds missing key to testing config, when asked to 'generate'.
    """
    mock_code_factory(
        label='diff-broken',
        data_dir_abspath=TEST_DATA_DIR,
        entry_point=CALC_ENTRY_POINT,
        ignore_paths=('_aiidasubmit.sh', 'file?.txt'),
        _config_action='generate',
    )
    assert 'diff-broken' in testing_config.get('mock_code')


def test_regenerate_test_data(mock_code_factory, generate_diff_inputs, datadir):  # pylint: disable=redefined-outer-name
    """
    Check that mock code regenerates test data if asked to do so.

    Note: So far, this only tests that the test still runs fine.
    Should e.g. check timestamp on test data directory.
    """
    mock_code = mock_code_factory(
        label='diff',
        data_dir_abspath=TEST_DATA_DIR,
        entry_point=CALC_ENTRY_POINT,
        ignore_paths=('_aiidasubmit.sh', ),
        _regenerate_test_data=True,
    )

    res, node = run_get_node(
        CalculationFactory(CALC_ENTRY_POINT), code=mock_code, **generate_diff_inputs()
    )
    assert node.is_finished_ok
    check_diff_output(res)

    # check that ignore_paths works
    assert not (datadir / '_aiidasubmit.sh').is_file()
    assert (datadir / 'file1.txt').is_file()


@pytest.mark.usefixtures('relative_code')
def test_regenerate_test_data_relative(mock_code_factory, generate_diff_inputs, datadir):  # pylint: disable=redefined-outer-name
    """
    Check that mock code regenerates test data if asked to do so
    for a executable specified with a relative path.

    Note: So far, this only tests that the test still runs fine.
    Should e.g. check timestamp on test data directory.
    """
    mock_code = mock_code_factory(
        label='diff-relative',
        data_dir_abspath=TEST_DATA_DIR,
        entry_point=CALC_ENTRY_POINT,
        ignore_paths=('_aiidasubmit.sh', ),
        _regenerate_test_data=True,
    )

    res, node = run_get_node(
        CalculationFactory(CALC_ENTRY_POINT), code=mock_code, **generate_diff_inputs()
    )
    assert node.is_finished_ok
    check_diff_output(res)

    # check that ignore_paths works
    assert not (datadir / '_aiidasubmit.sh').is_file()
    assert (datadir / 'file1.txt').is_file()


def test_regenerate_test_data_executable(mock_code_factory, generate_diff_inputs, datadir):  # pylint: disable=redefined-outer-name
    """
    Check that mock code regenerates test data if asked to do so
    for a executable specified is only specified via the executable name

    Note: So far, this only tests that the test still runs fine.
    Should e.g. check timestamp on test data directory.
    """
    mock_code = mock_code_factory(
        label='diff-executable',
        data_dir_abspath=TEST_DATA_DIR,
        entry_point=CALC_ENTRY_POINT,
        ignore_paths=('_aiidasubmit.sh', ),
        executable_name='diff',
        _regenerate_test_data=True,
    )

    res, node = run_get_node(
        CalculationFactory(CALC_ENTRY_POINT), code=mock_code, **generate_diff_inputs()
    )
    assert node.is_finished_ok
    check_diff_output(res)

    # check that ignore_paths works
    assert not (datadir / '_aiidasubmit.sh').is_file()
    assert (datadir / 'file1.txt').is_file()
