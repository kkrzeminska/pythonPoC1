import requests
import zipfile
import os
import csv


# Download the current timetable
def download_zip(engine):
    url = "https://www.wroclaw.pl/open-data/87b09b32-f076-4475-8ec9-6020ed1f9ac0/OtwartyWroclaw_rozklad_jazdy_GTFS.zip"
    response = requests.get(url)

    with open("OtwartyWroclaw_rozklad_jazdy_GTFS.zip", "wb") as file:
        file.write(response.content)

    zip_ref = zipfile.ZipFile("OtwartyWroclaw_rozklad_jazdy_GTFS.zip", "r")
    zip_name = zip_ref.filename.split(".")[0]
    zip_ref.extractall(zip_name)
    zip_ref.close()
    # Open routes.txt file
    with open(os.path.abspath(os.path.join("OtwartyWroclaw_rozklad_jazdy_GTFS", "routes.txt")), "r",
              encoding="UTF-8") as f:
        # Read column headers
        reader = csv.reader(f, delimiter=",")
        headers = next(reader)

        # Create a 'routes' table in the database with columns named after those read from a txt file
        with engine.connect() as conn:
            query = f"DROP TABLE IF EXISTS routes"
            conn.execute(query)

            query = f"CREATE TABLE routes ({','.join(headers)})"
            conn.execute(query)
            for row in reader:
                values = ",".join(f'"{col}"' for col in row)
                query = f"INSERT INTO routes ({','.join(headers)}) VALUES ({values})"
                conn.execute(query)


# Create 'cities' file
def create_cities_csv(engine):
    csv_path = 'OtwartyWroclaw_rozklad_jazdy_GTFS/cities.csv'
    cities = [
        (1, 'Wrocław')
    ]

    # Save data to a CSV file
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['city_id', 'city_name'])
        writer.writerows(cities)

    # Save data to a SQLite database
    with engine.connect() as conn:
        query = f"CREATE TABLE IF NOT EXISTS cities (city_id INTEGER, city_name TEXT)"
        conn.execute(query)

        conn.execute("DELETE FROM cities")
        query = f"INSERT INTO cities VALUES (1, 'Wrocław')"
        conn.execute(query)
