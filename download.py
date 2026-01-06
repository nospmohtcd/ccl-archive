# Ran this twice, once to collect 1991 through 1999 then
# again for 2000 through 2025
# You can edit line #46:
# years = [str(y) for y in range(91, 100)]

import os
import requests
import time

# Base configuration
BASE_ROOT = "https://server.ccl.net/cca/archived-messages/"
SAVE_DIR = os.path.join(os.getcwd(), "CCL_Archive")

def download_specific_file(year, month, day, suffix=""):
    """Constructs the URL and downloads the file if it exists."""
    # Construct the filename (e.g., '11' or '11.bak')
    filename = f"{day}{suffix}"
    
    # Construct the full URL
    url = f"{BASE_ROOT}{year}/{month}/{filename}"
    
    # Path to save on your Mac: CCL_Archive/91/01/11.txt
    local_folder = os.path.join(SAVE_DIR, year, month)
    local_file_path = os.path.join(local_folder, f"{filename}.txt")

    try:
        # Check if file exists on server
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            # Create folder only if we found a valid file
            os.makedirs(local_folder, exist_ok=True)
            
            with open(local_file_path, 'wb') as f:
                f.write(response.content)
            print(f"Successfully saved: {year}/{month}/{filename}")
            return True
        return False
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return False

def main():
    # Years: A to B 
    years = [str(y).zfill(2) for y in range(00, 26)]
    # Months: 01 to 12
    months = [str(m).zfill(2) for m in range(1, 13)]
    # Days: 01 to 31
    days = [str(d).zfill(2) for d in range(1, 32)]

    print(f"Starting targeted download into: {SAVE_DIR}")

    for year in years:
        for month in months:
            print(f"Checking Year {year}, Month {month}...")
            for day in days:
                # Try the standard file (e.g., /91/01/11)
                download_specific_file(year, month, day)
                
                # Try the .bak version (e.g., /91/01/11.bak)
                download_specific_file(year, month, day, suffix=".bak")
                
                # Small pause to avoid being blocked
                time.sleep(0.05)

if __name__ == "__main__":
    main()
