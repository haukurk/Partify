def filter_instagram_medias(medias):
    """
    Takes a list of Media objects (Instagram-python) and filters out stuff that you want to see.
    :param medias: List of Media objects.
    :return: list of dictionaries
    """

    filtered_media = []

    for media in medias:
        filtered_media.append(filter_instagram_media(media))

    return filtered_media


def filter_instagram_media(media):
    """
    Takes a Media object (Instagram-python) and filters out stuff that you want to see.
    :param media: Media objects.
    :return: dictionary
    """

    # Extract user info
    ret = {
        "media": {
            "low_resolution": media.get_thumbnail_url(),
            "standard_resolution": media.get_standard_resolution_url(),
        },
        "user": {
            "username": media.user.username,
            "profile_picture": media.user.profile_picture
        }
    }

    if media.caption:
        ret["caption"] = {"text": media.caption.text, "user": media.caption.user.username}
    else:
        ret["caption"] = ""

    return ret