import requests
from bs4 import BeautifulSoup

def main():
    url = "https://interpals.net/app/online"
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

if __name__ == "__main__":
    main()
