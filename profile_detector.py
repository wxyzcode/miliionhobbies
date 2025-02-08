from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Путь к файлу JSON
DATA_JSON_PATH = 'user_data/data.json'

def load_data():
    """Загрузить данные из JSON файла."""
    if os.path.exists(DATA_JSON_PATH):
        with open(DATA_JSON_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

@app.route('/templates/profile.html')
def profile():
    # Получаем ID из URL (после #)
    user_id = request.args.get('id')
    
    # Загружаем данные
    data = load_data()
    
    # Ищем хобби по ID
    hobby = data.get(user_id)

    return render_template('profile.html', hobby=hobby)

if __name__ == '__main__':
    app.run(debug=True)
