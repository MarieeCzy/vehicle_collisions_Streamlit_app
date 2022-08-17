import pandas as pd
import requests

url = 'https://data.cityofnewyork.us/resource/h9gi-nx95.json'
r = requests.get(url)

json = r.json()

#data frame
df = pd.DataFrame(json)
