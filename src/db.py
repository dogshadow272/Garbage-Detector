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
    '''Deletes bin with `id` from database'''
    sql(f'DELETE FROM info WHERE id="{id}"')

    for (time,) in sql(f'SELECT time FROM bin{id}').fetchall():
        sql(f'DROP TABLE {id}_{time}')

    sql(f'DROP TABLE bin{id}')
    con.commit()


def new_litter_entry(id: str, time: int, litter_items: list):
    '''Create a new entry for litter data.'''

    table_name = f'{id}_{time}'
    sql(f'INSERT INTO bin{id} VALUES ({time}, {len(litter_items)})')
    sql(f'CREATE TABLE {table_name} (confidence, width, height, left, top)')

    for i in litter_items:
        sql(
            f'INSERT INTO {table_name} VALUES ({i["confidence"]}, {i["width"]}, {i["height"]}, {i["left"]}, {i["top"]})'
        )

    con.commit()


def get_full_bin(id: str):
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


def fetch_bins():
    bins = _to_dicts('info')

    # These keys are not stored in the database, so we update the dicts here
    for i in bins:
        i['cam_connected'] = time() < i['cam_expiry']
        i['latest_litter_count'] = sql(
            f'SELECT litter_count FROM bin{i["id"]} ORDER BY time DESC'
        ).fetchone()[0]

    return bins


if __name__ == '__main__':
    delete_bin('e21217')
