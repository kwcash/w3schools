from flask import Flask, render_template, request, redirect, url_for
from database import db, NewMediaProject
from datetime import datetime
import os

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.instance_path, 'new_media.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    projects = NewMediaProject.query.all()
    return render_template('index.html', projects=projects)

@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        new_project = NewMediaProject(
            title=request.form['title'],
            author=request.form['author'],
            genre=request.form['genre'],
            logline=request.form['logline'],
            synopsis=request.form['synopsis'],
            status=request.form['status'],
            production_date=datetime.strptime(request.form['production_date'], '%Y-%m-%d') if request.form['production_date'] else None
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')
