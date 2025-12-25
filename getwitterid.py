import requests

def get_twitter_id(username):
    try:
        headers = {
            'Host': 'twitvd.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://twitvd.com/twitter-id/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Te': 'trailers'
        }

        response = requests.get(f"https://twitvd.com/twuserid.php?username={username}", headers=headers)
        
        if response.status_code == 200:
            json_data = response.json()
            if json_data['success']:
                return json_data['data']['user_id']
            else:
                print(f"Failed to get Twitter ID for {username}. Error: {json_data['error']}")
                return None
        else:
            print(f"Failed to get Twitter ID for {username}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    usernames_file = "usernames.txt"
    output_file = "twitter_ids.txt"

    with open(usernames_file, "r") as file:
        usernames = file.read().splitlines()

    with open(output_file, "w") as outfile:
        total_count = len(usernames)
        for count, username in enumerate(usernames, 1):
            twitter_id = get_twitter_id(username)
            if twitter_id:
                outfile.write(f"{twitter_id}\n")
                print(f"\r{count}/{total_count} - ID found: {twitter_id}", end="")
            else:
                print(f"\r{count}/{total_count} - ID not found for {username}", end="")

    print("\nTwitter ID retrieval complete. IDs saved to twitter_ids.txt")

if __name__ == "__main__":
    main()
