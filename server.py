from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route('/')
def home():
    """Serve the main app page. The main page will be 'static' in the sense of being purely client-side Svelte. So no further paramters or returns are needed."""
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory('client/public', path)

@app.route('/upload')
def submit_data(credential: str, endpoint: str, payload:str) -> str:
    """Take some object or payload from the frontend and send it off somewhere as an upload. The logic of where and how is TBD.

    Args:
        credential (str): Some sort of identifier that says you're allowed to put the thing where you're putting it.
        endpoint (str): _description_
        payload (str): The actual contents. Should be converted from string to json.

    Returns:
        str: _description_
    """
    return('Good job')

if __name__ == "__main__":
    app.run(debug=True)