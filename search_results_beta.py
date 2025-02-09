from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Загружаем данные из JSON-файла
with open('data.json', 'r', encoding='utf-8') as f:
    hobbies_data = json.load(f)

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search_results')
def search_results():
    return render_template('search_results.html')

@app.route('/api/search')
def api_search():
    query = request.args.get('query', '').lower()
    results = []

    # Поиск по данным
    for hobby in hobbies_data.values():
        if query in hobby['name'].lower() or query in hobby['desc'].lower():
            results.append(hobby)

    return jsonify(results)
  
if __name__ == '__main__':
    app.run(debug=True)
