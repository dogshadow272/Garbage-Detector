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
    return render_template('base.html', bins=db.fetch_data(), target=None)


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
        litter_data = (db.get_time_stamps(id), db.get_litter_counts(id))

        for i in db.fetch_data():
            if i['id'] == id:
                target = i
                break

        return render_template('garbage-stats.html', bins=db.fetch_data(), target=target, litter_data=litter_data)


@app.route('/newbin')
def new_bin():
    db.create_bin(db.get_next_id())
    db.save_changes()
    return redirect(f'/{db.get_next_id()-1}')


@app.route('/<int:id>/newcam')
def new_cam(id):
    # Update DB here
    db.change_info(id, 'cam_connected', 1)
    db.change_info(id, 'cam_timestamp', time.time() + DELAY)
    db.save_changes()
    return redirect(f'/{id}')


@app.route('/<int:id>/delete')
def delete(id):
    # Update DB here

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
