"""
Clean NYC 311 data ( 2010-2024) and save as Parquet for efficient storage.
Creates pre-aggregated CSV exports for D3.js visualizations.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

RAW_NAME = "311_Service_Requests_from_2010_to_Present_20251117.csv"
PARQUET_NAME = "311_curated_ 2010_2024.parquet"
SUMMARY_NAME = "311_curated_ 2010_2024_summary.json"

RAW_PATH = Path(__file__).with_name(RAW_NAME)
OUTPUT_PATH = Path(__file__).with_name(PARQUET_NAME)
SUMMARY_PATH = Path(__file__).with_name(SUMMARY_NAME)
EXPORTS_DIR = Path(__file__).parent / "exports"

START_DATE = pd.Timestamp(" 2010-01-01 00:00:00")  # Changed to  2010
END_DATE = pd.Timestamp("2024-12-31 23:59:59")     # End of 2024
MAX_RESPONSE_HOURS = 24 * 45

# Minimal columns - drop heavy text fields
USECOLS = [
    "Unique Key",
    "Created Date",
    "Closed Date",
    "Agency Name",
    "Complaint Type",
    "Descriptor",
    "Location Type",
    "Incident Zip",
    "City",
    "Status",
    "Borough",
    "Open Data Channel Type",
    "Latitude",
    "Longitude",
]

SEASON_MAP = {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring",
              6: "Summer", 7: "Summer", 8: "Summer", 9: "Fall", 10: "Fall", 11: "Fall"}


def clean_311_data():
    """Load, clean, and export NYC 311 data as Parquet."""
    
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw CSV not found at {RAW_PATH}")
    
    print(f"Loading raw data from {RAW_PATH}...")
    start_time = datetime.now()
    
    # Load with optimized dtypes
    df = pd.read_csv(
        RAW_PATH,
        usecols=USECOLS,
        dtype={
            "Unique Key": "Int64",
            "Agency Name": "category",
            "Complaint Type": "category",
            "Descriptor": "category",
            "Location Type": "category",
            "Status": "category",
            "Borough": "str",
            "Open Data Channel Type": "category",
            "City": "category",
            "Incident Zip": "string",
            "Latitude": "float32",
            "Longitude": "float32",
        },
        parse_dates=["Created Date", "Closed Date"],
    )
    
    rows_read = len(df)
    print(f"Loaded {rows_read:,} rows in {datetime.now() - start_time}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1e9:.2f} GB")
    
    # Rename columns
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    print("\nCleaning data...")
    
    # Parse dates with error handling
    df["created_date"] = pd.to_datetime(df["created_date"], errors='coerce')
    df["closed_date"] = pd.to_datetime(df["closed_date"], errors='coerce')
    
    # Filter:  2010-2024 (inclusive), valid dates only
    df = df[
        df["created_date"].notna() & 
        (df["created_date"] >= START_DATE) &
        (df["created_date"] <= END_DATE)
    ]
    print(f"Filtered to {len(df):,} rows ( 2010-2024 inclusive)")
    
    # Drop missing key fields
    before = len(df)
    df = df.dropna(subset=["complaint_type", "borough", "latitude", "longitude"])
    print(f"Dropped {before - len(df):,} rows missing key fields")
    
    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["unique_key"])
    print(f"Dropped {before - len(df):,} duplicates")
    
    # Clean borough names
    df["borough"] = df["borough"].str.strip().str.upper()
    borough_map = {
        "MANHATTAN": "Manhattan", "BRONX": "Bronx", "BROOKLYN": "Brooklyn",
        "QUEENS": "Queens", "STATEN ISLAND": "Staten Island",
        "RICHMOND / STATEN ISLAND": "Staten Island", "RICHMOND": "Staten Island",
    }
    df["borough"] = df["borough"].replace(borough_map).astype("category")
    
    # Clean zip codes
    df["incident_zip"] = (
        df["incident_zip"]
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .str.zfill(5)
        .where(lambda x: x.str.match(r"^\d{5}$"), pd.NA)
    )
    
    # Round coordinates to 5 decimals (~1m precision) - saves space
    df["latitude"] = df["latitude"].round(5)
    df["longitude"] = df["longitude"].round(5)
    
    # Map channel types
    def map_channel(val):
        if pd.isna(val):
            return "Unknown"
        v = str(val).upper()
        if "PHONE" in v or "CALL" in v:
            return "Phone"
        if "MOBILE" in v or "APP" in v:
            return "Mobile"
        if "WEBSITE" in v or "WEB" in v or "ONLINE" in v:
            return "Web"
        if "EMAIL" in v:
            return "Email"
        return "Other"
    
    df["channel_group"] = df["open_data_channel_type"].apply(map_channel).astype("category")
    
    print("\nDeriving temporal features...")
    
    # Time features
    df["year"] = df["created_date"].dt.year.astype("int16")
    df["month"] = df["created_date"].dt.month.astype("int8")
    df["month_name"] = df["created_date"].dt.month_name().astype("category")
    df["day_of_week"] = df["created_date"].dt.day_name().astype("category")
    df["hour"] = df["created_date"].dt.hour.astype("int8")
    df["season"] = df["month"].map(SEASON_MAP).astype("category")
    df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])
    
    # Response time
    valid_closed = df["closed_date"].notna() & (df["closed_date"] <= END_DATE)
    time_diff = df.loc[valid_closed, "closed_date"] - df.loc[valid_closed, "created_date"]
    response_hours = time_diff.dt.total_seconds() / 3600
    df["response_hours"] = pd.NA
    df.loc[valid_closed, "response_hours"] = response_hours.clip(lower=0, upper=MAX_RESPONSE_HOURS)
    
    # Final column order
    ordered_cols = [
        "unique_key", "created_date", "closed_date",
        "year", "month", "month_name", "day_of_week", "hour", "season", "is_weekend",
        "complaint_type", "descriptor", "status", "agency_name",
        "borough", "city", "incident_zip", "location_type",
        "open_data_channel_type", "channel_group",
        "latitude", "longitude", "response_hours",
    ]
    df = df[[c for c in ordered_cols if c in df.columns]]
    
    print(f"\nFinal memory: {df.memory_usage(deep=True).sum() / 1e9:.2f} GB")
    print(f"Writing Parquet file to {OUTPUT_PATH}...")
    
    # Write Parquet with excellent compression
    df.to_parquet(
        OUTPUT_PATH,
        engine='pyarrow',
        compression='snappy',
        index=False
    )
    
    file_size_mb = OUTPUT_PATH.stat().st_size / 1e6
    print(f"Parquet file: {file_size_mb:.1f} MB")
    
    # Create summary
    summary = {
        "rows_written": len(df),
        "date_range": " 2010-2024 (inclusive)",
        "earliest_date": df["created_date"].min().strftime("%Y-%m-%d"),
        "latest_date": df["created_date"].max().strftime("%Y-%m-%d"),
        "file_size_mb": file_size_mb,
        "boroughs": df["borough"].value_counts().to_dict(),
        "top_complaints": df["complaint_type"].value_counts().head(10).to_dict(),
        "years_covered": sorted(df["year"].unique().tolist()),
    }
    
    with SUMMARY_PATH.open("w") as f:
        json.dump(summary, f, indent=2)
    
    # Create pre-aggregated data for D3
    print("\nCreating D3 CSV exports...")
    create_d3_exports(df)
    
    elapsed = datetime.now() - start_time
    print(f"\nComplete in {elapsed}!")
    print(f"Main file: {OUTPUT_PATH} ({file_size_mb:.1f} MB)")
    print(f"D3 exports: {EXPORTS_DIR}")
    print(f"Summary: {SUMMARY_PATH}")


def create_d3_exports(df: pd.DataFrame):
    """Create small, aggregated CSV files for each D3 visualization."""
    
    EXPORTS_DIR.mkdir(exist_ok=True)
    
    # Q1: Monthly trends by borough (time series) - ORIGINAL, no changes
    monthly = df.groupby([
        df["created_date"].dt.to_period("M").dt.to_timestamp(),
        "borough"
    ]).size().reset_index(name="count")
    monthly.columns = ["date", "borough", "count"]
    monthly.to_csv(EXPORTS_DIR / "q1_monthly_trends.csv", index=False)
    print(f" q1_monthly_trends.csv ({len(monthly):,} rows, {(EXPORTS_DIR / 'q1_monthly_trends.csv').stat().st_size / 1e3:.0f} KB)")
    
    # Q2: Top complaints by borough - ADD YEAR, filter zeros
    complaints_by_borough = df.groupby(["year", "borough", "complaint_type"]).size().reset_index(name="count")
    complaints_by_borough = complaints_by_borough[complaints_by_borough["count"] > 0]  # Remove zero counts
    complaints_by_borough = complaints_by_borough.sort_values(["year", "borough", "count"], ascending=[True, True, False])
    complaints_by_borough.to_csv(EXPORTS_DIR / "q2_complaints_by_borough.csv", index=False)
    print(f" q2_complaints_by_borough.csv ({len(complaints_by_borough):,} rows, {(EXPORTS_DIR / 'q2_complaints_by_borough.csv').stat().st_size / 1e3:.0f} KB)")
    
    # Q3: Heatmap data (hour x day of week) - ORIGINAL, no changes
    top_complaints = df["complaint_type"].value_counts().head(20).index
    heatmap_data = df[df["complaint_type"].isin(top_complaints)].groupby([
        "complaint_type", "day_of_week", "hour"
    ]).size().reset_index(name="count")
    heatmap_data.to_csv(EXPORTS_DIR / "q3_hourly_patterns.csv", index=False)
    print(f" q3_hourly_patterns.csv ({len(heatmap_data):,} rows, {(EXPORTS_DIR / 'q3_hourly_patterns.csv').stat().st_size / 1e3:.0f} KB)")
    
    # Q4: Geographic data - ADD YEAR, filter zeros
    geo_agg = df.groupby(["year", "incident_zip", "borough"]).agg({
        "latitude": "mean",
        "longitude": "mean",
        "response_hours": "median",
        "unique_key": "count"
    }).reset_index()
    geo_agg.columns = ["year", "zip", "borough", "lat", "lng", "median_response_hours", "count"]
    geo_agg = geo_agg[geo_agg["count"] > 0]  # Remove zero counts
    geo_agg = geo_agg.dropna(subset=["median_response_hours"])
    geo_agg.to_csv(EXPORTS_DIR / "q4_response_by_location.csv", index=False)
    print(f" q4_response_by_location.csv ({len(geo_agg):,} rows, {(EXPORTS_DIR / 'q4_response_by_location.csv').stat().st_size / 1e3:.0f} KB)")
    
    # Q5: Channel usage by complaint type - ADD YEAR, filter zeros
    channels = df.groupby(["year", "complaint_type", "channel_group"]).size().reset_index(name="count")
    channels = channels[channels["count"] > 0]  # Remove zero counts
    channels = channels.sort_values(["year", "complaint_type", "count"], ascending=[True, True, False])
    channels.to_csv(EXPORTS_DIR / "q5_channels_by_complaint.csv", index=False)
    print(f" q5_channels_by_complaint.csv ({len(channels):,} rows, {(EXPORTS_DIR / 'q5_channels_by_complaint.csv').stat().st_size / 1e3:.0f} KB)")
    
    # Yearly summary
    yearly = df.groupby("year").agg({
        "unique_key": "count",
        "response_hours": "median"
    }).reset_index()
    yearly.columns = ["year", "total_requests", "median_response_hours"]
    yearly.to_csv(EXPORTS_DIR / "yearly_summary.csv", index=False)
    print(f" yearly_summary.csv ({len(yearly):,} rows, {(EXPORTS_DIR / 'yearly_summary.csv').stat().st_size / 1e3:.0f} KB)")


if __name__ == "__main__":
    clean_311_data()