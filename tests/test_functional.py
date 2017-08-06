import os
import re
import shutil
from subprocess import PIPE, Popen
import tempfile
# Third-party imports
import appdirs
import pytest


class PopenWrapper(object):
    def __init__(self, command):
        self._process = Popen(
            command, stdout=PIPE, stderr=PIPE, stdin=PIPE, bufsize=1)

    def read(self):
        stdout, stderr = self._process.communicate()
        if stderr:
            raise AssertionError(
                'Exception raised inside the wrapped process:\n'
                '============================================\n' + stderr
            )
        return stdout


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


# todo: in wrapper write to stdin everything at once and read all stdout at once
# todo: in test, however, make it look like we everything consequently
@pytest.mark.usefixtures('backup_and_restore_user_data')
def test_reads_paths_to_csv_files_from_stdin_and_visualizes_data():
    # zmsavings can be invoked from command-line (path to the core.py should
    # be passed as argument to the Python interpreter
    path_to_core_py = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'zmsavings_new', 'core.py')

    process = PopenWrapper(['python', path_to_core_py])

    # Since userdata dir is empty, we don't know, where input files are, so
    # we should ask user for path to file with goals...
    out = process.read()
    assert re.match(
        r'^Enter correct path to CSV file with goals \(Ctrl\+C to exit\): $',
        out)

    # ...and read his input
    pytest.fail('TBD')
