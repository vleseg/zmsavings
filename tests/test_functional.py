import os
import re
import shutil
from subprocess import PIPE, Popen
import tempfile
# Third-party imports
import appdirs
import pytest


class PopenWrapper(object):
    _popen_kwargs = dict(stdout=PIPE, stderr=PIPE, stdin=PIPE)

    def __init__(self, command, stdin, expected_stdout):
        self._command = command
        self._stdin = stdin
        self._expected_stdout = expected_stdout

    def invoke_and_test(self):
        process = Popen(self._command, **self._popen_kwargs)

        stdin_as_str = '\n'.join(self._stdin)
        stdout, stderr = process.communicate(stdin_as_str)
        if stderr:
            error_message = (
                'Exception raised inside the wrapped process:\n'
                '============================================\n' + stderr +
                '\n============================================\n' +
                'Output before the error:\n' +
                '============================================\n' + stdout
            )
            raise AssertionError(error_message)
        assert self._expected_stdout == stdout.splitlines()


@pytest.fixture
def backup_and_restore_user_data():
    temp_dir = unicode(tempfile.mkdtemp())
    userdata_dir = appdirs.user_data_dir('zmsavings')

    if os.path.isdir(userdata_dir):
        for f in os.listdir(userdata_dir):
            src = os.path.join(userdata_dir, f)
            shutil.move(src, temp_dir)
    yield
    for f in os.listdir(userdata_dir):
        trash = os.path.join(userdata_dir, f)
        os.remove(trash)
    for f in os.listdir(temp_dir):
        bak = os.path.join(temp_dir, f)
        shutil.move(bak, userdata_dir)
    shutil.rmtree(temp_dir)


@pytest.mark.usefixtures('backup_and_restore_user_data')
def test_reads_paths_to_csv_files_from_stdin_and_visualizes_data():
    # zmsavings can be invoked from command-line (path to the core.py should
    # be passed as argument to the Python interpreter
    test_root = os.path.dirname(__file__)
    path_to_core_py = os.path.join(
        os.path.dirname(test_root), 'zmsavings_new', 'core.py')

    stdin = [
        # Provide path to CSV file with goals, when requested
        os.path.join(test_root, 'data', 'goals.csv'),
    ]
    stdout = [
        # Since userdata dir is empty, we don't know, where input files are, so
        # we should ask user for path to file with goals
        'Enter correct path to CSV file with goals (Ctrl+C to exit) ',
    ]

    process = PopenWrapper(
        ['python', path_to_core_py], stdin=stdin, expected_stdout=stdout)
    process.invoke_and_test()
