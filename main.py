import tweepy
import config

client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
# client = tweepy.Client(
#     consumer_key=config.CONSUMER_KEY,
#     consumer_secret=config.CONSUMER_SECRET,
#     access_token=config.ACCESS_TOKEN,
#     access_token_secret=config.ACCESS_TOKEN_SECRET
# )

query = "e lang:de -has:links -has:mentions -has:media"

# response = client.search_recent_tweets(query=query, max_results=10)
response = client.search_recent_tweets(query=query, max_results=10, tweet_fields=["lang"], expansions=["author_id"])
users = {u["id"]: u for u in response.includes["users"]}
for i in range(0, len(response.data)):
    print("============== TWEET#" + str(i) + "==============")
    print(response.data[i].text)



