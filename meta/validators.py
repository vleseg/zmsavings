import os


def file_exists(_instance, _attribute, path):
    if not os.path.isfile(path):
        raise ValueError('File not found: {0}'.format(path))
