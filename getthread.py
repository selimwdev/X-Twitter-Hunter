import requests
import re

def main():
    # Read uid values from the file
    with open("uid_values.txt", "r") as file:
        uid_values = file.readlines()

    headers = {
        "Host": "interpals.net",
        "Cookie": "",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://interpals.net/BeboOoOo?_cs=11",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Te": "trailers"
    }

    # Open a file to save the thread IDs
    with open("thread_ids.txt", "a") as thread_file:
        for uid in uid_values:
            # Construct URL with uid value
            url = f"https://interpals.net/pm.php?action=send&uid={uid.strip()}"

            # Send request
            response = requests.get(url, headers=headers, allow_redirects=False)

            # Check if request was successful
            if response.ok:
                # Extract thread_id parameter value from URL
                thread_id_match = re.search(r'thread_id=(\d+)', response.headers.get("Location", ""))
                if thread_id_match:
                    thread_id = thread_id_match.group(1)
                    thread_file.write(thread_id + '\n')
                else:
                    print(f"Thread ID not found for UID {uid.strip()}.")
            else:
                print(f"Failed to fetch URL for UID {uid.strip()}.")

if __name__ == "__main__":
    main()
