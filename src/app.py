from flask import Flask, render_template
import sqlite3
import time


def get_columns(table: str) -> list:
    '''Return a list of the columns in `table`.'''
    return [i[1] for i in cur.execute(f'PRAGMA table_info({table})').fetchall()]


def get_property(id: int, property: str):
    '''Return the value of `property` on the bin with whose id is `id`.'''
    return cur.execute(f'SELECT {property} FROM info WHERE id={id}').fetchone()[0]


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


@app.route('/')
def index():
    return render_template('base.html', bins=dummy_bins)


@app.route('/<int:id>')
def garbage_stats(id):
    time_stamps = [i[0] for i in cur.execute('SELECT time FROM data')]
    litter_counts = [i[0] for i in cur.execute(f'SELECT bin{id} FROM data')]
    litter_data = (time_stamps, litter_counts)

    return render_template('garbage-stats.html', bins=dummy_bins, target=id, litter_data=litter_data)


if __name__ == '__main__':
    app.run(debug=True)
