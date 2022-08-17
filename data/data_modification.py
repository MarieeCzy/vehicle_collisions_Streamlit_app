import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import app
import pandas as pd

def short_raw_data(nrows):
    df = pd.read_csv(app.DATA_URL, nrows=nrows)
    df.to_csv('Motor_Vehicle_Collisions_-_Crashes_min.csv', index=False)

    
short_raw_data(90000)