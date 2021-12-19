import sqlite3
from time import time

con = sqlite3.connect('db.db', check_same_thread=False)
sql = con.cursor().execute


def cam_expiries():
    return [i[0] for i in sql('SELECT cam_expiry FROM info')]


def create_bin(
        id: int,
        img_path: str = 'bins/0.jpg',
        address: str = '209 Bishan Street 23',
        location: str = 'Staircase 5A',
        cam_expiry: int = 0):
    '''Add a new bin to the database.'''

    # TODO: remove the 0 when the SQL table has been updated
    sql(f'INSERT INTO info VALUES ({id}, "{img_path}", "{address}", "{location}", {cam_expiry})')
    sql(f'CREATE TABLE bin{id} (time, litter_count)')
    sql(f'INSERT INTO bin{id} VALUES (0, 0)')

    con.commit()


def update_bin(id: int, property: str, value):
    sql(f'UPDATE info SET {property}={value} WHERE id={id}')
    con.commit()


def delete_bin(id: int):
    '''Deletes bin with `id` from database'''
    sql(f'DELETE FROM info WHERE id={id}')
    sql(f'DROP TABLE bin{id}')
    con.commit()


def get_columns(table: str) -> list:
    '''Return a list of the columns in `table`.'''
    return [i[1] for i in sql(f'PRAGMA table_info({table})').fetchall()]


def get_next_id():
    return len(sql('SELECT id FROM info').fetchall()) + 1


def get_litter_counts(id):
    return [i[0] for i in sql(f'SELECT litter_count FROM bin{id}').fetchall()]


def get_property(id: int, property: str):
    '''Return the value of `property` on the bin with whose id is `id`.'''
    return sql(f'SELECT {property} FROM info WHERE id={id}').fetchone()[0]


def get_time_stamps(id):
    return [i[0] for i in sql(f'SELECT time FROM bin{id}').fetchall()]


def fetch_bins():
    bins = [
        {
            prop: get_property(i, prop) for prop in get_columns('info')
        }
        for (i,) in sql('SELECT id FROM info').fetchall()
    ]

    # These keys are not stored in the database, so we update the dicts here
    for i in bins:
        i['cam_connected'] = time() < i['cam_expiry']
        i['latest_litter_count'] = sql(
            f'SELECT litter_count FROM bin{i["id"]} ORDER BY time DESC'
        ).fetchone()[0]

    return bins


if __name__ == '__main__':
    print(cam_expiries())
