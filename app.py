from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sr_code = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sr_code = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    datetime = db.Column(db.String(50), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    sr_code = request.form['sr_code']
    qr = qrcode.make(sr_code)
    qr.save(f'static/{sr_code}.png')
    return redirect(url_for('show_qr', sr_code=sr_code))

@app.route('/qr/<sr_code>')
def show_qr(sr_code):
    return render_template('qr.html', sr_code=sr_code)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        sr_code = request.form['sr_code']
        description = request.form['description']
        datetime = request.form['datetime']
        new_schedule = Schedule(sr_code=sr_code, description=description, datetime=datetime)
        db.session.add(new_schedule)
        db.session.commit()
        return redirect(url_for('schedule'))
    all_schedules = Schedule.query.all()
    return render_template('schedule.html', schedules=all_schedules)

if __name__ == '__main__':
    app.run(debug=True)
