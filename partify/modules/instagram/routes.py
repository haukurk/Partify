from flask import Blueprint, jsonify
import filters
from __init__ import api
from partify.common import responses
from partify.common import statuscodes

mod = Blueprint('instagram', __name__, url_prefix='/api/instagram')


@mod.route('/hook/<string:subscription>', methods=['GET'])
def instagram_hook(subscription):
    """
    Route that hooks real-time feed to instagram
    @param hashtag: twitter hashtag
    @return: JSON response.
    """

    return jsonify({"status": "error", "message": "not implemented"}), statuscodes.HTTP_NOT_IMPLEMENTED


@mod.route('/search/<string:hashtag>', methods=['GET'])
def instragram_search(hashtag):
    """
    Route that search instagram
    :param hashtag: hashtag string to search for
    :return: JSON response
    """

    mediaIds, next_ = api.tag_recent_media(count=50, tag_name=hashtag)
    resp = filters.filter_instagram_medias(mediaIds)

    return jsonify(responses.create_multiple_object_response("success", resp, "posts")), statuscodes.HTTP_OK

