from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Путь к файлу JSON
DATA_JSON_PATH = 'stats.json'


def load_data():
    if os.path.exists(DATA_JSON_PATH):
        with open(DATA_JSON_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}


@app.route('/templates/search.html')
def profile():
    hobby_data = load_data()
    hobby = hobby_data['hobbies']
    user_data = load_data()
    user = user_data['users']
    return render_template('search.html', users=user, hobbies=hobby)

if __name__ == '__main__':
    app.run(debug=True)
