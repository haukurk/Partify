def filter_twitter_statuses(statues):
    """
    Takes a list of Status objects (tweepy) and filters out stuff that you want to see.
    :param statues: List of Tweepy Status objects.
    :return: list of dictionaries
    """

    filtered_statuses = []

    for status in statues:
        filtered_statuses.append(filter_twitter_status(status))

    return filtered_statuses


def filter_twitter_status(status):
    """
    Takes a Status object (tweepy) and filters out stuff that you want to see.
    :param status: Tweepy Status objects.
    :return: dictionaries
    """

    # Extract user info
    user = status.user

    return {"text": status.text.encode('utf8'),
            "user": user.name,
            "screen_name": user.screen_name,
            "profile_image_url": status.user.profile_image_url,
            "profile_image_url_not_scaled": status.user.profile_image_url.replace('_normal', ''),
            #"created_at": status.created_at,
            "geo": status.geo,
            "source": status.source}
