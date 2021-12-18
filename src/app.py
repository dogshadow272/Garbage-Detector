from flask import Flask, render_template, request, redirect
import sqlite3
import time
import base64


def delete_bin(id: int):
    '''Deletes bin with `id` from database'''
    cur.execute(f'ALTER TABLE data DROP bin{id}')
    cur.execute(f'DELETE FROM info WHERE id={id}')


def get_columns(table: str) -> list:
    '''Return a list of the columns in `table`.'''
    return [i[1] for i in cur.execute(f'PRAGMA table_info({table})').fetchall()]


def get_property(id: int, property: str):
    '''Return the value of `property` on the bin with whose id is `id`.'''
    return cur.execute(f'SELECT {property} FROM info WHERE id={id}').fetchone()[0]


def new_bin(id: str, img_path: str = 'bins/0.jpg', address: str = '209 Bishan Street 23', location: str = 'Staircase 5A'):
    '''Add a new bin to the database.'''
    cur.execute(f'ALTER TABLE data ADD bin{id} DEFAULT 0')
    cur.execute(
        f'INSERT INTO info VALUES ({id}, "{img_path}", "{address}", "{location}")')


def new_entry(data: list):
    '''Insert data into SQL database.'''
    cur.execute(
        f'INSERT INTO data VALUES ({time.time()}, {", ".join(map(str, data))})'
    )


app = Flask(__name__)
con = sqlite3.connect('src/db.db', check_same_thread=False)
cur = con.cursor()

dummy_bins = [
    {
        j: get_property(i, j) for j in get_columns('info')
    }
    for i in range(1, len(cur.execute('SELECT id FROM info').fetchall()) + 1)
]
for i in dummy_bins:
    i['latest_litter_count'] = cur.execute(
        f'SELECT bin{i["id"]} FROM data ORDER BY time DESC').fetchone()[0]

@app.route('/')
def index():
    return render_template('base.html', bins=dummy_bins, target=None)


@app.route('/<int:id>', methods=['POST', 'GET'])
def garbage_stats(id):
    if request.method == 'POST':
        # POST image of bin

        # Convert base64 string to png file
        img_file = base64.decodestring(id)

        return redirect(f'/{id}')
    else:
        # GET dashboard info for this bin
        time_stamps = [i[0] for i in cur.execute('SELECT time FROM data')]
        litter_counts = [i[0]
                         for i in cur.execute(f'SELECT bin{id} FROM data')]
        litter_data = (time_stamps, litter_counts)

        for i in dummy_bins:
            if i['id'] == id:
                target = i
                break

        return render_template('garbage-stats.html', bins=dummy_bins, target=target, litter_data=litter_data)


if __name__ == '__main__':
    app.run(debug=True)
