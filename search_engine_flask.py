import json
import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hobbies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    profile_id = db.Column(db.String(50), nullable=False)
    hobby_desc = db.Column(db.String(255), nullable=False)
    hobby_link = db.Column(db.String(255), nullable=False)

# Функция для инициализации базы данных из JSON
def init_db():
    if not os.path.exists('hobbies.db'):
        db.create_all()
        with open('data.json', 'r') as file:
            data = json.load(file)
            for key, value in data.items():
                new_hobby = Hobby(
                    title=value['title'].lower(),  # Преобразуем в нижний регистр
                    profile_id=value['profile_id'],
                    hobby_desc=value['description']['hobby_desc'],
                    hobby_link=value['description']['hobby_link']
                )
                db.session.add(new_hobby)
            db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.form.get('search', '').lower()  # Преобразуем в нижний регистр
    page = request.args.get('page', 1, type=int)
    
    if search_query:
        hobbies = Hobby.query.filter(Hobby.title.contains(search_query)).paginate(page=page, per_page=5)
    else:
        hobbies = Hobby.query.paginate(page=page, per_page=5)

    return render_template('index.html', hobbies=hobbies, search_query=search_query)

if __name__ == '__main__':
    init_db()  # Инициализируем базу данных
    app.run(debug=True)
