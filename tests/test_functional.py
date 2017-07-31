import os
import re
import shutil
from subprocess import PIPE, Popen
import tempfile
# Third-party imports
import appdirs
import pytest


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
    path_to_core_py = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'zmsavings_new', 'core.py')

    process = Popen(
        ['python', path_to_core_py], stdout=PIPE, stderr=PIPE, bufsize=1)

    # Since userdata dir is empty, we don't know, where input files are, so
    # we should ask user for path to file with goals...
    stdout, stderr = process.communicate()
    assert re.match(
        r'^Enter correct path to CSV file with goals \(Ctrl\+C to exit\): $',
        stdout)

    # ...and read his input
    pytest.fail('TBD')
