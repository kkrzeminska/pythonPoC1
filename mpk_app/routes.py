from flask import render_template, jsonify
from app import app


@app.route('/')
def welcome():
    return render_template("welcome")


# Display data from the database table 'routes' in JSON format
@app.route("/public_transport/city/wroclaw/routes")
def lista_przejazdow(engine):
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM routes")
        rows = [dict(row) for row in result]
        return jsonify(rows)


# Display data from the database table 'cities' in JSON format
@app.route("/cities")
def lista_miast(engine):
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM cities")
        rows = [dict(row) for row in result]
        return jsonify(rows)
