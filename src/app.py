from flask import Flask, render_template, request, redirect
import boto3
import db
import time


DELAY = 70

app = Flask(__name__)
s3 = boto3.resource('s3')
bucket_name = 'custom-labels-console-us-east-1-bdd057d599'


@app.route('/')
def index():
    return render_template('base.html', bins=db.fetch_bins(), target=None)


def request_litter_data(id: str) -> str:
    # Get litter counts and their corresponding timestamps
    litter_data = (db.get_time_stamps(id), db.get_litter_counts(id))
    bins = db.fetch_bins()

    # Find the target bin
    for i in bins:
        if i['id'] == id:
            target = i
            break

    return render_template('garbage-stats.html', bins=bins, target=target, litter_data=litter_data)


def receive_camera_input(id: str):
    '''Handle `camera.py`'s POST request.

    Request body shape:
    ```
    {
        'timestamp': int,
        'litterItems': [
            {
                'confidence': float,
                'width': float,
                'height': float,
                'left': float,
                'top': float
            }
        ]
    }
    ```
    '''
    res = request.json
    db.new_litter_entry(id, res['timestamp'], res['litterItems'])


def update_bin_details(id: str):
    # Update address and location of bin
    field, value = request.json['field'], f'"{request.json["value"]}"'
    db.update_bin(id, field, value)


@app.route('/b/<id>', methods=['GET', 'POST', 'PUT'])
def garbage_stats(id) -> str:
    if request.method == 'GET':
        return request_litter_data(id)
    elif request.method == 'POST':
        receive_camera_input(id)
    else:
        update_bin_details(id)

    return ''


@app.route('/newbin')
def new_bin():
    id = db.create_bin()
    return redirect(f'/b/{id}')


@app.route('/b/<id>/delete')
def delete(id):
    db.delete_bin(id)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
