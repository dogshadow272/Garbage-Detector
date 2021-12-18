from flask import Flask, render_template, request, redirect
import sqlite3
import time
import base64
import boto3


def delete_bin(id: int):
    '''Deletes bin with `id` from database'''
    cur.execute(f'DELETE FROM info WHERE id={id}')
    cur.execute(f'DROP TABLE bin{id}')


def get_columns(table: str) -> list:
    '''Return a list of the columns in `table`.'''
    return [i[1] for i in cur.execute(f'PRAGMA table_info({table})').fetchall()]


def get_property(id: int, property: str):
    '''Return the value of `property` on the bin with whose id is `id`.'''
    return cur.execute(f'SELECT {property} FROM info WHERE id={id}').fetchone()[0]


def create_bin(id: str, img_path: str = 'bins/0.jpg', address: str = '209 Bishan Street 23', location: str = 'Staircase 5A', cam_connected: int = 0):
    '''Add a new bin to the database.'''
    cur.execute(
        f'INSERT INTO info VALUES ({id}, "{img_path}", "{address}", "{location}", {cam_connected})')
    cur.execute(f'CREATE TABLE bin{id} (time, litter_count)')


app = Flask(__name__)
con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()
s3 = boto3.resource('s3')
bucket_name = 'custom-labels-console-us-east-1-bdd057d599'

dummy_bins = [
    {
        j: get_property(i, j) for j in get_columns('info')
    }
    for i in range(1, len(cur.execute('SELECT id FROM info').fetchall()) + 1)
]
for i in dummy_bins:
    i['latest_litter_count'] = cur.execute(
        f'SELECT litter_count FROM bin{i["id"]} ORDER BY time DESC').fetchone()[0]
next_id = len(cur.execute('SELECT id FROM info').fetchall()) + 1


@app.route('/')
def index():
    return render_template('base.html', bins=dummy_bins, target=None)


@app.route('/<int:id>', methods=['POST', 'GET'])
def garbage_stats(id):
    if request.method == 'POST':
        # Recieve POST request for image of bin

        # Convert base64 string to png file
        b64_str = request.json['data']
        print(b64_str)
        # img_file = base64.standard_b64decode(request.json['data'])
        return redirect(f'/{id}')
    else:
        # GET dashboard info for this bin
        time_stamps = [i[0] for i in cur.execute(
            f'SELECT time FROM bin{id}').fetchall()]
        litter_counts = [i[0] for i in cur.execute(
            f'SELECT litter_count FROM bin{id}').fetchall()]
        litter_data = (time_stamps, litter_counts)

        for i in dummy_bins:
            if i['id'] == id:
                target = i
                break

        return render_template('garbage-stats.html', bins=dummy_bins, target=target, litter_data=litter_data)


@app.route('/newbin')
def new_bin():
    global next_id
    create_bin(next_id)
    next_id += 1
    return redirect(f'/{next_id}')


if __name__ == '__main__':
    app.run(debug=True)
