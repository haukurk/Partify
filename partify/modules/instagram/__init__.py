import config
from instagram.client import InstagramAPI

# Instagram instance.
api = InstagramAPI(access_token=config.INSTAGRAM_AUTH_TOKEN)