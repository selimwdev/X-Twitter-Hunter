import requests

def main():
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

    for thread_id in thread_ids:
        # Strip whitespace and newline characters from thread ID
        thread_id = thread_id.strip()
        
        # Replace the thread parameter value in the payload
        payload = payload_template.format(thread_id)

        # Send POST request
        response = requests.post("https://interpals.net/pm.php", headers=headers, data=payload)

        # Print the response
        print(response.text)

if __name__ == "__main__":
    main()
