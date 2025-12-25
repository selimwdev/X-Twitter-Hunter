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

def follow_user(user_id, bearer_token, count, total_count):
    headers = {
        'Host': 'twitter.com',
        'Cookie': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Client-Uuid': '558ff0e5-748f-4385-91d4-e0f1e5e160f2',
        'X-Twitter-Auth-Type': 'OAuth2Session',
        'X-Csrf-Token': '',
        'X-Twitter-Client-Language': 'en',
        'X-Twitter-Active-User': 'yes',
        'X-Client-Transaction-Id': '+',
        'Authorization': f'Bearer {bearer_token}',
        'Referer': 'https://twitter.com/home',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Te': 'trailers'
    }

    data = {
        'include_profile_interstitial_type': '1',
        'include_blocking': '1',
        'include_blocked_by': '1',
        'include_followed_by': '1',
        'include_want_retweets': '1',
        'include_mute_edge': '1',
        'include_can_dm': '1',
        'include_can_media_tag': '1',
        'include_ext_is_blue_verified': '1',
        'include_ext_verified_type': '1',
        'include_ext_profile_image_shape': '1',
        'skip_status': '1',
        'user_id': user_id,
    }

    try:
        response = requests.post('https://twitter.com/i/api/1.1/friendships/create.json', headers=headers, data=data)
        if response.status_code == 200:
            print(f"{count}/{total_count} user followed", end='\r')
        else:
            print(f"Failed to follow user with ID {user_id}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    usernames_file = "usernames.txt"
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'  # Replace with your Twitter API bearer token

    with open(usernames_file, "r") as file:
        usernames = file.read().splitlines()

    for count, username in enumerate(usernames, 1):
        twitter_id = get_twitter_id(username)
        if twitter_id:
            print(f"{count}/{len(usernames)} user followed", end='\r')
            follow_user(twitter_id, bearer_token, count, len(usernames))
        else:
            print(f"Failed to get Twitter ID for {username}")

if __name__ == "__main__":
    main()
