import requests
from bs4 import BeautifulSoup
import re
import time

def save_href_values():
    url = "https://interpals.net/app/online?age1=16&age2=110&online=1&offset=0&limit=60&sort=last_login&order=desc&totalResults=2687&itemsStart=1&itemsEnd=60&itemsPerPage=60&page=1&pages=45&offset=60"
    headers = {
        "Host": "interpals.net",
        "Cookie": "",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://interpals.net/app/account",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Te": "trailers"
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
        male_links = soup.find_all("a", class_="male")
        female_links = soup.find_all("a", class_="female")
        href_values = [link.get("href") for link in male_links + female_links]

        # Write href values to a text file
        with open("href_values.txt", "w") as file:
            for href in href_values:
                file.write(href + "\n")

        print("Href values saved to href_values.txt")
    else:
        print("Failed to fetch /app/online content.")

def save_uid_values():
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

def save_thread_ids():
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

def send_messages():
    # Read thread ids from the file
    with open("thread_ids.txt", "r") as file:
        thread_ids = file.readlines()

    headers = {
        "Host": "interpals.net",
        "Cookie": "",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://interpals.net",
        "Referer": "https://interpals.net/pm.php?thread_id=1630376675959788547",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers"
    }

    # Define the payload
    payload_template = "action=send_message&thread={}&message=Hey+there!+Want+to+supercharge+your+sales%3F+Get+into+%22Black+Hat+Marketing%22+for+game-changing+techniques+that'll+turbocharge+your+profits%E2%80%94for+only+%244!+Unveil+forbidden+tactics%2C+real-life+case+studies%2C+and+risk+assessment.+Ready+to+level+up%3F+(cutt+dot+ly%2Fpw6Q3vHq).+Connect+on+LinkedIn+for+free+consultations+and+mentoring+sessions.+Reach+out+anytime%E2%80%94I'm+here+to+help+you+succeed!"

    total_messages = len(thread_ids)
    message_count = 0

    for thread_id in thread_ids:
        # Strip whitespace and newline characters from thread ID
        thread_id = thread_id.strip()
        
        # Replace the thread parameter value in the payload
        payload = payload_template.format(thread_id)

        # Send POST request
        response = requests.post("https://interpals.net/pm.php", headers=headers, data=payload)

        # Update message count
        message_count += 1

        # Print progress
        print(f"{message_count}/{total_messages} message sent")

        # Print the response
        print(response.text)

        # Introduce a delay to avoid overloading the server
        time.sleep(5)

def main():
    while True:
        save_href_values()
        save_uid_values()
        save_thread_ids()
        send_messages()
        print("All tasks completed. Restarting...")
        time.sleep(60)  # Wait for 1 minute before restarting

if __name__ == "__main__":
    main()
