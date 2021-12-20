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


@app.route('/b/<id>', methods=['GET', 'POST', 'PUT'])
def garbage_stats(id):
    if request.method == 'GET':
        # GET dashboard info for this bin
        litter_data = (db.get_time_stamps(id), db.get_litter_counts(id))

        for i in db.fetch_bins():
            if i['id'] == id:
                target = i
                break

        return render_template('garbage-stats.html', bins=db.fetch_bins(), target=target, litter_data=litter_data)
    elif request.method == 'POST':
        # Handle `camera.py`'s POST request
        print(request.form)
        return ''
    else:
        # Update address/location of bin
        field, value = request.json['field'], f'"{request.json["value"]}"'
        db.update_bin(id, field, value)

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
