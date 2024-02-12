import argparse
import logging
import os
import re
import requests
import google_play_scraper as gps

APP_ID = "jp.enish.gotopazu"

def fetch_latest_version(app_id):
    try:
        app_details = gps.app(app_id)
        return app_details['version']
    except Exception as e:
        logging.error(f"Failed to fetch the latest version for {app_id}: {e}", exc_info=True)
        return None

def download_files(url, version, output_dir, file_list):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    downloaded_files = 0
    total_files = len(file_list)

    for i, file in enumerate(file_list):
        file_url = f"{url}/{file}"
        print(f"Downloading {i+1}/{total_files}: {file}")
        try:
            response = requests.get(file_url, stream=True)
            with open(os.path.join(output_dir, file), 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            downloaded_files += 1
        except Exception as e:
            logging.error(f"Failed to download {file}: {e}", exc_info=True)
    
    print(f"All files are downloaded: {downloaded_files}/{total_files}")

def main():
    parser = argparse.ArgumentParser(description='Download files for a given app version.')
    # Optional path argument
    parser.add_argument('--path', '-p', type=str, default=os.getcwd(),
                        help='Path where the files will be downloaded. Defaults to the current directory.')
    # Optional version argument
    parser.add_argument('--version', '-v', type=str, default='',
                        help='App version to download. If not specified, fetches the latest version.')
    
    args = parser.parse_args()
    output_dir = args.path
    specified_version = args.version

    # Fetch the latest version if not specified
    version = specified_version if specified_version else fetch_latest_version(APP_ID)
    if version:
        print(f"Version to download: {version}")
        version = version.replace(".", "_")
        output_dir = os.path.join(output_dir, f"v{version}")
        url = f"https://www-cancer.enish-games.com/v{version}/resource/list/Android"
        response = requests.get(url).text
        file_names = set(re.findall(r"[0-9a-f]{32}", response))

        existing_files = set()
        for subdir, dirs, files in os.walk(output_dir):
            for file in files:
                if file in file_names:
                    existing_files.add(file)

        file_list = list(file_names - existing_files)
        print(f"Number of files to download: {len(file_list)}")
        if len(file_list) > 0:
            download_files(url, version, output_dir, file_list)
        else:
            print("No new files to download.")
    else:
        print("Failed to get the specified version.")

if __name__ == "__main__":
    main()