from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Структурированные данные резюме (CV)
cv_data = {
    "name": "Иван Иванов",
    "experience": [
        {"company": "Компания А", "position": "Разработчик", "years": 3},
        {"company": "Компания Б", "position": "Старший разработчик", "years": 2}
    ],
    "skills": ["Python", "Flask", "SQL", "Git"],
    "contact": {
        "email": "ivan@example.com",
        "LinkedIn": "https://linkedin.com/in/ivan",
        "phone": "+123456789"
    },
    "education": [
        {"degree": "Бакалавр компьютерных наук", "year": 2018, "institution": "Университет X"},
        {"degree": "Магистр информационных технологий", "year": 2020, "institution": "Университет Y"}
    ],
    "projects": [
        {"title": "Проект 1", "description": "Описание проекта 1", "year": 2021},
        {"title": "Проект 2", "description": "Описание проекта 2", "year": 2022}
    ]
}

# HTML-шаблон
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>CV API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        button {
            margin: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        #result {
            margin-top: 20px;
            padding: 10px;
        }
        table {
            border-collapse: collapse;
            margin: 5px 0;
            width: 80%%;
            max-width: 800px;
        }
        table, th, td {
            border: 1px solid #999;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        h1, h2, h3 {
            margin-top: 20px;
        }
        .section-title {
            margin-top: 20px;
            font-weight: bold;
            font-size: 1.2em;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Personal CV API</h1>
    <p>Click on the button to  get the corresponding  section of the resume:</p>
    <button onclick="fetchData('/cv')">Полное резюме</button>
    <button onclick="fetchData('/cv/experience')">Опыт работы</button>
    <button onclick="fetchData('/cv/skills')">Навыки</button>
    <button onclick="fetchData('/cv/contact')">Контакты</button>
    <button onclick="fetchData('/cv/education')">Образование</button>
    <button onclick="fetchData('/cv/projects')">Проекты</button>
    
    <div id="result"></div>
    
    <script>
        // Функция для преобразования объекта/массива в HTML
        function renderData(data) {
            // Если это массив
            if (Array.isArray(data)) {
                // Проверим, являются ли элементы массива объектами (например, [{...}, {...}])
                // Если это объекты, создадим таблицу
                if (data.length > 0 && typeof data[0] === 'object' && !Array.isArray(data[0])) {
                    let html = '<table><tr>';
                    // Берём ключи из первого объекта
                    let keys = Object.keys(data[0]);
                    // Заголовок таблицы
                    for (let key of keys) {
                        html += '<th>' + key + '</th>';
                    }
                    html += '</tr>';
                    // Строки таблицы
                    for (let item of data) {
                        html += '<tr>';
                        for (let key of keys) {
                            // Если значение – тоже объект или массив, обрабатываем рекурсивно
                            if (typeof item[key] === 'object') {
                                html += '<td>' + renderData(item[key]) + '</td>';
                            } else {
                                html += '<td>' + item[key] + '</td>';
                            }
                        }
                        html += '</tr>';
                    }
                    html += '</table>';
                    return html;
                } else {
                    // Если это массив простых значений (например, [\"Python\", \"Flask\"])
                    // или массив объектов в другом формате, выведем как список
                    let html = '<ul>';
                    for (let item of data) {
                        if (typeof item === 'object') {
                            html += '<li>' + renderData(item) + '</li>';
                        } else {
                            html += '<li>' + item + '</li>';
                        }
                    }
                    html += '</ul>';
                    return html;
                }
            } 
            // Если это объект
            else if (typeof data === 'object' && data !== null) {
                let html = '';
                for (let key in data) {
                    html += '<div class=\"section-title\">' + key + '</div>';
                    html += '<div>' + renderData(data[key]) + '</div>';
                }
                return html;
            } 
            // Если это примитив (строка, число и т.д.)
            else {
                return '<span>' + data + '</span>';
            }
        }

        function fetchData(endpoint) {
            fetch(endpoint)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').innerHTML = renderData(data);
                })
                .catch(error => {
                    document.getElementById('result').innerHTML = 'Ошибка: ' + error;
                });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/cv", methods=["GET"])
def full_cv():
    return jsonify(cv_data)

@app.route("/cv/experience", methods=["GET"])
def cv_experience():
    years_filter = request.args.get("years", type=int)
    experience = cv_data.get("experience", [])
    if years_filter is not None:
        filtered_experience = [job for job in experience if job.get("years") == years_filter]
        return jsonify({"experience": filtered_experience})
    return jsonify({"experience": experience})

@app.route("/cv/skills", methods=["GET"])
def cv_skills():
    return jsonify({"skills": cv_data.get("skills", [])})

@app.route("/cv/contact", methods=["GET"])
def cv_contact():
    return jsonify({"contact": cv_data.get("contact", {})})

@app.route("/cv/education", methods=["GET"])
def cv_education():
    return jsonify({"education": cv_data.get("education", [])})

@app.route("/cv/projects", methods=["GET"])
def cv_projects():
    return jsonify({"projects": cv_data.get("projects", [])})

if __name__ == "__main__":
    app.run(debug=True)
