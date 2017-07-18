from itertools import izip_longest, tee
import os
# Third-party imports
import appdirs


def read_yes_no(prompt):
    prompt = prompt.strip() + ' (y/n or Ctrl+C to abort) '
    while True:
        s = raw_input(prompt)
        if s in 'yY':
            return True
        elif s in 'nN':
            return False


def read_path(prompt):
    prompt = prompt.strip() + ' (Ctrl+C to abort) '
    while True:
        s = raw_input(prompt)
        if os.path.isfile(s):
            return s
        print 'File does not exist: {0}'.format(s)


def path_from_appdata_or_input(app_name, appdata_name, file_description):
    print '{0}: loading file...'.format(file_description)

    data_dir = appdirs.user_data_dir(app_name)
    appdata_file = os.path.join(data_dir, appdata_name)
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    if os.path.isfile(appdata_file):
        with open(appdata_file, 'r') as f:
            path = f.read().strip()
        yes_no_prompt = '{0}: do you want to use file "{1}"?'.format(
            file_description, path)
        if os.path.isfile(path) and read_yes_no(yes_no_prompt):
            return path
        os.remove(appdata_file)

    path = read_path('{0}: enter correct path'.format(file_description))
    with open(appdata_file, 'w') as f:
        f.write(path)
    return path


# Based on https://docs.python.org/2.7/library/itertools.html#recipes
def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return izip_longest(a, b)
