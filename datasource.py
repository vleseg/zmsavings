import unicodecsv as csv


class CSVSource(object):
    def __init__(self, conn_settings):
        path = conn_settings.path
        print 'Loading file "{0}"'.format(path)

        f = open(path, 'rb')
        self.reader = csv.reader(f)
        for _ in xrange(conn_settings.header_row - 1):
            next(self.reader)
        header = next(self.reader)
        if len(set(header)) < len(header):
            raise ValueError('Non-unique CSV headers in file "{0}"'
                             .format(path))

        self.header_map = {}
        for field_name in conn_settings.use_fields:
            try:
                self.header_map[field_name] = header.index(field_name)
            except ValueError:
                raise ValueError(
                    'Field name "{0}" defined in connection settings, but not '
                    'found in "{1}"'.format(field_name, path))

    def __iter__(self):
        for csv_entry in self.reader:
            yield {field_name: csv_entry[idx]
                   for field_name, idx in self.header_map.items()}

    def all(self):
        return self.__iter__()
