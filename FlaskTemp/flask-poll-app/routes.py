from flask import render_template, request, redirect, url_for
from models import Poll, Option, db  # Импортируем модели и db

def configure_routes(app):
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
