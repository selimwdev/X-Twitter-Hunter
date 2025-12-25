import re
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor

def extract_emails_from_website(url):
    try:
        with urlopen(url) as response:
            html_content = response.read().decode('utf-8')
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_regex, html_content)
        return emails
    except Exception as e:
        print(f"Error extracting emails from {url}: {e}")
        return []

def process_website(website):
    global processed_websites
    global total_websites
    processed_websites += 1
    print(f"{processed_websites}/{total_websites} processed.", end='\r')
    emails = extract_emails_from_website(website)
    if emails:
        with open("resultemails.txt", "a", encoding="utf-8") as result_file:
            for email in emails:
                result_file.write(email + "\n")

def main():
    global processed_websites
    global total_websites
    websites_file = "websites.txt"
    with open(websites_file, "r", encoding="utf-8") as file:
        websites = file.read().splitlines()
    total_websites = len(websites)
    processed_websites = 0
    with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust the number of workers as needed
        executor.map(process_website, websites)
    print("\nExtraction completed.")

if __name__ == "__main__":
    main()
