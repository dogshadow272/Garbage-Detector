from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    # Placeholder for database stuff
    dummy_bins = [
        {
            'img_path': 'bins/0.jpg',
            'address': '209 Bishan Street 23',
            'location': 'Staircase 5A'
        },
        {
            'img_path': 'bins/0.jpg',
            'address': '209 Bishan Street 23',
            'location': 'Staircase 5A'
        },
        {
            'img_path': 'bins/0.jpg',
            'address': '209 Bishan Street 23',
            'location': 'Staircase 5A'
        },
        {
            'img_path': 'bins/0.jpg',
            'address': '209 Bishan Street 23',
            'location': 'Staircase 5A'
        },
        {
            'img_path': 'bins/0.jpg',
            'address': '209 Bishan Street 23',
            'location': 'Staircase 5A'
        },
        {
            'img_path': 'bins/0.jpg',
            'address': '209 Bishan Street 23',
            'location': 'Staircase 5A'
        },
    ]

    return render_template('base.html', bins=dummy_bins)


@app.route('/<id>')
def garbage_stats(id):
    return render_template('garbage-stats.html', id=id)


if __name__ == "__main__":
    app.run(debug=True)
