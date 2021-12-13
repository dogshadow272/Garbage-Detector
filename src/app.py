from flask import Flask, render_template
from math import sin  # For dummy data

app = Flask(__name__)

# Placeholder for database stuff
dummy_bins = [
    {
        'id': i,
        'img_path': 'bins/0.jpg',
        'address': '209 Bishan Street 23',
        'location': 'Staircase 5A'
    }
    for i in range(10)
]


@app.route('/')
def index():
    return render_template('base.html', bins=dummy_bins)


@app.route('/<int:id>')
def garbage_stats(id):
    # Placeholder for SQLite stuff
    # (time_stamps, litter_counts)
    dummy_data = (
        [t * 600000 for t in range(672)],
        [int(8 * sin(.01 * x) + sin(.1 * x) + 9) for x in range(672)]
    )

    return render_template('garbage-stats.html', bins=dummy_bins, target=id, litter_data=dummy_data)


if __name__ == "__main__":
    app.run(debug=False)
