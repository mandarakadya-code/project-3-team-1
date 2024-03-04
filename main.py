from flask import Flask, render_template, jsonify, request
import psycopg2

app = Flask(__name__)

def get_data(category):
    try:
        conn = psycopg2.connect("host=localhost dbname=project_3 user=postgres password=admin")
        cur = conn.cursor()

        if category == 'current':
            cur.execute("SELECT  year_,sum(annual_co2_emissions) as annual_co2_emissions FROM annual_emission WHERE year_ BETWEEN 2010 AND 2022 group by year_ order by year_")
        elif category == 'historic':
            cur.execute("SELECT year_,sum(annual_co2_emissions) as annual_co2_emissions FROM annual_emission WHERE year_ BETWEEN 1960 AND 1980 group by year_ order by year_")
        elif category == 'per-capita':
            cur.execute("SELECT year_,sum(annual_co2_emissions) as annual_co2_emissions FROM per_capita_emissions WHERE year_ BETWEEN 2010 AND 2022 group by year_ order by year_")

        # Fetch all records
        records = cur.fetchall()

        # Close cursor and connection
        cur.close()
        conn.close()

        return records

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL:", error)
        return None

@app.route('/')
def index():
    return render_template('co2_emissions_visualization.html')

@app.route('/data', methods=['GET'])
def serve_data():
    category = request.args.get('category')

    data = get_data(category)

    if data:
        data_dict = []
        for record in data:
            record_dict = {


                'year': record[0],
                'annual_co2_emissions': record[1]
            }
            data_dict.append(record_dict)
        return jsonify(data_dict)
    else:
        return jsonify({'error': 'Failed to fetch data from database'})

if __name__ == '__main__':
    app.run(debug=True)
