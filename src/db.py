import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
sql = con.cursor().execute


def cam_timestamps():
    camera_timestamps = [i[0] for i in sql('SELECT cam_timestamp FROM info')]
    return camera_timestamps


def create_bin(
        id: int,
        img_path: str = 'bins/0.jpg',
        address: str = '209 Bishan Street 23',
        location: str = 'Staircase 5A',
        cam_connected: int = 0,
        cam_timestamp: int = 0):
    '''Add a new bin to the database.'''

    sql(f'INSERT INTO info VALUES ({id}, "{img_path}", "{address}", "{location}", {cam_connected}, {cam_timestamp})')
    sql(f'CREATE TABLE bin{id} (time, litter_count)')
    sql(f'INSERT INTO bin{id} VALUES (0, 0)')


def change_info(id: int, property: str, value):
    sql(f'UPDATE info SET {property}={value} WHERE id={id}')


def delete_bin(id: int):
    '''Deletes bin with `id` from database'''
    sql(f'DELETE FROM info WHERE id={id}')
    sql(f'DROP TABLE bin{id}')


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


def fetch_data():
    bins = [
        {
            j: get_property(i, j) for j in get_columns('info')
        }
        for i in range(1, len(sql('SELECT id FROM info').fetchall()) + 1)
    ]
    for i in bins:
        i['latest_litter_count'] = sql(
            f'SELECT litter_count FROM bin{i["id"]} ORDER BY time DESC').fetchone()[0]

    return bins


def save_changes():
    con.commit()


if __name__ == '__main__':
    print(cam_timestamps())
