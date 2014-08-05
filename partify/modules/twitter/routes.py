from flask import Blueprint, jsonify
import filters
import tweepy
from __init__ import auth
from partify.common import responses
from partify.common import statuscodes

mod = Blueprint('cakes', __name__, url_prefix='/api')

twitter_api = tweepy.API(auth)

@mod.route('/twitter/<string:hashtag>', methods=['GET'])
def search_twitter(hashtag):
    """
    Route that queries Twitter from a given hashtag
    @param hashtag: twitter hashtag
    @return: JSON response.
    """

    hashtag = u"#%s" % unicode(hashtag)

    searched_tweets = []

    try:
        searched_tweets = twitter_api.search(q=hashtag, result_type="recent", count=100)
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        return jsonify(
            responses.create_error_response("error", e.message)), statuscodes.HTTP_OK
        # break

    tweets = filters.filter_twitter_statuses(searched_tweets)

    return jsonify(
        responses.create_single_object_response('success', tweets, "tweets")), statuscodes.HTTP_OK
