import pandas as pd

# Load the raw dataset
df = pd.read_csv("311_Service.csv", low_memory=False)

rename_dict = {
    'Unique Key': 'unique_key',
    'Created Date': 'created_date',
    'Agency': 'agency',
    'Agency Name': 'agency_name',
    'Complaint Type': 'complaint_type',
    'Descriptor': 'descriptor',
    'Borough': 'borough',
    'City': 'city',
    'Open Data Channel Type': 'open_data_channel_type',
    'Latitude': 'latitude',
    'Longitude': 'longitude',
}

df = df.rename(columns=rename_dict)

# Keep useful columns
keep_cols = [
    'unique_key', 'created_date',
    'complaint_type', 'descriptor',
    'agency', 'agency_name',
    'borough', 'city',
    'latitude', 'longitude',
    'open_data_channel_type'
]
df = df[keep_cols]

# convert the 'created_date' column to datetime
df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')

# drop rows with invalid or missing created_date
df = df.dropna(subset=['created_date'])

# clean up text columns
for c in ['complaint_type', 'descriptor', 'agency', 'agency_name', 'borough', 'city']:
    df[c] = df[c].astype(str).str.strip().str.title()

# standardize borough name
df['borough'] = df['borough'].replace({
    'Manhattan': 'MANHATTAN',
    'Bronx': 'BRONX',
    'Brooklyn': 'BROOKLYN',
    'Queens': 'QUEENS',
    'Staten Island': 'STATEN ISLAND',
    'Nan': 'UNKNOWN',
    '': 'UNKNOWN'
})

# remove duplicate records by unique_key
df = df.drop_duplicates(subset=['unique_key'])

# drop rows with no latitude or longitude
df = df.dropna(subset=['latitude', 'longitude'])

# save the cleaned dataset and export to a new CSV file
df.to_csv("311_clean.csv", index=False)

print("Done")
