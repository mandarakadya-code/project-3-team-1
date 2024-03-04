from flask import Flask, jsonify, request
from database import get_db_connection
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)

def fetch_annual_emissions_data(start_year, end_year):
    conn = get_db_connection()
    with conn.cursor() as cur:
        query = """
        SELECT Entity, annual_co2_emissions FROM annual_emissions
        WHERE year >= %s AND year <= %s;
        """
        cur.execute(query, (start_year, end_year))
        records = cur.fetchall()
        results = [{"country": record[0], "emission": record[1]} for record in records]
        return results

def fetch_top_countries_data():
    conn = get_db_connection()
    with conn.cursor() as cur:
        # Assuming 'annual_co2_emissions' is a numeric field for total emissions
        query = """
        SELECT Entity AS country, SUM(annual_co2_emissions) AS total_emissions
        FROM annual_emissions
        GROUP BY Entity
        ORDER BY total_emissions DESC
        LIMIT 10;
        """
        cur.execute(query)
        records = cur.fetchall()
        results = [{"country": record[0], "total_emissions": record[1]} for record in records]
        return results

@app.route('/data/annual_emissions')
def annual_emissions_data():
    start_year = request.args.get('start_year', '2010')
    end_year = request.args.get('end_year', '2022')
    data = fetch_annual_emissions_data(start_year, end_year)
    return jsonify(data)

@app.route('/data/top_countries')
def top_countries_data():
    data = fetch_top_countries_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)








