__author__ = 'haukurk'

from flask import session


def kill_stream(consumers, producers):
    """Kills the current user's Twitter consumer."""

    user = session['identity']
    consumer = consumers.get(user, None)
    if session['tracking']:
        terms = frozenset(session['tracking'])
    else:
        print "FAIL! tracking session not found."
    producer = producers.get(terms, None)

    if consumer:
        consumer.kill()
        del consumers[user]

        if producer:
            producer.remove_client(user)