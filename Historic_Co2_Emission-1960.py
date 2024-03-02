import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Read the CSV file
file_path = r'C:\Users\r_mat\OneDrive\Desktop\Classwork\Project_03\Resources\annual-co-emissions-by-region.csv'
Co2 = pd.read_csv(file_path)

# Display basic information about the DataFrame
print(Co2.info())

# Drop the 'Code' column
Co2.drop('Code', axis=1, inplace=True)

# Rename the 'annual_co2_emissions' column to 'A_Co2_emissions'
Co2.rename(columns={'annual_co2_emissions': 'A_Co2_emissions'}, inplace=True)

# Display the first few rows of the DataFrame
print(Co2.head())

# Display unique values in 'Year' and 'Entity' columns
print(Co2['Year'].unique())
print(Co2['Entity'].unique())

# Rename the 'Entity' column to 'Country'
Co2.rename(columns={'Entity': 'Country'}, inplace=True)

# Display updated information about the DataFrame
print(Co2.info())

# Filter out rows with negative 'A_Co2_emissions'
condition = Co2['A_Co2_emissions'] >= 0
df = Co2[condition]

# Create subsets for different time periods
p1 = df['Year'] <= 1959
Period_1 = df[p1]

P2_Y1 = df['Year'] <= 1980
P2_Y2 = df['Year'] > 1959
Period_2 = df[P2_Y1 & P2_Y2]

# Display the first few rows of each period
print(Period_1.head())
print(Period_2.head())

# Group by country and sum the 'A_Co2_emissions' for the top 65 countries
top_countries = Period_2.groupby('Country')['A_Co2_emissions'].sum().sort_values(ascending=False)[:65]

# Plot a bar chart for the top 10 emitting countries from 1960 to 1980
sns.set_style('darkgrid')
plt.figure(figsize=(10, 6))  # Optional: Adjust the figure size
chart = top_countries[1:10].plot(kind='bar')
plt.title('Top 10 Countries in emitting Co2 from 1960 to 1980', fontweight='bold')
plt.ylabel('Co2 Emissions')

# Create a folder for saving the output if it doesn't exist
output_folder = 'output_folder'
os.makedirs(output_folder, exist_ok=True)

# Save the plot to a file (e.g., PNG format)
output_file_path = os.path.join(output_folder, 'top_countries_co2_emissions_plot.png')
plt.savefig(output_file_path, bbox_inches='tight')

# Display the plot
plt.show()

# Display the top 10 emitting years from 1960 to 1980
print(Period_2.groupby('Year')['A_Co2_emissions'].sum().sort_values(ascending=False)[:10])

# Plot a bar chart for Co2 emissions from 1960 to 1980
sns.set_style('darkgrid')
plt.figure(figsize=(10, 6))  # Optional: Adjust the figure size
chart = Period_2.groupby('Year')['A_Co2_emissions'].sum().sort_values(ascending=False).plot(kind='bar')
plt.title('Emitting Co2 from 1960 to 1980', fontweight='bold')
plt.ylabel('Co2 Emissions')

# Create a folder for saving the output if it doesn't exist
output_folder = 'output_folder'
os.makedirs(output_folder, exist_ok=True)

# Save the plot to a file (e.g., PNG format)
output_file_path = os.path.join(output_folder, 'co2_emissions_plot.png')
plt.savefig(output_file_path, bbox_inches='tight')

# Display the plot
plt.show()

