from flask import Flask, jsonify
from database import get_db_connection
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def fetch_top_countries_data():
    conn = get_db_connection()
    with conn.cursor() as cur:
        query = """
        SELECT Entity AS country, annual_co2_emissions AS total_emissions
        FROM annual_emissions
        WHERE year = '2022'
        AND Entity NOT LIKE '%(GCP)%'
        AND Entity NOT LIKE '%(excl. China and India)%'
        AND Entity NOT LIKE '%(%'
        AND Entity NOT LIKE '%income%'
        AND Entity NOT LIKE 'Africa' -- Exclude the continent Africa
        AND Entity NOT LIKE 'South America' -- Exclude the continent South America
        AND Entity NOT IN ('World', 'High-income countries', 'OECD', 'Non-OECD', 'Asia', 'Europe', 'North America', 'European Union')
        ORDER BY total_emissions DESC
        LIMIT 10;
        """
        cur.execute(query)
        records = cur.fetchall()
        results = [{"country": record[0], "emissions": record[1]} for record in records]
        return results

@app.route('/data/top_countries')
def top_countries_data():
    data = fetch_top_countries_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)










