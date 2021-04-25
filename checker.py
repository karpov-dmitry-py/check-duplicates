import logging
import random
import sys
import json

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def _log(msg):
    logging.info(msg)


def _err(msg):
    logging.error(msg)


def _exc(exception):
    return f'Error: ({exception.__class__.__name__}) {str(exception)}'


def _save(data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        _log(f'Saved data to file: {filename}')
    except Exception as err:
        err_msg = f'Failed to save data to file: {filename}: {_exc(err)}'
        _err(err_msg)
        raise Exception(err_msg)


def _read(filename):
    try:
        with open(filename) as file:
            data = json.load(file)
        _log(f'Read data from file: {filename}')
        return data
    except Exception as err:
        err_msg = f'Failed to read data from file: {filename}: {_exc(err)}'
        _err(err_msg)
        raise Exception(err_msg)


def _get_random_int(min=1000, max=50000):
    return random.randint(min, max)


class Checker:
    default_source_filename = 'source.json'
    default_result_filename = 'duplicates.json'

    def __init__(self):
        self.create_source()

    def create_source(self):
        source = [
            {
                'user': 'John',
                'age': 30,
                'lang_id': 10,
            },
            {
                'user': 'Mike',
                'age': 32,
                'lang_id': 18,
            },
            {
                'user': 'Nick',
                'age': 27,
                'lang_id': 5,
            },
        ]

        data = []
        _id = 0
        for _ in range(5):
            for item in source:
                _item = item.copy()
                _id += 1
                _log(f'_id: {_id}')
                _item['row_id'] = _id
                _item['balance'] = _get_random_int()
                data.append(_item)
        _save(data, self.default_source_filename)

    def check_source(self, unique_fields, filename=None):
        filename = filename or self.default_source_filename
        data = _read(filename)
        duplicates = dict()
        for row in data:
            _fields = ' | '.join(str(row[field]) for field in unique_fields)
            if duplicates.get(_fields) is not None:
                duplicates[_fields].append({'duplicate_row_id': row['row_id'], 'duplicate_row': row})
            else:
                duplicates[_fields] = []

        _save(duplicates, self.default_result_filename)


def main():
    checker = Checker()
    unique_fields = ('user', 'age', 'lang_id',)
    checker.check_source(unique_fields=unique_fields)


if __name__ == '__main__':
    main()
