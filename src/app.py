from flask import Flask, render_template


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
    bin_data = [
        # (time, litter_count)
        (0.,    0),
        (600.,  2),
        (1200., 5),
        (1800., 8),
        (2400., 8),
        (3000., 12),
        (3600., 1)
    ]

    return render_template('garbage-stats.html', bins=dummy_bins, target_bin=bin_data)


if __name__ == "__main__":
    app.run(debug=True)
