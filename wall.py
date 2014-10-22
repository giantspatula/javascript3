import json

from flask import Flask, request, render_template, make_response, redirect

from api import wall_list, wall_add, wall_error, clear_messages, check_flooding


app = Flask(__name__)

# The "secret key" is needed for the Flask session machinery. In a real
# application, this should be a unguessable string and should NOT be
# checked into version control. Typically, one stores this as an
# environmental variable outside of the Flask app and gets it with
# os.environ['MY_SECRET_KEY']. For our exercise purposes, though, it's
# fine to have this here.
app.secret_key = 'a4c96d59-57a8-11e4-8b97-80e6500ee2f6'


@app.route("/")
def index():
    """Return index page."""
    page = render_template("wall.html", messages=['message #1'])
    return page


def _convert_to_JSON(result):
    """Convert result object to a JSON web request."""

    # In order for us to return a response that isn't just HTML, we turn our
    # response dictionary into a string-representation (using json.dumps),
    # then use the flask `make_response` function to create a response object
    # out of this.
    response = make_response(json.dumps(result))

    # We can then set some headers on this response object:

    # Access-Control-Allow-Origin isn't needed for this example, but it's
    # a demonstration of a useful feature: since it should be safe to allow
    # Javascript from websites other than ours to get/post to our API, we
    # explicitly allow this.
    response.headers['Access-Control-Allow-Origin'] = "*"

    # Setting the MIMETYPE to JSON's will explicitly mark this as JSON;
    # this can help some client applications understand what they get back.
    response.mimetype = "application/json"

    return response


@app.route("/api/wall/list.json")
def list_messages_json():
    """Return list of wall messages as JSON."""

    result = wall_list()
    return _convert_to_JSON(result)


@app.route("/api/wall/list.html")
def list_messages_html():
    """Return list of wall messages as JSON."""

    result = wall_list()
    messages = []
    for message in result.get('messages', []):
        print message['message']
        print type(message['message'])

    return render_template('_messages.html', messages=result.get('messages', []))


@app.route("/api/wall/reset", methods=['POST'])
def reset_messages():
    clear_messages()
    return _convert_to_JSON({"result" : "OK"})


@app.route("/api/wall/add", methods=['POST'])
def add_message():
    """Add a message and return list of wall messages as JSON."""

    # Get the message from the "m" argument passed in the POST.
    # (to get things from a GET response, we've used request.args.get();
    # this is the equivalent for getting things from a POST response)
    msg = request.form.get('m').strip()
    datetime = int(request.form.get('datetime').strip())
    print datetime

    if check_flooding(datetime):
        return _convert_to_JSON({"result" : "failure"})

    if msg is None:
        result = wall_error("You did not specify a message to set.")

    elif msg == "":
        result = wall_error("Your message is empty")

    else:
        result = wall_add(msg)

    return _convert_to_JSON(result)



if __name__ == "__main__":
    app.run(debug=True)