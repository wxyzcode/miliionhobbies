from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/search')
def render():
    return render_template('search.html')

@app.route('/create_hobby_result', methods=["GET"])
def search_results():
    with open('hobby_data/data.json', 'r', encoding='utf-8') as f:
        hobbies_data = json.load(f)
        
    name = request.args.get('hobby_name')
    desc = request.args.get('hobby_desc')
    link = request.args.get('hobby_link')
    user = request.args.get('hobby_user')
    uniqueuser = request.args.get('hobby_uniqueuser')
    
    new_data ={
            "title": name,
            "desc": desc,
            "uniquename": uniqueuser,
            "name": user,
            "link": link
         }
    
    hobbies_data.append(new_data)
    
    with open('hobby_data/data.json', 'w') as f:
        json.dump(hobbies_data, f, indent=4)
    
    return render_template('create_hobby_result.html', results=results, n=n)

if __name__ == '__main__':
    app.run(debug=True)
