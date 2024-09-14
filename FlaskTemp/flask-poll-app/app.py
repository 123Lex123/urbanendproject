from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)  # Инициализация SQLAlchemy с приложением


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    options = db.relationship('Option', backref='poll', lazy=True)


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)

# Маршруты приложения
@app.route('/')
def index():
    polls = Poll.query.all()
    return render_template('index.html', polls=polls)

@app.route('/create', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        question = request.form['question']
        options = request.form.getlist('options')
        poll = Poll(question=question)
        db.session.add(poll)
        db.session.commit()

        for option_text in options:
            option = Option(text=option_text, poll_id=poll.id)
            db.session.add(option)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create_poll.html')

@app.route('/vote/<int:poll_id>', methods=['GET', 'POST'])
def vote(poll_id):
    poll = Poll.query.get(poll_id)

    if request.method == 'POST':
        option_id = request.form['option']
        option = Option.query.get(option_id)
        option.votes += 1
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('vote.html', poll=poll)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаем таблицы
    app.run(debug=True)
