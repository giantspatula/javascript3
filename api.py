"""API for JS Webapp Wall application.

In real life, for us to share messages between different users of this
application, we'd want to store the messages in a server-side persistent
store (like a relational database). However, since we're demonstrating how
to use client-side session systems, this stores things there.
"""


from flask import session
import time

# So that you can play with the `get` API, we return a single
# test message as the default.
DEFAULT_MESSAGES = [
    {'message': 'Welcome! (this is the built-in first message)'},
]


def wall_error(error):
    """Handle API errors.

        error: (string) error message

        returns: dictionary error object.
    """

    return {
        "result": error,
    }


def wall_list():
    """Get messages.

        returns: dictionary with messages list + result code.
    """

    return {
        "result": "OK",
        "messages": session.setdefault('wall', DEFAULT_MESSAGES),
    }

def check_flooding(datetime):
    datetime = int(time.time())
    last_message = session.get("last_message", 0)
    if datetime - last_message < 5000:
        #print "api line 46 (flooding)"
        return True
    else:
        session["last_message"] = datetime
        #print "api line 50 (no flooding)"
        return False

def wall_add(msg):
    """Set a new message.

        msg: (string) message

        returns: dictionary with messages list + result code.
    """

    wall_dict = {
        "message": msg,
    }

    session.setdefault('wall', []).append(wall_dict)

    result = wall_list()
    result["result"] = "Message Received"

    return result

def clear_messages():
    """ clears messages and returns default session & message"""
    session['wall'] = DEFAULT_MESSAGES


