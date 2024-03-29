from flask import Flask, render_template, request, redirect
from config import LITTER_NOTIFICATION_THRESHOLD
import db
import sns


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html', bins=db.fetch_bins(), target=None)


def get_dashboard_page(id: str) -> str:
    return render_template('garbage-stats.html', bins=db.fetch_bins(), target=db.get_full_bin(id))


def receive_camera_input(id: str):
    '''Handle `camera.py`'s POST request.

    Request body shape:
    ```
    {
        'image': str,
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
    bin = db.get_full_bin(id)
    curr_litter_count = len(res['litterItems'])
    prev_litter_count = bin['latest_litter_count'] or 0

    # Send SMS notification if litter crosses threshold
    if prev_litter_count < LITTER_NOTIFICATION_THRESHOLD <= curr_litter_count:
        sns.send_message(
            f'There are {curr_litter_count} litter items around the bin at {bin["address"]}, {bin["location"]}.'
        )

    # Save litter data
    db.new_litter_entry(id, res['timestamp'], res['image'], res['litterItems'])


def update_bin_details(id: str):
    # Update address and location of bin
    field, value = request.json['field'], f'"{request.json["value"]}"'
    db.update_bin(id, field, value)


@app.route('/b/<id>', methods=['GET', 'POST', 'PUT'])
def garbage_stats(id) -> str:
    if request.method == 'GET':
        return get_dashboard_page(id)
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
