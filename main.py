from flask import Flask, render_template, request
from pymongo import MongoClient
from flask_login import current_user, login_required
from config import Config
from forms import SearchPatients
from db import users, followups, patients
from datetime import datetime
from flask_cors import CORS
from flask_mail import Mail

# Blueprint routes #
from admin import admin
from subjects import subjects
from searches import searches
from emailnoti import emailnoti



app = Flask(__name__)
app.config.from_object(Config)
db = MongoClient(Config.MONGO_URI, wtimeout=2500)
CORS(app)
mail = Mail(app)

app.register_blueprint(admin)
app.register_blueprint(subjects)
app.register_blueprint(searches)
app.register_blueprint(emailnoti)

@app.template_filter()
def dateonlyfilter(value, format='%d/%m/%Y'):
    return datetime.strftime(value, format)
    """Convert a datetime to date only"""

app.jinja_env.filters['dateonlyfilter'] = dateonlyfilter

todolist = []

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    upcoming = followups.aggregate([
            {'$match': {'dtof': {'$gt': datetime.today()}}
                    },
            {'$lookup': {
                    'from': 'patient_info',
                    'let': {'hkid': "$HKID"},
                    'pipeline': [{
                    '$match': {
                    '$expr': {
                    '$eq': ["$HKID", "$$hkid"]}}},
                    {'$project': {'name': 1, 'mobile': 1, 'wts': 1}}],
                    'as': 'info'
                        }
                    },
                    {'$sort': {'dtof': -1}}
    ])

    todo = request.form.get('todo')
    if todo and todo is not None:
        todolist.insert(0, todo)
        if len(todolist) > 6:
            todolist.pop(-1)

    role = users.find_one({'username': current_user.get_id()})['role']
    Role = {'ADMIN': "Administrator",
            'RA': "Research assistant",
            'PI': "Principle investigator",
            'COI': "Co-investigator",
            'RO': "Research Office"}[role]
    return render_template('index.html', role=Role, form=SearchPatients(), todolist=todolist, upcoming=upcoming)

@app.route('/exceltable', methods=['GET', 'POST'])
def excel():
    results = followups.find({'dtof': {'$lt': datetime.today()}})
    return render_template('exceltable.html', form=SearchPatients(), results=results)




