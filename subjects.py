from flask import Blueprint, render_template,redirect, request, flash, url_for
from forms import RegNewPatient, SearchPatients, NewFolloups, UpdateFollowup
from db import patients, followups
from flask_login import login_required, current_user
from datetime import datetime
from emailnoti import appointment_notice, delete_notice

subjects = Blueprint('subjects', __name__, static_folder='static', template_folder='templates')


class Subjects:
    @login_required
    @subjects.route('/newpatients', methods=['GET', 'POST'])
    def register():
        form = RegNewPatient()
        if form.validate_on_submit():
            patients.insert({'name': form.name.data.upper(),
                           'chisurname': form.chisurname.data,
                           'HKID': form.hkid.data,
                           'mobile': form.mobile.data,
                           'gender': form.gender.data,
                           'DOB': form.dob.data,
                           'rct_date': form.rct_date.data,
                           'wts': form.wts.data,
                           'spre': form.spre.data})
            flash('New patient registered', 'info')
        return render_template('addnewpatients.html', title='Registered', form=form)

    @subjects.route('/deletepatient/<delhkid>', methods=['GET', 'POST'])
    def delete_patient(delhkid):
        form = SearchPatients
        if current_user.is_authenticated:
            id = delhkid
            name = patients.find_one({'HKID': id})['name']
            confirmed = request.form.get('confirm')
            flash(f'Would you like to delete patient {name} ID {id}?', 'del_confirm')
            if confirmed:
                patients.delete_one({'name': name, 'HKID': id})
                flash(f'Patient {name} deleted', 'info')
                return redirect(url_for('index'))
            return render_template('deletepatient.html', id=id, form=form)

    @subjects.route('/followups/<id>', methods=['GET', 'POST'])
    def new_fus(id):
        name = patients.find_one({'HKID': id})['name']
        form = NewFolloups()
        if form.validate_on_submit():
            stage = form.stage.data
            eyes = form.eyes.data
            dtof = form.dtof.data
            exfu = followups.find_one({'HKID': id, 'stage': stage, 'eyes': eyes})
            if exfu is None:
                if dtof > datetime.today():
                    followups.insert({'dtof': dtof,
                                      'HKID': id,
                                      'stage': stage,
                                      'eyes': eyes})
                    appointment_notice(name, id, dtof, stage)
                else:
                    followups.insert({'dtof': dtof,
                                      'HKID': id,
                                      'stage': stage,
                                      'eyes': eyes,
                                      'md': form.md.data,
                                      'psd': form.psd.data,
                                      'iop1': form.iop1.data,
                                      'iop2': form.iop2.data,
                                      'vfi': form.vfi.data,
                                      'cct': form.cct.data,
                                      'rnfl': form.rnfl.data,
                                      'rim': form.rim.data,
                                      'disc': form.disc.data,
                                      'vcd': form.vcd.data,
                                      'cup': form.cup.data,
                                      're': form.re.data})
                    flash('New follow up recorded', 'info')
            else:
                flash('Duplicated record! Please check')
        return render_template('followups.html', form=form, id=id, name=name)

    @subjects.route('/details/<pid>', methods=['GET', 'POST'])
    def details(pid):
        form = SearchPatients
        id = pid
        result = patients.find_one({'HKID': id})
        dob = result['DOB']
        age = int((datetime.today() - dob).days / 365.2425)
        furesults = followups.find({'HKID': id}).sort('dtof', 1)
        return render_template('details.html', form=form, id=id, result=result, age=age, furesults=furesults,
                               datetime=datetime)

    @subjects.route('/deleterecord/<reid>/<int:stage>/<eye>', methods=['GET', 'POST'])
    def delrecord(reid, stage, eye):
        form = SearchPatients
        if current_user.is_authenticated:
            id = reid
            confirmed = request.form.get('confirm')
            target = {'HKID': id, 'stage': stage, 'eyes': eye}
            date = followups.find_one(target)['dtof']
            if date > datetime.today():
                flash('Would you like to delete this appointment?', 'del_confirm')
                if confirmed:
                    delete_notice(id, date)
                    followups.delete_one(target)
                    flash('Appointment deleted', 'info')
                    return redirect(url_for('index'))
            else:
                flash('Would you like to delete this record?', 'del_confirm')
                if confirmed:
                    followups.delete_one(target)
                    flash('Record deleted', 'info')
                    return redirect(url_for('index'))
        return render_template('deleterecord.html', id=id, form=form, stage=stage, eye=eye)

    @subjects.route('/updaterecord/<uid>/<int:stage>/<eye>', methods=['GET', 'POST'])
    def updaterecord(uid, stage, eye):
        if current_user.is_authenticated:
            name = patients.find_one({'HKID': uid})['name']
            form = UpdateFollowup()
            id = uid
            record = followups.find_one({'HKID': id, 'stage': stage, 'eyes': eye})
            if form.validate_on_submit():
                followups.update_one(record,
                                     {'$set':
                                     {'md': form.md.data,
                                      'psd': form.psd.data,
                                      'iop1': form.iop1.data,
                                      'iop2': form.iop2.data,
                                      'vfi': form.vfi.data,
                                      'cct': form.cct.data,
                                      'rnfl': form.rnfl.data,
                                      'rim': form.rim.data,
                                      'disc': form.disc.data,
                                      'vcd': form.vcd.data,
                                      'cup': form.cup.data,
                                      're': form.re.data}})
                flash('Record updated', 'info')
                return redirect(url_for('index'))
            else:
                flash('Please update the record')
        return render_template('updaterecord.html', name=name, id=id, form=form, record=record)












