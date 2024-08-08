import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Google Drive file ID
FILE_ID = "1Hu-NQvSLTeWQbYSHKj5UCzMX27rT3zZK"

def main():
    st.title("CSV Explorer")

    @st.cache_data  # This decorator caches the data to improve performance
    def load_data():
        # Construct the direct download URL
        download_url = f"https://drive.google.com/uc?id={FILE_ID}"
        
        # Use requests to get the content
        response = requests.get(download_url)
        response.raise_for_status()  # Raise an exception for bad responses
        
        # Read the CSV content
        return pd.read_csv(StringIO(response.text))

    try:
        df = load_data()
        st.success("Data loaded successfully from Google Drive!")
    except Exception as e:
        st.error(f"Error loading data from Google Drive: {e}")
        st.stop()

    # Display basic information about the dataset
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")

    # Column selection
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect("Select columns to display", all_columns, default=all_columns)

    # Filtering
    st.subheader("Filter Data")
    filter_column = st.selectbox("Select a column to filter", selected_columns)
    unique_values = df[filter_column].unique().tolist()
    selected_values = st.multiselect(f"Select values for {filter_column}", unique_values, default=unique_values)

    # Apply filters and column selection
    filtered_df = df[df[filter_column].isin(selected_values)][selected_columns]

    # Display the filtered dataframe
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Download filtered CSV
    st.download_button(
        label="Download filtered data as CSV",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name="filtered_data.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    main()
