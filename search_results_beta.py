from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

with open('hobby_data/data.json', 'r', encoding='utf-8') as f:
    hobbies_data = json.load(f)

@app.route('/search_results')
def search_results():
    query = request.args.get('query', '').lower()
    result = []
    n = 0
    for hobby in hobbies_data['hobbies']:
        if query in hobby['name'].lower() or query in hobby['desc'].lower():
            n += 1
            result.append(hobby)

    return render_template('search_results.html', result=result, n=n)

if __name__ == '__main__':
    app.run(debug=True)
