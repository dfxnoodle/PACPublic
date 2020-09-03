from flask import render_template, url_for, Blueprint, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from forms import RegNewUser, Login, ChangePassword
from db import users
from flask_login import current_user, login_user, logout_user, login_required, LoginManager


admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')

logman = LoginManager()
logman.login_view = 'admin.login'
logman.session_protection = "strong"

@admin.record_once
def on_load(state):
    logman.init_app(state.app)

class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    def check_admin(self):
        if users.find_one({"username": current_user.get_id()})['role'] != 'ADMIN':
            flash('Admin function! Please login as administrator', 'warning')
            logout_user()
            return redirect(url_for('admin.login'))

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    @logman.user_loader
    def load_user(login_user):
        usr = users.find_one({"username": login_user})
        if not usr:
            return render_template('login.html')
        return User(username=usr["username"])

    @admin.route('/login', methods=['GET', 'POST'])
    def login():
        form = Login()
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if form.validate_on_submit():
            valid_user = users.find_one({'username': form.username.data})
            if valid_user and User.check_password(valid_user['password'], form.password.data):
                user_obj = User(username=valid_user['username'])
                login_user(user_obj)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    return redirect(url_for('index'))
            else:
                flash("Invalid username or password", 'info')
        return render_template('login.html', form=form)

    @admin.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('admin.login'))

    @admin.route('/register', methods=['GET', 'POST'])
    def register():
        if users.find_one({"username": current_user.get_id()})['role'] != 'ADMIN':
            flash('Admin function! Please login as administrator', 'warning')
            logout_user()
            return redirect(url_for('admin.login'))
        form = RegNewUser()
        if form.validate_on_submit():
            users.insert({'username': form.username.data,
                          'email': form.email.data,
                          'password': generate_password_hash(form.password.data),
                          'role': form.role.data})
            flash('New user registered', 'info')
        return render_template('register.html', title='Register', form=form)

    @admin.route('/changepassword', methods=['GET', 'POST'])
    def changepassword():
        form = ChangePassword()
        user = users.find_one({'username': current_user.get_id()})
        if form.validate_on_submit():
            users.update_one(user,
                             {'$set': {'password': generate_password_hash(form.password.data)}})
            flash('Password Changed', 'info')
            return redirect(url_for('index'))
        return render_template('changepassword.html', title="Change Password", form=form)

