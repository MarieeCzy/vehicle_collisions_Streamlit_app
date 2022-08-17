import sys
import os.path
from typing import NoReturn
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import app
import pandas as pd

def short_raw_data(nrows):
    df = pd.read_csv(app.DATA_URL, nrows=nrows)
    #excelWriter = pd.ExcelWriter(f'{app.DATA_URL[:-3]}_min.csv')
    df.to_csv('Motor_Vehicle_Collisions_-_Crashes_min.csv', index=False)
    #excelWriter.save()
    #excelWriter.close()
    
short_raw_data(90000)