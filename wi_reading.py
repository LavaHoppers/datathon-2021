import requests
import pandas

# r = requests.get("https://www.wisconsin-demographics.com/zip_codes_by_population") population per zip

df = pandas.read_csv('data_formatted.csv')

print(df)