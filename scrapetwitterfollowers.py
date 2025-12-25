import requests
from requests.exceptions import ConnectTimeout
import csv
import re
import time
from itertools import cycle
import sys
import json
# List of authentication tokens
def read_auth_tokens_from_file(filename):
    with open(filename, "r") as file:
        return json.load(file)

auth_tokens = read_auth_tokens_from_file("auth_tokens.json")

num_tokens = len(auth_tokens)

def read_cursor_from_file(filename):
    with open(filename, "r") as file:
        return file.read().strip()

def write_cursor_to_file(cursor_value, filename):
    with open(filename, "w") as file:
        file.write(cursor_value)

initial_cursor = read_cursor_from_file("cursor.txt")

initial_url = f'https://twitter.com/i/api/graphql/9h9mQXmOcAzq_ylCepCfAQ/Followers?variables={{"userId":"328990309","count":50,"includePromotedContent":false,"cursor":"{initial_cursor}"}}&features={{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}}'

column_names = ["Created At", "Description", "Websites", "Fast Followers Count", "Favourites Count", "Followers Count", "Friends Count", "Has Custom Timelines", "Is Translator", "Listed Count", "Location", "Media Count", "Name", "Screen Name", "Professional", "URL"]

def extract_entity_value(entities, key):
    match = re.search(fr'"{key}":(.*?)(?:,|}})', entities)
    value = match.group(1).strip() if match else "Not Available"
    if key == "url" and value != "Not Available":
        urls_match = re.findall(r'"expanded_url":"([^"]+)"', value)
        return urls_match if urls_match else "Not Available"
    else:
        return value

def extract_entity_values2(entities):
    match = re.search(r'"expanded_url":"([^"]+)"', entities)
    if match:
        return match.group(1)
    else:
        return "Not Available"

def extract_entity_values3(entities, key):
    match = re.search(fr'"{key}":\s*(\d+)', entities)
    value = match.group(1).strip() if match else "Not Available"
    return value

try:
    with open("follower_data.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)  

        # Cycle through authentication tokens
        token_cycle = cycle(auth_tokens)

        found_timeline_cursor = False

        for _ in range(num_tokens):
            if found_timeline_cursor:
                break

            current_token = next(token_cycle)
            headers = current_token["headers"]

            try:
                response = requests.get(initial_url, headers=headers, timeout=10)
                response.raise_for_status()
            except (ConnectTimeout, requests.exceptions.ReadTimeout):
                print("Timeout occurred. Waiting for 10 seconds before retrying...")
                time.sleep(10)
                continue
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 401:
                    print(f"Unauthorized access with {current_token['token']}. Trying with the next token.")
                elif err.response.status_code == 403:
                    print("Access forbidden. Waiting for 10 seconds before retrying...")
                    time.sleep(10)
                else:
                    print(f"HTTP error occurred: {err}")
                continue

            response_text = response.text

            if "AuthorizationError" in response_text and "account is temporarily locked" in response_text:
                print(f"{current_token['token']} is temporarily locked. Trying with the next token.")
                continue  # Move to the next token

            if response.status_code == 401:
                print(f"Unauthorized access with {current_token['token']}. Trying with the next token.")
                continue

            pattern = r'"created_at":"([^"]+?)".*?"description":"([^"]*?)".*?"entities":(.*?),"name":"([^"]+?)".*?"screen_name":"([^"]+?)"(.*?)("professional":\{(.*?)\}.*?)?"element":"user"'

            matches = re.findall(pattern, response_text)

            for match in matches:
                created_at, description, entities, name, screen_name, _, professional, _ = match
                
                professional_value = professional.strip() if professional.strip() else "Not Available"

                websites_value = extract_entity_values2(entities)
                fast_followers_count_value = extract_entity_value(entities, "fast_followers_count")
                favourites_count_value = extract_entity_value(entities, "favourites_count")
                followers_count_value = extract_entity_value(entities, "followers_count")
                friends_count_value = extract_entity_value(entities, "friends_count")
                has_custom_timelines_value = extract_entity_value(entities, "has_custom_timelines")
                is_translator_value = extract_entity_value(entities, "is_translator")
                listed_count_value = extract_entity_value(entities, "listed_count")
                location_value = extract_entity_value(entities, "location")
                media_count_value = extract_entity_values3(entities, "media_count")

                url = f"https://twitter.com/{screen_name}"

                location_value = location_value.replace('"', '')

                writer.writerow([
                    created_at, 
                    description if description else "Not Available", 
                    "".join(websites_value) if websites_value != "Not Available" else "Not Available", 
                    fast_followers_count_value, 
                    favourites_count_value, 
                    followers_count_value, 
                    friends_count_value, 
                    has_custom_timelines_value, 
                    is_translator_value, 
                    listed_count_value, 
                    location_value, 
                    media_count_value, 
                    name, 
                    screen_name, 
                    professional_value, 
                    url if url else "Not Available"
                ])

            pattern_cursor = r'"value":"(\d+\|\-?\d+)"'  
            match_cursor = re.search(pattern_cursor, response_text)

            if match_cursor:
                cursor_value = match_cursor.group(1)
                found_timeline_cursor = True
                print("Value of TimelineCursor:", cursor_value)

                while cursor_value and not cursor_value.startswith("0|"):
                    updated_url = initial_url.replace(f'"cursor":"{initial_cursor}"', f'"cursor":"{cursor_value}"')

                    current_token = next(token_cycle)
                    headers = current_token["headers"]

                    try:
                        response = requests.get(updated_url, headers=headers, timeout=10)
                        response.raise_for_status()
                    except (ConnectTimeout, requests.exceptions.ReadTimeout):
                        print("Timeout occurred. Waiting for 10 seconds before retrying...")
                        time.sleep(10)
                        continue
                    except requests.exceptions.HTTPError as err:
                        if err.response.status_code == 401:
                            print(f"Unauthorized access with {current_token['token']}. Trying with the next token.")
                        elif err.response.status_code == 403:
                            print("Access forbidden. Waiting for 10 seconds before retrying...")
                            time.sleep(10)
                        else:
                            print(f"HTTP error occurred: {err}")
                        continue

                    response_text = response.text

                    if "AuthorizationError" in response_text and "account is temporarily locked" in response_text:
                        print(f"{current_token['token']} is temporarily locked. Trying with the next token.")
                        continue  # Move to the next token

                    if response.status_code == 401:
                        print(f"Unauthorized access with {current_token['token']}. Trying with the next token.")
                        continue

                    matches = re.findall(pattern, response_text)

                    for match in matches:
                        created_at, description, entities, name, screen_name, _, professional, _ = match
                        
                        professional_value = professional.strip() if professional.strip() else "Not Available"

                        websites_value = extract_entity_values2(entities)
                        fast_followers_count_value = extract_entity_value(entities, "fast_followers_count")
                        favourites_count_value = extract_entity_value(entities, "favourites_count")
                        followers_count_value = extract_entity_value(entities, "followers_count")
                        friends_count_value = extract_entity_value(entities, "friends_count")
                        has_custom_timelines_value = extract_entity_value(entities, "has_custom_timelines")
                        is_translator_value = extract_entity_value(entities, "is_translator")
                        listed_count_value = extract_entity_value(entities, "listed_count")
                        location_value = extract_entity_value(entities, "location")
                        media_count_value = extract_entity_values3(entities, "media_count")

                        url = f"https://twitter.com/{screen_name}"

                        location_value = location_value.replace('"', '')

                        writer.writerow([
                            created_at, 
                            description if description else "Not Available", 
                            "".join(websites_value) if websites_value != "Not Available" else "Not Available", 
                            fast_followers_count_value, 
                            favourites_count_value, 
                            followers_count_value, 
                            friends_count_value, 
                            has_custom_timelines_value, 
                            is_translator_value, 
                            listed_count_value, 
                            location_value, 
                            media_count_value, 
                            name, 
                            screen_name, 
                            professional_value, 
                            url if url else "Not Available"
                        ])

                    match_cursor = re.search(pattern_cursor, response_text)
                    if match_cursor:
                        cursor_value = match_cursor.group(1)
                        print("Value of TimelineCursor:", cursor_value)
                        write_cursor_to_file(cursor_value, "cursor.txt")
                    else:
                        print("TimelineCursor value not found in the response. Waiting 10 seconds before retrying...")
                        time.sleep(10)
                        continue

                    time.sleep(20/num_tokens)  # every account sends one request every 20 sec to not exceed the ratelimit

                if cursor_value.startswith("0|"):
                    print("All followers scraped.")
                    write_cursor_to_file("-1|1", "cursor.txt") #to make the tool start from the start again when scraping a new account
                    sys.exit(1)  # Exit with code 1 to indicate successful completion
            else:
                print("TimelineCursor value not found")
                print("Data is saved in follower_data.csv.")
                sys.exit(2)  # Exit with a non-zero code (other than 1) to indicate an error

    print("Follower data saved to follower_data.csv")

except KeyboardInterrupt:
    print("Data is saved.")
    sys.exit(0)  # Exit with code 0 to indicate success

except Exception as e:
    print("An error occurred:", e)
    sys.exit(2)  # Exit with a non-zero code (other than 1) to indicate an error