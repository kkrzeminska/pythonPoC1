from flask import Flask
from sqlalchemy import create_engine
from functions import download_zip, create_cities_csv


# Create a Flask application object
app = Flask(__name__)
# Create SQLite database engine
engine = create_engine('sqlite:///database.db', echo=True)

download_zip(engine)
create_cities_csv(engine)

if __name__ == '__main__':
    app.run()

