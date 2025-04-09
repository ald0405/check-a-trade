# Load and clean function
import pandas as pd
import numpy as np

def load_and_clean(path):
    df = pd.read_csv(path)
    
    # Step 1: Clean column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Step 2: Convert columns with 'date' or 'time' in their names to datetime (if not timedelta columns)
    for col in df.columns:
        if any(x in col for x in ['date', 'datetime']) and col not in ['handle_time', 'speed_of_answer', 'accept_time']:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Step 3: Specific time duration columns to convert to minutes
    time_cols = ['handle_time', 'speed_of_answer', 'accept_time']
    for col in time_cols:
        if col in df.columns:
            df[col] = df[col].replace('-', np.nan)  # Replace dash placeholders
            df[col] = pd.to_timedelta(df[col], errors='coerce')  # Parse as timedelta
            df[col] = df[col].dt.total_seconds() / 60  # Convert to minutes

    return df
