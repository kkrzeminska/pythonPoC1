from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine
from functions import download_zip, create_cities_csv


# Create a Flask application object
app = Flask(__name__)
# Create SQLite database engine
engine = create_engine('sqlite:///database.db', echo=True)


@app.route('/')
def welcome():
    return render_template("welcome")


# Display data from the database table 'routes' in JSON format
@app.route("/public_transport/city/wroclaw/routes")
def lista_przejazdow():
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM routes")
        rows = [dict(row) for row in result]
        return jsonify(rows)


# Display data from the database table 'cities' in JSON format
@app.route("/cities")
def lista_miast():
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM cities")
        rows = [dict(row) for row in result]
        return jsonify(rows)


download_zip(engine)
create_cities_csv(engine)

if __name__ == '__main__':
    app.run()
