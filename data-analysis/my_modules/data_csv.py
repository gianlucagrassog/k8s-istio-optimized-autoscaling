import logging
import pandas as pd

def read_data(filename):
    try:
        df = pd.read_csv(filename, header=0)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        logging.error(f"Error reading file {filename}: {e}")
