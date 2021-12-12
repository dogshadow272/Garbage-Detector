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
    # (time_stamps, litter_counts)
    litter_data = (
        [0, 1000000000, 2000000000, 3000000000,
            4000000000, 5000000000, 6000000000],
        [0, 2, 5, 8, 8, 1, 1]
    )

    return render_template('garbage-stats.html', bins=dummy_bins, target=id, litter_data=litter_data)


if __name__ == "__main__":
    app.run(debug=True)
