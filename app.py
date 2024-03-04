from flask import Flask, send_file
from io import BytesIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Read the CSV file
file_path = r'C:\Users\r_mat\OneDrive\Desktop\Classwork\Project_03\Resources\annual-co-emissions-by-region.csv'
Co2 = pd.read_csv(file_path)

# Drop the 'Code' column
Co2.drop('Code', axis=1, inplace=True)

# Rename the 'annual_co2_emissions' column to 'A_Co2_emissions'
Co2.rename(columns={'annual_co2_emissions': 'A_Co2_emissions'}, inplace=True)

# Rename the 'Entity' column to 'Country'
Co2.rename(columns={'Entity': 'Country'}, inplace=True)

# Filter out rows with negative 'A_Co2_emissions'
condition = Co2['A_Co2_emissions'] >= 0
df = Co2[condition]

# Create subsets for different time periods
p1 = df['Year'] <= 1959
Period_1 = df[p1]

P2_Y1 = df['Year'] <= 1980
P2_Y2 = df['Year'] > 1959
Period_2 = df[P2_Y1 & P2_Y2]

# Group by country and sum the 'A_Co2_emissions' for the top 65 countries
top_countries = Period_2.groupby('Country')['A_Co2_emissions'].sum().sort_values(ascending=False)[:65]

# Function to save and return the plot as bytes
def save_and_return_plot(data, title):
    sns.set_style('darkgrid')
    plt.figure(figsize=(10, 6))  # Optional: Adjust the figure size
    chart = data.plot(kind='bar')
    plt.title(title, fontweight='bold')
    plt.ylabel('Co2 Emissions')

    # Save the plot to bytes
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png', bbox_inches='tight')
    plt.close()

    return img_bytes.getvalue()

@app.route('/')
def home():
    return """
    <h1>Welcome to the Historic Co2 Emission API!</h1>
    <p>Explore the following plots:</p>
    <ul>
        <li><a href="/top_countries_plot">Top 10 Countries Plot</a></li>
        <li><a href="/co2_emissions_plot">Co2 Emissions Plot</a></li>
    </ul>
    """

@app.route('/top_countries_plot')
def top_countries_plot():
    # Group by country and sum the 'A_Co2_emissions' for the top 10 countries
    top_countries_data = top_countries[1:10]

    img_bytes = save_and_return_plot(top_countries_data, 'Top 10 Countries in emitting Co2 from 1960 to 1980')

    return send_file(BytesIO(img_bytes),
                     download_name='top_countries_co2_emissions_plot.png',
                     mimetype='image/png')

@app.route('/co2_emissions_plot')
def co2_emissions_plot():
    # Group by year and sum the 'A_Co2_emissions' for the top 10 years
    emissions_by_year_data = Period_2.groupby('Year')['A_Co2_emissions'].sum().sort_values(ascending=False)

    img_bytes = save_and_return_plot(emissions_by_year_data, 'Emitting Co2 from 1960 to 1980')

    return send_file(BytesIO(img_bytes),
                     download_name='co2_emissions_plot.png',
                     mimetype='image/png')

if __name__  == '__main__':
    app.run()
