'''`db.py` manages the SQL database stored in `db.db`, 
which consists of three types of tables.

The first type is the main table, called `info`, which contains general 
information about bins and cameras. Its columns are as follows:

1. `id`: UID of a bin or camera.
2. `img_path`: File path of the bin's image.
3. `address`: Address at which the bin is located.
4. `location`: Specific place at which the bin is located.
5. `cam_expiry`: Unix timestamp at which the bin's camera will be 
considered disconnected. This timestamp is renewed every time the bin's 
camera sends a POST request to the webserver.

The second type of tables contain basic information about a camera's image
captures. It follows the naming convention `bin_<id>`, where `<id>` is the
UID of the bin. Its columns are as follows:

1. `timestamp`: Unix timestamp at which an image was captured.
2. `litter_count`: Number of litter items detected in the image.

The third type of tables contain detailed information about the contents
of a captured image. It follows the naming convention `bin_<id>_<timestamp>`,
where `<id>` is the UID of the bin, and `timestamp` is the Unix timestamp at
which the image was captured. Each row in these tables represents a bounding 
box around a litter item. Its columns are as follows:

1. `confidence`: Rekognition's confidence that the bounding box contains
a litter item, on a scale of 0 to 100.
2. `width`: Width of the bounding box as a ratio of the overall image width.
3. `height`: Height of the bounding box as a ratio of the overall image height.
4. `left`: Left coordinate of the bounding box as a ratio of overall image width. 
5. `top`: Top coordinate of the bounding box as a ratio of overall image height.
'''

import sqlite3
from time import time
from uuid import uuid4

# `cd` into the src directory before running db.py or app.py
con = sqlite3.connect('db.db', check_same_thread=False)
sql = con.cursor().execute

###   Internal helper-functions   ###


def _get_col_names(table_name: str) -> 'list[str]':
    '''Return the column names of the table `table_name`.'''
    return [i[1] for i in sql(f'PRAGMA table_info({table_name})').fetchall()]


def _to_dict(table_name: str, predicate: str) -> dict:
    '''
    Find the row in the SQL table `table_name` that matches the predicate, then
    convert that row to a dictionary, with the keys being the table's column names.
    '''
    keys = _get_col_names(table_name)
    values = sql(f'SELECT * FROM {table_name} WHERE {predicate}').fetchone()
    return {
        k: v for k, v in zip(keys, values)
    }


def _to_dicts(table_name: str) -> 'list[dict]':
    '''
    Convert a SQL table to a list of dictionaries,
    with each dictionary being a row of the table.
    '''
    keys = _get_col_names(table_name)
    return [
        {
            k: v for k, v in zip(keys, row)
        }
        for row in sql(f'SELECT * FROM {table_name}').fetchall()
    ]


###   Public interfaces   ###


def create_bin(
        img_path: str = 'bins/0.jpg',
        address: str = '209 Bishan Street 23',
        location: str = 'Staircase 5A',
        cam_expiry: int = 0) -> str:
    '''Add a new bin to the database.'''
    # Generate unique id
    id = str(uuid4())[:6]
    sql(f'INSERT INTO info VALUES ("{id}", "{img_path}", "{address}", "{location}", {cam_expiry})')
    sql(f'CREATE TABLE bin{id} (time, litter_count)')
    con.commit()

    return id


def update_bin(id: str, property: str, value):
    '''Set `property` of bin #`id` to `value`.'''
    sql(f'UPDATE info SET {property}={value} WHERE id="{id}"')
    con.commit()


def delete_bin(id: str):
    '''Delete bin #`id` from database.'''
    sql(f'DELETE FROM info WHERE id="{id}"')

    for (time,) in sql(f'SELECT time FROM bin{id}').fetchall():
        sql(f'DROP TABLE {id}_{time}')

    sql(f'DROP TABLE bin{id}')
    con.commit()


def new_litter_entry(id: str, timestamp: int, litter_items: list):
    '''Create a new entry for litter data.'''

    table_name = f'{id}_{timestamp}'
    sql(f'INSERT INTO bin{id} VALUES ({timestamp}, {len(litter_items)})')
    sql(f'CREATE TABLE {table_name} (confidence, width, height, left, top)')

    for i in litter_items:
        sql(
            f'INSERT INTO {table_name} VALUES ({i["confidence"]}, {i["width"]}, {i["height"]}, {i["left"]}, {i["top"]})'
        )

    con.commit()


def get_full_bin(id: str):
    '''Return a detailed dict of bin #`id`.'''
    bin = _to_dict('info', f'id="{id}"')

    # Include extra info
    bin['captures'] = []

    for (time, litter_count) in sql(f'SELECT * FROM bin{id}').fetchall():
        bin['captures'].append({
            'timestamp': time,
            'litterCount': litter_count,
            'boundingBoxes': _to_dicts(f'{id}_{time}')
        })

    return bin


def fetch_bins() -> 'list[dict]':
    '''Return a dict of each bin.'''
    bins = _to_dicts('info')

    # These keys are not stored in the database, so we update the dicts here
    for i in bins:
        i['cam_connected'] = time() < i['cam_expiry']
        latest_litter_count = sql(
            f'SELECT litter_count FROM bin{i["id"]} ORDER BY time DESC'
        ).fetchone()

        if latest_litter_count is not None:
            i['latest_litter_count'] = latest_litter_count[0]
        else:
            i['latest_litter_count'] = None

    return bins


if __name__ == '__main__':
    delete_bin('e21217')
