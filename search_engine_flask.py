from flask import Flask, render_template, request
import json

app = Flask(__name__)

def load_data():
    with open('hobby_data/data.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_results')
def search_results():
    query = request.args.get('query', '')
    data = load_data()

    results = [item for item in data if query.lower() in item['name'].lower() or query.lower() in item['description'].lower()]
    
    return render_template('search_results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)

