# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 09:51:32 2022

@author: Local User
"""

import pandas as pd
import requests
import json

def download(key, strategy, underlying, from_date, end_date = None):
    
    try:
    
        data_request = requests.get(f"https://qgserver.pythonanywhere.com/download?key={key}&strategy={strategy}&underlying={underlying}&from_date={from_date}&end_date={end_date}")
        # data_request = requests.get(f"http://127.0.0.1:5000/download?key={key}&strategy={strategy}&underlying={underlying}&from_date={from_date}&end_date={end_date}")
    
        if strategy == 'pt_extended':
            
            try:
                formatted_data = pd.DataFrame.from_dict(json.loads(data_request.content))
                formatted_data['datetime'] = pd.to_datetime(formatted_data['datetime'], unit = 'ms')
                formatted_data = formatted_data.set_index('datetime')
            
            except:
                return data_request.text
            
        elif strategy == 'pt' or strategy == 'dca':
            
            try:
                formatted_data = pd.DataFrame.from_dict(json.loads(data_request.content)).set_index('datetime')
            
            except:
                return data_request.text
            
        return formatted_data    

    except:
        return 'Internal server error, please wait or modify parameters. If the error persists, contact: services@qg-indices.com along with your relevant code.'
    