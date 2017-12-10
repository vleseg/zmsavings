from __future__ import print_function
import os
# Third-party imports
import appdirs

APP_NAME = 'ZmSavings'


def get_random_file_path():
    pass


def get_or_create_user_data_dir():
    user_data_dir = appdirs.user_data_dir(APP_NAME)
    if not os.path.isdir(user_data_dir):
        os.makedirs(user_data_dir)

    return user_data_dir


def read_path(prompt):
    while True:
        path = raw_input(prompt + ' (Ctrl+C to abort) ')
        if os.path.isfile(path):
            return path
        print_function('File does not exist')


def read_yes_no(prompt):
    while True:
        user_input = raw_input(prompt + ' (y/n or Ctrl+C to abort) ')

        if user_input.lower() == 'y':
            return True
        elif user_input.lower() == 'n':
            return False


def path_from_appdata_or_input(filename):
    path_to_ptr_file = os.path.join(get_or_create_user_data_dir(), filename)

    if os.path.isfile(path_to_ptr_file):
        with open(path_to_ptr_file, 'r') as f:
            path = f.read()
            if os.path.isfile(path):
                if read_yes_no("Do you want to use file '{0}'?".format(path)):
                    return path
            else:
                print_function("Stored path '{0}' does not exist".format(path))

    with open(path_to_ptr_file, 'w') as f:
        path = read_path("Enter valid path to '{0}'".format(filename))
        f.write(path)

        return path
