from typing import List

import tweepy
import config

client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
# client = tweepy.Client(
#     consumer_key=config.CONSUMER_KEY,
#     consumer_secret=config.CONSUMER_SECRET,
#     access_token=config.ACCESS_TOKEN,
#     access_token_secret=config.ACCESS_TOKEN_SECRET
# )

QUERY_STRING_CONSTANT = " -has:links -has:mentions -has:media -has:hashtags"

keywords = {
    "en": ["the"],
    "fr": ["le"],
    "es": ["el"],
    "de": ["die"],
}


def get_query_string(lang: str, keywords: List[str]):
    string_so_far = keywords[0]
    for i in range(1, len(keywords)):
        string_so_far += " OR " + keywords[i]

    string_so_far += " lang:" + lang + QUERY_STRING_CONSTANT
    print(string_so_far)
    return string_so_far


def get_user_info(this_client, username):
    user = this_client.get_user(username=username, user_fields='public_metrics')
    return user


# response = client.search_recent_tweets(query=query, max_results=10)
response = client.search_recent_tweets(
    query=get_query_string("en", keywords["en"]),
    max_results=10,
    tweet_fields=["lang"],
    expansions=["author_id"])

users = {u["id"]: u for u in response.includes["users"]}

for i in range(0, len(response.data)):
    this_tweet = response.data[i]
    this_user = get_user_info(client, users[this_tweet.author_id])

    if this_user.data.public_metrics["followers_count"] <= 1:
        continue

    tweet_link = "https://twitter.com/" + users[this_tweet.author_id].username + "/status/" + str(this_tweet.id)
    print("============== TWEET#" + str(i) + " | " + tweet_link + " ==============")
    print(this_tweet.text)






