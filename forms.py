from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateTimeField, BooleanField, \
    TextAreaField, IntegerField, RadioField, FloatField
from wtforms.validators import ValidationError, InputRequired, Email, EqualTo, Length, optional, NumberRange, Optional
import re
from datetime import datetime
from db import users, patients
from flask_login import current_user





class Login(FlaskForm):
    username = StringField('Login username', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=25)])

class ChangePassword(FlaskForm):
    opw = PasswordField('Old Password', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=25)])
    password2 = PasswordField('Password2', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Change password')

    def validate_opw(Flaskform, opw):
        global inputopw
        inputopw = opw.data
        hashedpw = users.find_one({'username': current_user.get_id()})['password']
        if not check_password_hash(hashedpw, inputopw):
            raise ValidationError('Invalid old password')

    def validate_password(Flaskform, password):
        if password.data == inputopw:
            raise ValidationError('Please use a new Password')

class RegNewUser(FlaskForm):
    username = StringField('New username', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=25)])
    password2 = PasswordField('Password2', validators=[InputRequired(), EqualTo('password')])
    email = StringField('Email', validators=[InputRequired(), Email()])
    role = SelectField('User role', choices=[('ADMIN', 'Administrator'),
                                            ('RA', 'Research assistant'),
                                            ('PI', 'Principle investigator'),
                                            ('COI', 'Co-investigator'),
                                            ('RO', 'Research office')])
    submit = SubmitField('register')

    def validate_username(self, username):
        user = users.find_one({'username': username.data})
        if user is not None:
            raise ValidationError('Please use another username')

    def validate_email(self, email):
        email = users.find_one({'email': email.data})
        if email is not None:
            raise ValidationError('Please use a different Email address')

class SearchPatients(FlaskForm):
    search = StringField('search', validators=[Length(min=1)])

class SearchForm(FlaskForm):
    search_form = StringField('search', validators=[Length(min=1)])


class RegNewPatient(FlaskForm):
    name = StringField('Patient name', validators=[InputRequired()])
    chisurname = StringField('Chinese Name', validators=[Optional()])
    hkid = StringField('Hong Kong ID', validators=[InputRequired()])
    mobile = StringField('Mobile number', validators=[Optional()])
    gender = SelectField('Gender', choices=[('M', 'MALE'), ('F', 'FEMALE')])
    dob = DateTimeField('Date of Birth', format='%Y-%m-%d', validators=[InputRequired()])
    rct_date = DateTimeField('Date of recruitment', format='%Y-%m-%d', validators=[InputRequired()])
    wts = BooleanField('Whatsapp', validators=[InputRequired()])
    spre = TextAreaField('Special Remarks', validators=[optional()])
    add = SubmitField('Add new patient')

    def validate_hkid(self, hkid):
        d = re.search("(^[a-zA-Z])(\d{7})", hkid.data)
        if d is None:
            raise ValidationError('Invalid Hong Kong ID')
        else:
            id = patients.find_one({'HKID': d.string})
            if id is not None:
                raise ValidationError('Patient registered already')

    def validate_mobile(self, mobile):
        mobileno = re.search(("\d{8}"), mobile.data)
        if mobileno is None:
            raise ValidationError('Phone number invalid')

    def validate_name(self, name):
        name = re.search("(\w.+\s).+", name.data)
        if name is None:
            raise ValidationError('Please enter a full name')

    def validate_dob(self, dob):
        bday = dob.data
        print(bday)
        if bday > datetime.now():
            raise ValidationError('Not from future')

class NewFolloups(FlaskForm):
    dtof = DateTimeField('Date and Time of Appointment', format='%Y-%m-%d %H:%M', validators=[InputRequired()])
    stage = IntegerField('Stage of fu', validators=[InputRequired()])
    eyes = RadioField('OD or OS', choices=[('R', 'OD'), ('L', 'OS')])
    md = FloatField('MD', validators=[Optional()])
    psd = FloatField('PSD', validators=[Optional()])
    iop1 = IntegerField('IOP 1', validators=[NumberRange(max=99), Optional()])
    iop2 = IntegerField('IOP 2', validators=[NumberRange(max=99), Optional()])
    vfi = IntegerField('VFI', validators=[NumberRange(max=999), Optional()])
    cct = IntegerField('CCT', validators=[NumberRange(max=999), Optional()])
    rnfl = IntegerField('Average RNFL', validators=[NumberRange(max=999), Optional()])
    rim = FloatField('RIM', validators=[Optional()])
    disc = FloatField('Disc Area', validators=[Optional()])
    vcd = FloatField('VCD', validators=[Optional()])
    cup = FloatField('Cup Volume', validators=[Optional()])
    re = StringField('Remarks', validators=[Optional()])
    addfu = SubmitField('Add a new follow up record')

class UpdateFollowup(FlaskForm):
    md = FloatField('MD', validators=[Optional()])
    psd = FloatField('PSD', validators=[Optional()])
    iop1 = IntegerField('IOP 1', validators=[NumberRange(max=99), Optional()])
    iop2 = IntegerField('IOP 2', validators=[NumberRange(max=99), Optional()])
    vfi = IntegerField('VFI', validators=[NumberRange(max=999), Optional()])
    cct = IntegerField('CCT', validators=[NumberRange(max=999), Optional()])
    rnfl = IntegerField('Average RNFL', validators=[NumberRange(max=999), Optional()])
    rim = FloatField('RIM', validators=[Optional()])
    disc = FloatField('Disc Area', validators=[Optional()])
    vcd = FloatField('VCD', validators=[Optional()])
    cup = FloatField('Cup Volume', validators=[Optional()])
    re = StringField('Remarks', validators=[Optional()])
    updatefu = SubmitField('Update follow up record')



class Confirmation(FlaskForm):
    confirm = ('Confirmation')
    submit = SubmitField('Submit')







