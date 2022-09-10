import numpy as np
import tweepy
import config, save_file
import pandas as pd
import matplotlib.pyplot as plt

# Constants for query
QUERY_STRING_CONSTANT = " -has:links -has:mentions -has:media -has:hashtags"
NUM_TWEETS_BY_LANGUAGE = 70

# Words to search for in the query by language
keywords = {
    "en": ["covid"],
    "fr": ["covid"],
    "es": ["covid"],
    "de": ["covid"],
}

# The client object that is used by the API
client = tweepy.Client(
    bearer_token=config.BEARER_TOKEN,
    access_token=config.ACCESS_TOKEN,
    access_token_secret=config.ACCESS_TOKEN_SECRET,
    consumer_key=config.CONSUMER_KEY,
    consumer_secret=config.CONSUMER_SECRET
)


def get_query_string(lang: str):
    """Convert a list of common words into a Twitter query string"""
    words_to_add = keywords[lang]
    string_so_far = words_to_add[0]
    for i in range(1, len(words_to_add)):
        string_so_far += " OR " + words_to_add[i]

    string_so_far += " lang:" + lang + QUERY_STRING_CONSTANT
    return string_so_far


def get_user_info(this_client, username):
    """Return information for a user by username"""
    user = this_client.get_user(username=username, user_fields='public_metrics')
    return user


def get_tweets_by_lang(lang: str, n: int, verbose=False):
    """
    Get n tweets for the specified language and return a series corresponding to
    The distribution of the lengths of the tweets
    """
    response = client.search_recent_tweets(
        query=get_query_string(lang),
        max_results=n,
        tweet_fields=["lang"],
        expansions=["author_id"])

    users = {u["id"]: u for u in response.includes["users"]}

    list_of_data_points = []
    for i in range(0, len(response.data)):
        this_tweet = response.data[i]
        this_user = get_user_info(client, users[this_tweet.author_id])

        if this_user.data.public_metrics["followers_count"] <= 1:
            continue

        if verbose:
            tweet_link = "https://twitter.com/" + users[this_tweet.author_id].username + "/status/" + str(this_tweet.id)
            print("============== TWEET#" + str(i) + " | " + tweet_link + " ==============")
            print(this_tweet.text)

        list_of_data_points.append(len(this_tweet.text))

    return pd.Series(list_of_data_points)


def populate_test_data(n: int, verbose=False):
    """Placeholder function for simulating data"""
    list_of_data_points = []
    for i in range(0, n):
        list_of_data_points.append(np.random.randint(10, 280))

    return pd.Series(list_of_data_points)


def append_dataframe_to_existing(new_df: pd.DataFrame, filename: str):
    """Append this data to the existing pickled data, AND return the concatenated df"""
    file_df = save_file.read_df_from_file(filename)
    if isinstance(file_df, bool) and not file_df:
        save_file.write_df_to_file(filename, new_df)
        return new_df
    else:
        concat_df = pd.concat([new_df, file_df], ignore_index=True)
        save_file.write_df_to_file(filename, concat_df)
        return concat_df


def reset_file_data(filename: str):
    save_file.delete_file(filename)


def get_new_dataframe():
    """Create dataframe and list of series that will be used"""
    df = pd.DataFrame()
    for language in keywords:
        # Either use real or test data
        new_series = get_tweets_by_lang(language, NUM_TWEETS_BY_LANGUAGE, True)
        # new_series = populate_test_data(NUM_TWEETS_BY_LANGUAGE, True)

        # Use the language as a parameter in the function
        args = {language: new_series}
        df = df.assign(**args)

    return df


def new_empty_dataframe():
    return pd.DataFrame()


df = append_dataframe_to_existing(get_new_dataframe(), "data.pkl")
# df = append_dataframe_to_existing(new_empty_dataframe(), "data.pkl")


# Create the histograms
print(df)
hist = df.hist(bins=10)
plt.show()
