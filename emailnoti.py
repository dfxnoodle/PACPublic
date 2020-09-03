from flask import Blueprint, flash, redirect, url_for
from flask_mail import Message, Mail
from ics import Calendar, Event
from datetime import timedelta, datetime
from db import patients
from pytz import timezone

mail = Mail()

emailnoti = Blueprint('emailnoti', __name__, static_folder='static', template_folder='templates')


@emailnoti.route("/apptnoti")
def appointment_notice(name, id, dtof, stage):
    c = Calendar()
    atte = (['dinochlai@cuhk.edu.hk', 'poemenchan@cuhk.edu.hk'])
    esubj = f'Appointment of patient {name}'
    mobile = patients.find_one({'HKID': id})['mobile']
    progress = ['Baseline 1', 'Baseline 2', 'Month 4', 'Month 8', 'Month 12'][stage]
    econt = f"""
            Name: {name}, ID: {id}, phone no.: {mobile}
            Progress: {progress}
            """
    e = Event(name=esubj, description=econt, attendees=atte)
    e.begin = dtof.astimezone(timezone('Asia/Hong_Kong'))
    e.duration = timedelta(hours=3)
    c.events.add(e)
    with open('appt.ics', 'w') as f:
        f.write(str(c))
    subj = f'New Appointment of patient {name}'
    recip = ['dinochlai@cuhk.edu.hk', 'dfxnoodle@yahoo.com.hk']
    text = f"""
            System generated notification.
            Patient: {name} 
            ID: {id}
            Phone: {mobile} 
            has a new appointment at:
            Date: {dtof: %d-%m-%Y}({dtof: %A}) 
            Time: {dtof:%H:%M}.
            Progress: {progress}
            Please add to calendar.
            """
    msg = Message(subj, recip, text)
    with open("appt.ics") as fp:
        msg.attach("appt.ics", "appt/ics", fp.read())
        mail.send(msg)
        flash('New appointment. Email notification sent', 'info')
        return redirect(url_for('index'))

def delete_notice(id, date):
    name = patients.find_one({'HKID': id})['name']
    apdate = date.astimezone(timezone('Asia/Hong_Kong'))
    subj = f'Appointment Cancellation of patient {name}'
    recip = ['dinochlai@cuhk.edu.hk', 'dfxnoodle@yahoo.com.hk']
    text = f"""
            System generated notification.
            Patient: {name}
            ID: {id} 
            cancelled the appointment of the following date and time:
            Date: {apdate: %d-%m-%Y}({apdate: %A})
            Time: {apdate: %H:%M}
            Please delete the appointment from calendar.
            """
    msg = Message(subj, recip, text)
    mail.send(msg)
    return redirect(url_for('index'))
