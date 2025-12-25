import requests
from bs4 import BeautifulSoup
import re

def main():
    # Open the file to save uid values in append mode
    with open("uid_values.txt", "a") as uid_file:
        # Read href values from the file
        with open("href_values.txt", "r") as file:
            href_values = file.readlines()

        headers = {
            "Host": "interpals.net",
            "Cookie": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://interpals.net/app/online",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"
        }

        for href in href_values:
            # Construct URL
            url = f"https://interpals.net{href.strip()}"

            # Send request
            response = requests.get(url, headers=headers)

            # Check if request was successful
            if response.ok:
                # Parse HTML response
                soup = BeautifulSoup(response.content, "html.parser")
                # Find <a> tags with title containing "Write to" and get their href values
                write_to_links = soup.find_all("a", title=lambda title: title and "Write to" in title)
                for link in write_to_links:
                    href_value = link.get("href")
                    # Extract uid parameter value using regex
                    uid_value = re.search(r'uid=(\d+)', href_value)
                    if uid_value:
                        uid = uid_value.group(1)
                        print(uid)
                        # Write uid to file
                        uid_file.write(uid + "\n")
                        # Flush the buffer to save immediately
                        uid_file.flush()
                    else:
                        print("UID value not found.")
            else:
                print(f"Failed to fetch {url}.")

if __name__ == "__main__":
    main()
