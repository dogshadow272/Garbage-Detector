import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()


def create_bin(id: str, img_path: str = 'bins/0.jpg', address: str = '209 Bishan Street 23', location: str = 'Staircase 5A', cam_connected: int = 0):
    '''Add a new bin to the database.'''
    cur.execute(f'INSERT INTO info VALUES ({id}, "{img_path}", "{address}", "{location}", {cam_connected})')
    cur.execute(f'CREATE TABLE bin{id} (time, litter_count)')
    cur.execute(f'INSERT INTO bin{id} VALUES (0, 0)')


def delete_bin(id: int):
    '''Deletes bin with `id` from database'''
    cur.execute(f'DELETE FROM info WHERE id={id}')
    cur.execute(f'DROP TABLE bin{id}')


def get_columns(table: str) -> list:
    '''Return a list of the columns in `table`.'''
    return [i[1] for i in cur.execute(f'PRAGMA table_info({table})').fetchall()]


def get_next_id():
    return len(cur.execute('SELECT id FROM info').fetchall()) + 1


def get_litter_counts(id):
    return [i[0] for i in cur.execute(f'SELECT litter_count FROM bin{id}').fetchall()]


def get_property(id: int, property: str):
    '''Return the value of `property` on the bin with whose id is `id`.'''
    return cur.execute(f'SELECT {property} FROM info WHERE id={id}').fetchone()[0]


def get_time_stamps(id):
    return [i[0] for i in cur.execute(f'SELECT time FROM bin{id}').fetchall()]


def fetch_data():
    bins = [
        {
            j: get_property(i, j) for j in get_columns('info')
        }
        for i in range(1, len(cur.execute('SELECT id FROM info').fetchall()) + 1)
    ]
    for i in bins:
        i['latest_litter_count'] = cur.execute(
            f'SELECT litter_count FROM bin{i["id"]} ORDER BY time DESC').fetchone()[0]
    
    return bins

def save_changes():
    con.commit()