import etcd3
from flask import Flask, request

app = Flask(__name__)

def list_all_keys():
    """Connects to etcd and retrieves all keys, returning decoded strings."""
    try:
        etcd = etcd3.client()
        keys = etcd.get_all()
        return [key.decode('utf-8') for key, _ in keys]
    except Exception as e:
        return f"Error listing keys: {e}"

def get_value_for_key(key):
    """Connects to etcd, retrieves value for the provided key, and decodes it."""
    try:
        etcd = etcd3.client()
        value, _ = etcd.get(key.encode('utf-8'))
        if value is None:
            return f"Key '{key}' doesn't exist."
        return value.decode('utf-8')
    except Exception as e:
        return f"Error getting value: {e}"

def put_key_value_pair(key, value):
    """Connects to etcd and puts the key-value pair, returning a success message."""
    try:
        etcd = etcd3.client()
        etcd.put(key.encode('utf-8'), value.encode('utf-8'))
        return f"Key '{key}' with value '{value}' successfully added to etcd"
    except Exception as e:
        return f"Error putting key-value pair: {e}"

def delete_key(key):
    """Connects to etcd and attempts to delete the provided key."""
    try:
        etcd = etcd3.client()
        deleted = etcd.delete(key.encode('utf-8'))
        if deleted:
            return f"Key '{key}' successfully deleted."
        else:
            return f"Key '{key}' doesn't exist."
    except Exception as e:
        return f"Error deleting key: {e}"

@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ETCD Key-Value Store</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #007bff;
            text-align: center;
        }
        button {
            padding: 10px 20px;
            margin: 5px;
            border: none;
            background-color: #007bff;
            color: #fff;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background-color: #0056b3;
        }
        form {
            margin-top: 20px;
        }
        input[type="text"] {
            padding: 8px;
            font-size: 16px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        input[type="submit"] {
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            background-color: #007bff;
            color: #fff;
            cursor: pointer;
            border-radius: 5px;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 5px;
        }
    </style>
    <script>
        function showSection(sectionId) {
            var sections = document.querySelectorAll('.section');
            for (var i = 0; i < sections.length; i++) {
                sections[i].style.display = 'none';
            }
            document.getElementById(sectionId).style.display = 'block';
        }
        function redirectTo(url) {
            window.location.href = url;
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>ETCD Key-Value Store</h1>
        <button onclick="redirectTo('/list')">List All Keys</button>
        <button onclick="showSection('get')">Get Value for Key</button>
        <button onclick="showSection('put')">Put Key-Value Pair</button>
        <button onclick="showSection('delete')">Delete Key</button>
        
        <div id="get" class="section" style="display: none;">
            <h2>Get Value for Key</h2>
            <form method="post" action="/get">
                Key: <input type="text" name="key">
                <input type="submit" value="Get">
            </form>
        </div>
        
        <div id="put" class="section" style="display: none;">
            <h2>Put Key-Value Pair</h2>
            <form method="post" action="/put">
                Key: <input type="text" name="key"><br>
                Value: <input type="text" name="value"><br>
                <input type="submit" value="Put">
            </form>
        </div>
        
        <div id="delete" class="section" style="display: none;">
            <h2>Delete Key</h2>
            <form method="post" action="/delete">
                Key: <input type="text" name="key">
                <input type="submit" value="Delete">
            </form>
        </div>
    </div>
</body>
</html>

    """

@app.route('/list', methods=['GET'])
def list_keys():
    keys = list_all_keys()
    return "<h2>All Keys</h2><ul>{}</ul>".format("".join(f"<li>{key}</li>" for key in keys))

@app.route('/get', methods=['POST'])
def get_key():
    key_to_get = request.form['key']
    value = get_value_for_key(key_to_get)
    return f"<h2>Value for '{key_to_get}':</h2><p>{value}</p>"

@app.route('/put', methods=['POST'])
def put_key():
    key_to_put = request.form['key']
    value_to_put = request.form['value']
    return put_key_value_pair(key_to_put, value_to_put)

@app.route('/delete', methods=['POST'])
def delete_key_route():
    key_to_delete = request.form['key']
    return delete_key(key_to_delete)

if __name__ == '__main__':
    app.run(debug=True)
