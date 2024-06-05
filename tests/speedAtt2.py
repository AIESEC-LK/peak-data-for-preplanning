import requests
import pandas as pd
import re
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import numpy as np
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Starts =", current_time)

import sys
print ('argument list', sys.argv)
year = int(sys.argv[1])
ey=int(sys.argv[2])
def process_applicants(df):
    # Define the function to extract values
    def extract_applicants_value(row):
        if pd.isna(row['applicants']):
            return row.get('doc_count', np.nan)
        elif isinstance(row['applicants'], dict) and 'value' in row['applicants']:
            return row['applicants']['value']
        else:
            return row.get('doc_count', np.nan)
    
    # Check if 'doc_count' column exists and apply the function
    if 'doc_count' in df.columns:
        df['value'] = df.apply(extract_applicants_value, axis=1)
    else:
        df['value'] = df['applicants'].apply(lambda x: x['value'] if isinstance(x, dict) and 'value' in x else np.nan)
    
    return df

# API endpoint
url = "https://analytics.api.aiesec.org/v2/applications/analyze.json"

def fetch_data(year, month):
    print(f"Sending request for {datetime(year, month, 1).strftime('%B %Y')}")
    # Get the first day of the month
    start_date = datetime(year, month, 1).strftime("%Y-%m-%d")
    # Get the last day of the month
    end_date = datetime(year, month, pd.Period(year=year, month=month, freq='M').days_in_month).strftime("%Y-%m-%d")

    params = {
        "access_token": "0b085db925bfe08eb8b7acbe9c53eefd26fbe6347cb943ac1da87b1204e5c8db",
        "start_date": start_date,
        "end_date": end_date,
        "filters[status]": "Open,Applied,Matched,Accepted,Approved,Realized,Finished,Completed",
        "performance_v3[office_id]": "1585",
        "filters[products]": "Total,iGV,iGTa,iGTe,oGV,oGTa,oGTe"
    }

    # Send GET request
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Convert JSON response to DataFrame
        df = response.json()
        df = pd.DataFrame(df)

        # List of columns to omit
        #ASL
        # columns_to_omit = ['5490', '2188', '2175', '221', '1340', '872', '1821', '2186', '4535', '222', '2204']


        # Turkey 1622

        # columns_to_omit = ['155',
        #                     '156',
        #                     '259',
        #                     '260',
        #                     '502',
        #                     '503',
        #                     '1693',
        #                     '2035',
        #                     '2192',
        #                     '2423',]
        
        # £india 1585
        
        columns_to_omit = ['14',
                                '21',
                                '74',
                                '75',
                                '150',
                                '228',
                                '229',
                                '241',
                                '272',
                                '273',
                                '432',
                                '588',
                                '608',
                                '616',
                                '630',
                                '631',
                                '632',
                                '651',
                                '1393',
                                '1418',
                                '1449',
                                '1490',
                                '1669',
                                '1794',
                                '2012',
                                '2280',
                                '2281',
                                '2282',
                                '2283',
                                '2284',
                                '2289',
                                '2340',
                                '2872',
                                '2873',
                                '4566',
                                '4567',
                                '5787',]

        # Drop the specified columns
        df = df.drop(columns=columns_to_omit,errors='ignore')
        # data = df
        df = df.transpose()
        
        # df = df[['applicants']]

        df = process_applicants(df)
        df = df[['value']]

        print(df)
        df.rename(columns={'value': 'APP'}, inplace=True)

        # New column for status
        df['status'] = df.index.str.split('_').str[1]

        functionRegex = [
            {"name": "Total", "pattern": re.compile("^.*_total$")},
            {"name": "oGV", "pattern": re.compile("^o_.*_[7]$")},
            {"name": "oGTa", "pattern": re.compile("^o_.*_[8]$")},
            {"name": "oGTe", "pattern": re.compile("^o_.*_[9]$")},
            {"name": "iGV", "pattern": re.compile("^i_.*_[7]$")},
            {"name": "iGTa", "pattern": re.compile("^i_.*_[8]$")},
            {"name": "iGTe", "pattern": re.compile("^i_.*_[9]$")},
            {"name": "Old iGV", "pattern": re.compile("^i_.*_[1]$")},
            {"name": "Old oGV", "pattern": re.compile("^o_.*_[1]$")},
            {"name": "Old iGT", "pattern": re.compile("^i_.*_[2]$")},
            {"name": "Old oGT", "pattern": re.compile("^o_.*_[2]$")},
            {"name": "iGE", "pattern": re.compile("^i_.*_[5]$")},
            {"name": "oGE", "pattern": re.compile("^o_.*_[5]$")},
            # # for 'open_i_programme_7'
            {"name": "iGV", "pattern": re.compile("^open_i_.*_[1]$")},
            {"name": "iGV", "pattern": re.compile("^open_i_.*_[7]$")},
            {"name": "iGTa", "pattern": re.compile("^open_i_.*_[8]$")},
            {"name": "iGT Old", "pattern": re.compile("^open_i_.*_[2]$")},
            {"name": "iGE", "pattern": re.compile("^open_i_.*_[5]$")},
            {"name": "iGTe", "pattern": re.compile("^open_i_.*_[9]$")},
            # # for 'open_o_programme_7'
            {"name": "oGV", "pattern": re.compile("^open_o_.*_[1]$")},
            {"name": "oGV", "pattern": re.compile("^open_o_.*_[7]$")},
            {"name": "oGTa", "pattern": re.compile("^open_o_.*_[8]$")},
            {"name": "oGT Old", "pattern": re.compile("^open_o_.*_[2]$")},
            {"name": "oGE", "pattern": re.compile("^open_o_.*_[5]$")},
            {"name": "oGTe", "pattern": re.compile("^open_o_.*_[9]$")},
        ]

        # Function to match pattern and retrieve name
        def get_function_name(index):
            for item in functionRegex:
                if item["pattern"].match(index):
                    return item["name"]
            return None

        # Add 'function' column based on pattern matching
        df['function'] = df.index.map(get_function_name)

        
        # Define the mapping dictionary
        mapping = {
            'oGE': 'oGTa',
            'Old iGT': 'iGTa',
            'Old iGV': 'iGV',
            'oGTe': 'oGTe',
            'oGTa': 'oGTa',
            'oGV': 'oGV',
            'iGTa': 'iGTa',
            'iGV': 'iGV',
            'iGTe': 'iGTe',
            'Old oGT': 'oGTa',
            'Old oGV': 'oGV',
            'iGE': 'iGTa',
            'oGT Old': 'oGTa',
            'iGT Old': 'iGTa',
            'Total': 'Total'
        }

        # Apply the mapping to create the 'function_new' column
        df['function_new'] = df['function'].map(mapping)

        df = df.drop(['open_ogx', 'open_icx','index'], errors='ignore')

        df['Month'] = datetime(year, month, 1).strftime("%B %Y")
        temp_cols=df.columns.tolist()
        new_cols=temp_cols[1:] + temp_cols[0:1]
        df=df[new_cols]
        df = df.drop(df[df.status == "matched"].index)
        df = df.drop(df[df.status == "an"].index)
        return df

    else:
        print(f"Failed to fetch data for {datetime(year, month, 1).strftime('%B %Y')}. Status code:", response.status_code)
        return pd.DataFrame()

# Create ThreadPoolExecutor with max_workers set to number of CPU cores
with ThreadPoolExecutor(max_workers=None) as executor:
    # Execute the fetch_data function for each month from 2016 Jan to 2023 Dec
    results = [executor.submit(fetch_data, year, month)  for month in range(1, 12)]
    # Execute the fetch_data function for each month from 2024 Jan to 2024 Apr

    dfs = [result.result() for result in results]
# dfs=fetch_data(2022,2)
# Concatenate all DataFrames in the list
combined_df = pd.concat(dfs, ignore_index=True)
# dfs.to_csv('final2.csv')
# Save the combined DataFrame to a CSV file
combined_df.to_csv(str(ey)+"-"+str(year)+'.csv', index=False)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Ends =", current_time)
