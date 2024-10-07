from pywebcopy import save_webpage
import os

def download_website(url, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

        # Configure pywebcopy
        kwargs = {
            'project_name': url.split('//')[-1],
            'bypass_robots': True,
            'debug': True,
            'open_in_browser': False,
            'delay': 1,
            'threaded': False,
        }

        # Download the website
        save_webpage(
            url=url,
            project_folder=output_folder,
            **kwargs
        )

        print(f"Finished downloading: {url}")

# List of websites to download
websites = [
    # 'https://apple.com',
    # 'https://python.org',
    # 'https://github.com'
    # 'https://www.sunshinepokerleague.com/'
    'https://hockeystack.com',
]

# Base output folder
base_output_folder = 'downloaded_websites'

# Download each website
for site in websites:
    site_folder = os.path.join(base_output_folder, site.split('//')[-1])
    download_website(site, site_folder)