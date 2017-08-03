import os
# Third-party imports
import appdirs

APP_NAME = 'ZmSavings'


def get_user_data_dir():
    user_data_dir = appdirs.user_data_dir(APP_NAME)
    if not os.path.isdir(user_data_dir):
        os.makedirs(user_data_dir)

    return user_data_dir


def path_from_appdata_or_input(filename):
    path_to_ptr_file = os.path.join(get_user_data_dir(), filename)

    return open(path_to_ptr_file, 'rb')
