
import requests
import zipfile
import io
import os
from dashboard.views_pages import toolkit as tk
def download_binance_data():

    def download_and_unzip(url, extract_to='.'):
        """
        Downloads a ZIP file from the given URL and extracts its contents to the specified directory.
        The file is handled entirely in memory without writing to disk.
        
        Args:
            url (str): The URL of the ZIP file to download.
            extract_to (str): The directory path where the contents will be extracted.
        """
        # Ensure the extraction directory exists
        os.makedirs(extract_to, exist_ok=True)
        
        # Download the ZIP file content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Read the ZIP file content into memory
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            # Extract all contents to the specified directory
            zip_file.extractall(path=tk.bot_tmp_folder_path)

    # Example usage
    # List of URLs pointing to ZIP files
    url_list = [

        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-01.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-02.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-03.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-04.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-05.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-06.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-07.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-08.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-09.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-10.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-11.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2024-12.zip",


        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2025-01.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2025-02.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2025-03.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2025-04.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2025-05.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2025-06.zip",
        # "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2025-07.zip",
        "https://data.binance.vision/data/spot/monthly/klines/ETHUSDC/1s/ETHUSDC-1s-2025-08.zip",


    ]
    # Download and extract each ZIP file
    for url in url_list:
        print(f"Downloading and extracting {url}...")
        download_and_unzip(url, extract_to="./extracted_files")
    print("All files have been downloaded and extracted.")   