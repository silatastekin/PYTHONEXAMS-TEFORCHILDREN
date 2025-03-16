#SILA TAŞTEKİN-16.03.2025-PYTHON EXAM SİTE
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam.db'
db = SQLAlchemy(app)

# Kullanıcı Tablosu
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    highest_score = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Integer, default=0)

# Sınav Tablosu
class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answers = db.Column(db.JSON)  # Kullanıcının cevaplarını JSON olarak kaydedeceğiz

# Sınav Soruları
questions = [
    {
        "id": 1,
        "question": "Flask nedir?",
        "options": ["Bir Python web framework'ü", "Bir veritabanı", "Bir programlama dili"],
        "answer": "Bir Python web framework'ü",
        "topic": "Python ile web geliştirme (Flask)"
    },
    {
        "id": 2,
        "question": "Discord bot otomasyonu için hangi kütüphane kullanılır?",
        "options": ["Discord.py", "Flask", "TensorFlow"],
        "answer": "Discord.py",
        "topic": "Python ile sohbet botu otomasyonu (Discord.py)"
    },
    {
        "id": 3,
        "question": "TensorFlow öncelikle ne için kullanılır?",
        "options": ["Web geliştirme", "Makine öğrenmesi", "Veri kazıma"],
        "answer": "Makine öğrenmesi",
        "topic": "Bilgisayar görüşü (Computer Vision - TensorFlow, ImageAI)"
    },
    {
        "id": 4,
        "question": "Python'da web kazıma için hangi kütüphane kullanılır?",
        "options": ["BeautifulSoup", "NLTK", "Flask"],
        "answer": "BeautifulSoup",
        "topic": "Doğal Dil İşleme (Natural Language Processing)"
    },
    {
        "id": 5,
        "question": "NLTK ne için kullanılır?",
        "options": ["Web geliştirme", "Doğal Dil İşleme", "Bilgisayar görüşü"],
        "answer": "Doğal Dil İşleme",
        "topic": "Doğal Dil İşleme (Natural Language Processing)"
    },
    {
        "id": 6,
        "question": "Görüntü tanıma için hangi kütüphane kullanılır?",
        "options": ["ImageAI", "Flask", "Discord.py"],
        "answer": "ImageAI",
        "topic": "Bilgisayar görüşü (Computer Vision - TensorFlow, ImageAI)"
    },
    {
        "id": 7,
        "question": "Flask'ın temel kullanım amacı nedir?",
        "options": ["Web geliştirme", "Makine öğrenmesi", "Veri analizi"],
        "answer": "Web geliştirme",
        "topic": "Python ile web geliştirme (Flask)"
    },
    {
        "id": 8,
        "question": "Python'da yapay zeka geliştirme için hangi kütüphane kullanılır?",
        "options": ["TensorFlow", "BeautifulSoup", "Flask"],
        "answer": "TensorFlow",
        "topic": "Python ile yapay zeka geliştirme"
    },
    {
        "id": 9,
        "question": "BeautifulSoup'un temel amacı nedir?",
        "options": ["Web kazıma", "Doğal Dil İşleme", "Web geliştirme"],
        "answer": "Web kazıma",
        "topic": "Doğal Dil İşleme (Natural Language Processing)"
    },
    {
        "id": 10,
        "question": "Sohbet botu oluşturmak için hangi kütüphane kullanılır?",
        "options": ["Discord.py", "Flask", "NLTK"],
        "answer": "Discord.py",
        "topic": "Python ile sohbet botu otomasyonu (Discord.py)"
    }
]

# Ana Sayfa
@app.route('/')
def home():
    return render_template('index.html')

# Sınav Başlatma
@app.route('/start_exam', methods=['POST'])
def start_exam():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, highest_score=0, last_score=0)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('exam', username=username))

# Sınav Sayfası
@app.route('/exam/<username>')
def exam(username):
    user = User.query.filter_by(username=username).first()
    global_highest_score = db.session.query(db.func.max(User.highest_score)).scalar()
    return render_template('exam.html', questions=questions, username=username, global_highest_score=global_highest_score, user_highest_score=user.highest_score)

# Sınav Sonuçları
@app.route('/submit_exam/<username>', methods=['POST'])
def submit_exam(username):
    score = 0
    user_answers = {}

    for q in questions:
        user_answer = request.form.get(f'q{q["id"]}')
        user_answers[f'q{q["id"]}'] = user_answer
        if user_answer == q["answer"]:
            score += 1

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, highest_score=0, last_score=0)
        db.session.add(user)

    # Yeni sınav sonucunu kaydet
    new_exam = Exam(score=score, user_id=user.id, answers=user_answers)
    db.session.add(new_exam)

    # En yüksek puanı güncelle
    if score > user.highest_score:
        user.highest_score = score
    user.last_score = score
    db.session.commit()

    # En yüksek puanı alan tüm kullanıcıları bul
    global_highest_score = db.session.query(db.func.max(User.highest_score)).scalar()
    global_highest_users = User.query.filter_by(highest_score=global_highest_score).all()

    return render_template('result.html', score=score, user_highest_score=user.highest_score, global_highest_score=global_highest_score, global_highest_users=global_highest_users, username=username)

# Tüm Sonuçları Görüntüleme
@app.route('/view_results')
def view_results():
    users = User.query.all()
    user_results = []

    # En yüksek puanı alan tüm kullanıcıları bul
    global_highest_score = db.session.query(db.func.max(User.highest_score)).scalar()
    global_highest_users = User.query.filter_by(highest_score=global_highest_score).all()

    for user in users:
        user_info = {
            "username": user.username,
            "highest_score": user.highest_score,
            "last_score": user.last_score,
            "details": []
        }
        exams = Exam.query.filter_by(user_id=user.id).all()
        for exam in exams:
            exam_details = {
                "score": exam.score,
                "answers": exam.answers
            }
            user_info["details"].append(exam_details)
        user_results.append(user_info)

    return render_template('view_results.html', user_results=user_results, global_highest_score=global_highest_score, global_highest_users=global_highest_users)

# Veritabanını Temizleme
@app.route('/clear_database')
def clear_database():
    try:
        # Tüm kullanıcıları ve sınav sonuçlarını sil
        db.session.query(User).delete()
        db.session.query(Exam).delete()
        db.session.commit()
        return "Veritabanı başarıyla temizlendi!"
    except Exception as e:
        db.session.rollback()
        return f"Veritabanı temizlenirken bir hata oluştu: {str(e)}"

# Uygulama Başlatma
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)