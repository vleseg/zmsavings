import os


def get_user_data_dir():
    pass


def path_from_appdata_or_input(filename):
    path_to_ptr_file = os.path.join(get_user_data_dir(), filename)

    return open(path_to_ptr_file, 'rb')
