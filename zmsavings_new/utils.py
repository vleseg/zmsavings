import os
# Third-party imports
import appdirs

APP_NAME = 'ZmSavings'


def get_user_data_dir():
    user_data_dir = appdirs.user_data_dir(APP_NAME)
    if not os.path.isdir(user_data_dir):
        os.makedirs(user_data_dir)

    return user_data_dir


def read_path(prompt):
    pass


def path_from_appdata_or_input(filename):
    path_to_ptr_file = os.path.join(get_user_data_dir(), filename)

    if os.path.isfile(path_to_ptr_file):
        with open(path_to_ptr_file, 'rb') as f:
            return f.read()
    else:
        return read_path("Enter valid path to '{0}'".format(filename))
