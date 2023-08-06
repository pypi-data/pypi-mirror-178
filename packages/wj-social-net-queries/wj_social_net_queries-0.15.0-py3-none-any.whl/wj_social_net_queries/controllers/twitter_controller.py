from typing import Optional, List
from wj_social_net_queries.connectors.api_twitter_connector import TwitterWJ

def fetch_terms_tweets(
    terms: List[str],
    twitter_consumer_key: str,
    twitter_consumer_secret: str,
    twitter_key: str,
    twitter_secret: str,
    max_tweets_per_term: Optional[int] = 20
):
    """
    Description
    ----------
    Function that retrieves a list of tweets from the configured terms set by
    the admin.

    Arguments
    ---------
    terms:
        List of Tweets names
    Credentials:
        https://developer.twitter.com/en/docs/authentication/oauth-1-0a/api-key-and-secret
        twitter_consumer_key
        twitter_consumer_secret
        twitter_key
        twitter_secret
    max_tweets_per_term:
        Number of max tweets captured in the request

    Return
    -------
    Fisrt n tweets founds with the term and a list with the last tweet id by term.
        list, tweets | list, terms_updated

    """
    tweets = []
    terms_updated = []
    twitter_wj = TwitterWJ(
        twitter_consumer_key=twitter_consumer_key,
        twitter_consumer_secret=twitter_consumer_secret,
        twitter_key=twitter_key,
        twitter_secret=twitter_secret
    )
    # Fetch tweets for each term
    for term in terms:

        # Fetch tweets
        term_tweets = twitter_wj.get_term_tweets(
            term=term,
            num_tweets=max_tweets_per_term,
        )
        # Update since_id using latest tweet fetched
        tweet_ids = [tweet["tweet_id"] for tweet in term_tweets]
        if len(tweet_ids):
            tweets.extend(term_tweets)
            new_since_id = str(max(tweet_ids))
        else:
            new_since_id = None
        terms_updated.append(
            {
                "name": term,
                "since_id": new_since_id
            }
        )
    return tweets, terms_updated


def send_direct_message(
    text: str,
    twitter_id: str,
    twitter_consumer_key: str,
    twitter_consumer_secret: str,
    twitter_key: str,
    twitter_secret: str,
):
    """
    Description
    ----------
    Function that retrieves a list of tweets from the configured terms set by
    the admin.

    Arguments
    ---------
    text:
        Text to send
    twitter_id:
        Id of the tw user
    Credentials:
        https://developer.twitter.com/en/docs/authentication/oauth-1-0a/api-key-and-secret
        twitter_consumer_key
        twitter_consumer_secret
        twitter_key
        twitter_secret
    max_tweets_per_term:
        Number of max tweets captured in the request

    Return
    -------
    None

    """
    twitter_wj = TwitterWJ(
        twitter_consumer_key=twitter_consumer_key,
        twitter_consumer_secret=twitter_consumer_secret,
        twitter_key=twitter_key,
        twitter_secret=twitter_secret
    )
    
    try:
        message_sent = twitter_wj.send_direct_message(
            text=text,
            twitter_id=twitter_id
        )
        return message_sent
    except Exception as e:
        print("send_direct_message controller :: ", e)


def write_comment(
    status:str,
    in_reply_status_id:str,
    user_name: str,
    twitter_consumer_key: str,
    twitter_consumer_secret: str,
    twitter_key: str,
    twitter_secret: str,
):
    """
    Description
    ----------
    Function that retrieves a list of tweets from the configured terms set by
    the admin.

    Arguments
    ---------
    status:
        Text to send
    twitter_id:
        Id of the tw user
    Credentials:
        https://developer.twitter.com/en/docs/authentication/oauth-1-0a/api-key-and-secret
        twitter_consumer_key
        twitter_consumer_secret
        twitter_key
        twitter_secret
    max_tweets_per_term:
        Number of max tweets captured in the request

    Return
    -------
    None

    """
    twitter_wj = TwitterWJ(
        twitter_consumer_key=twitter_consumer_key,
        twitter_consumer_secret=twitter_consumer_secret,
        twitter_key=twitter_key,
        twitter_secret=twitter_secret
    )
    
    try:
        message_sent = twitter_wj.write_comment(
            status=status,
            in_reply_status_id=in_reply_status_id,
            user_name=user_name
        )
        return message_sent
    except Exception as e:
        print("send_direct_message controller :: ", e)


def get_user_by_screen_name(
    screen_name: str,
    twitter_consumer_key: str,
    twitter_consumer_secret: str,
    twitter_key: str,
    twitter_secret: str,
):
    """
    Description
    ----------
    Function that gets a usar info, given his/her user name

    Arguments
    ---------
    screen_name:
        Text to send
    Credentials:
        https://developer.twitter.com/en/docs/authentication/oauth-1-0a/api-key-and-secret
        twitter_consumer_key
        twitter_consumer_secret
        twitter_key
        twitter_secret

    Return
    -------
    dict | None: Dictionary with user info if is found, None if not

    """
    twitter_wj = TwitterWJ(
        twitter_consumer_key=twitter_consumer_key,
        twitter_consumer_secret=twitter_consumer_secret,
        twitter_key=twitter_key,
        twitter_secret=twitter_secret
    )
    user = twitter_wj.get_user(
        screen_name=screen_name
    )
    if user:
        return user[0].__dict__
    return None

