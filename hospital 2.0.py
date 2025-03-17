from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

diseases = {
    "Травма головы": 1,
    "Инфаркт": 1,
    "Инсульт": 1,
    "Перелом": 2,
    "Аппендицит": 2,
    "Грипп": 3,
    "ОРВИ": 3,
    "Пневмония": 2,
    "Повышенная температура": 3,
    "Ангина": 3,
    "Диабет": 2,
    "Гастрит": 3
}

# Создание базы данных
def init_db():
    with sqlite3.connect("patients.db") as conn:
        cursor = conn.cursor()
        
        # Включаем поддержку внешних ключей
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Таблица пациентов
        cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            diagnosis TEXT,
                            urgency INTEGER,
                            doctor_id INTEGER NULL,  -- Разрешаем NULL для doctor_id
                            status TEXT DEFAULT "waiting",
                            FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE SET NULL
                        )''')

        # Таблица врачей
        cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            specialty TEXT NOT NULL
                        )''')

        # Таблица соответствия врачей и болезней
        cursor.execute('''CREATE TABLE IF NOT EXISTS doctor_specialties (
                            doctor_id INTEGER,
                            disease TEXT,
                            FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
                        )''')

        conn.commit()

# Добавление врачей (если их нет)
def seed_doctors():
    with sqlite3.connect("patients.db") as conn:
        cursor = conn.cursor()

        # Проверяем, есть ли врачи в базе
        cursor.execute("SELECT COUNT(*) FROM doctors")
        if cursor.fetchone()[0] == 0:
            doctors = [
                ("Иван Петров", "Кардиолог"),
                ("Елена Смирнова", "Невролог"),
                ("Алексей Иванов", "Травматолог"),
                ("Мария Козлова", "Терапевт"),
                ("Дмитрий Сидоров", "Хирург"),
                ("Ольга Васильева", "Эндокринолог"),
                ("Наталья Орлова", "Гастроэнтеролог"),
            ]
            cursor.executemany("INSERT INTO doctors (name, specialty) VALUES (?, ?)", doctors)
            conn.commit()

        # Заполняем связи врачей с диагнозами
        cursor.execute("SELECT COUNT(*) FROM doctor_specialties")
        if cursor.fetchone()[0] == 0:
            doctor_specialties = [
                (1, "Инфаркт"),
                (1, "Инсульт"),
                (2, "Травма головы"),
                (3, "Перелом"),
                (4, "Грипп"),
                (4, "ОРВИ"),
                (4, "Повышенная температура"),
                (5, "Аппендицит"),
                (5, "Пневмония"),
                (6, "Диабет"),
                (7, "Гастрит"),
            ]
            cursor.executemany("INSERT INTO doctor_specialties (doctor_id, disease) VALUES (?, ?)", doctor_specialties)
            conn.commit()


def update_db_schema():
    with sqlite3.connect("patients.db") as conn:
        cursor = conn.cursor()

        # Получаем список колонок в таблице patients
        cursor.execute("PRAGMA table_info(patients);")
        columns = [col[1] for col in cursor.fetchall()]

        # Добавляем колонку doctor_id, если её нет
        if "doctor_id" not in columns:
            cursor.execute("ALTER TABLE patients ADD COLUMN doctor_id INTEGER NULL;")
            conn.commit()

        # Добавляем колонку status, если её нет
        if "status" not in columns:
            cursor.execute("ALTER TABLE patients ADD COLUMN status TEXT DEFAULT 'Ожидание';")
            conn.commit()

            print("Колонка 'status' успешно добавлена!")


def find_doctor_for_disease(diagnosis):
    with sqlite3.connect("patients.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT doctor_id FROM doctor_specialties WHERE disease = ?", (diagnosis,))
        doctor = cursor.fetchone()
        return doctor[0] if doctor else None

# Регистрация пациента
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        try:
            name = request.form['name']
            if any(char.isdigit() for char in name):
                raise ValueError("Имя не может содержать цифры")
        except Exception as e:
            return f"Ошибка в имени: {e}"

        try:
            age = int(request.form['age'])
            if not (0 <= age <= 130):
                raise ValueError("Возраст должен быть в диапазоне от 0 до 130")
        except ValueError as e:
            return f"Ошибка в возрасте: {e}"
        except Exception:
            return "Ошибка в вводе возраста"
        
        diagnosis = request.form['diagnosis']
        urgency = diseases.get(diagnosis, 3)

        doctor_id = find_doctor_for_disease(diagnosis)

        with sqlite3.connect("patients.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO patients (name, age, diagnosis, urgency, doctor_id) VALUES (?, ?, ?, ?, ?)", 
                           (name, age, diagnosis, urgency, doctor_id))
            conn.commit()

        return redirect(url_for('list_patients'))

    return '''
    <form method="post">
        Имя: <input type="text" name="name" required><br>
        Возраст: <input type="number" name="age" required><br>
        Диагноз: <select name="diagnosis">
            ''' + ''.join([f'<option value="{d}">{d} (Срочность {v})</option>' for d, v in diseases.items()]) + '''
        </select><br>
        <input type="submit" value="Зарегистрировать">
    </form>
    '''

# Список пациентов с врачами
@app.route('/patients')
def list_patients():
    with sqlite3.connect("patients.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT patients.id, patients.name, patients.age, patients.diagnosis, patients.urgency, patients.status, doctors.name 
            FROM patients 
            LEFT JOIN doctors ON patients.doctor_id = doctors.id
            ORDER BY patients.urgency ASC
        """)
        patients = cursor.fetchall()

    return '<br>'.join([f"ID: {p[0]}, {p[1]}, {p[2]} лет, Диагноз: {p[3]}, Срочность: {p[4]}, Статус: {p[5]}, Врач: {p[6] if p[6] else 'Не назначен'}" for p in patients])

# Список врачей
@app.route('/doctors')
def list_doctors():
    with sqlite3.connect("patients.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()

    return '<br>'.join([f"ID: {d[0]}, {d[1]}, Специализация: {d[2]}" for d in doctors])

# Поиск врача по болезни
@app.route('/find_doctor', methods=['GET', 'POST'])
def find_doctor():
    if request.method == 'POST':
        diagnosis = request.form['diagnosis']

        with sqlite3.connect("patients.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT doctors.name FROM doctors JOIN doctor_specialties ON doctors.id = doctor_specialties.doctor_id WHERE doctor_specialties.disease = ?", (diagnosis,))
            doctor = cursor.fetchone()

        if doctor:
            return f"Рекомендуемый врач: {doctor[0]}"
        else:
            return "Подходящий врач не найден."

    return '''
    <form method="post">
        Выберите диагноз: <select name="diagnosis">
            ''' + ''.join([f'<option value="{d}">{d}</option>' for d in diseases.keys()]) + '''
        </select><br>
        <input type="submit" value="Найти врача">
    </form>
    '''

if __name__ == '__main__':
    init_db()
    update_db_schema()  
    seed_doctors()
    app.run(debug=True)
