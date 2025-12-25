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
        'Cookie': 'g_state={"i_l":0}; kdt=q2UFinXgzeJTfNwKadbmEAkLb2JWstImj4tqhmsL; d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; _ga=GA1.2.1352642500.1704914873; ads_prefs="HBIRAAA="; guest_id=v1%3A171391447535871875; guest_id_ads=v1%3A171391447535871875; guest_id_marketing=v1%3A171391447535871875; auth_token=439709ce41374ebdfe03dc01bfdcfbcbfaa36674; ct0=e346dab0a114a1cf38fc2ee10e7664be10a16eacdde7c98f0ea6771767dfece0a93b058108351d935861d5bc9ca9e5bc859d6715c4ad4630099168472d4c1a0ea31f4820af8fd2d6201088f6581c9e21; twid=u%3D1782780932384038912; dnt=1; lang=en; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCMLJUjSPAToMY3NyZl9p%250AZCIlNzZjN2I5YWQxOTUyZDk2NDZjYzllNTliMTFiZTFhNGI6B2lkIiU3YTgx%250AYzIyOWVhZTcyN2U0ZmE4MDExNTQwZTQxMmQyMQ%253D%253D--03f34e81295fb4364b1ee9978249b32df2a33773; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; _gid=GA1.2.766785609.1714779983; personalization_id="v1_vuaKYT9U7dJmHXrBGv6dLA=="',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'X-Client-Uuid': '558ff0e5-748f-4385-91d4-e0f1e5e160f2',
        'X-Twitter-Auth-Type': 'OAuth2Session',
        'X-Csrf-Token': 'e346dab0a114a1cf38fc2ee10e7664be10a16eacdde7c98f0ea6771767dfece0a93b058108351d935861d5bc9ca9e5bc859d6715c4ad4630099168472d4c1a0ea31f4820af8fd2d6201088f6581c9e21',
        'X-Twitter-Client-Language': 'en',
        'X-Twitter-Active-User': 'yes',
        'X-Client-Transaction-Id': 'ZVERl1N09K4F8g0272tTUmuCKxwD6kA6z3B2yVBh9rqoHtMSi+82WyJFNaHpsGYJkgjRvGQRK9b9RebgIpcUt4Is08mEZg',
        'Authorization': f'Bearer {bearer_token}',
        'Referer': 'https://twitter.com/home',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Te': 'trailers'
    }

    data = {
        "variables": {
            "listId": "1786798928085532955",
            "userId": user_id
        },
        "features": {
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True
        },
        "queryId": "FpvDMFk4k8HXtkYjQGg_bw"
    }

    try:
        response = requests.post('https://twitter.com/i/api/graphql/FpvDMFk4k8HXtkYjQGg_bw/ListAddMember', headers=headers, json=data)
        if response.status_code == 200:
            print(f"{count}/{total_count} user added", end='\r')
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
            print(f"{count}/{len(usernames)} user added", end='\r')
            follow_user(twitter_id, bearer_token, count, len(usernames))
        else:
            print(f"Failed to get Twitter ID for {username}")

if __name__ == "__main__":
    main()
