__author__ = 'haukurk'
from instagram import subscriptions

def process_tag_update(update):
    """
    Prints update to stdout.
    :param update: update message
    :return: void
    """
    print update

# React to user type updates
reactor = subscriptions.SubscriptionsReactor()
reactor.register_callback(subscriptions.SubscriptionType.USER, process_tag_update)


