from flask import Blueprint, url_for, redirect, flash, render_template, request
import re
from db import patients
from forms import SearchPatients, SearchForm
from flask_login import login_required

searches = Blueprint('searches', __name__, static_folder='static', template_folder='templates')


def pnot_found():
    flash("Patient not found", 'not_found')
    pass

class search:
    @searches.route('/searchbar', methods=['GET', 'POST'])
    @login_required
    def searchbar():

        form = SearchPatients()
        if form.validate_on_submit():
            HKID = re.search("(^[A-Z])(\d{7})", form.search.data.strip().upper())
            mobile = re.search("(\d{8})", form.search.data.strip())
            name = re.search("(\w.+\s).+", form.search.data.strip().upper())
            if HKID is not None:
                if len(list(patients.find({'HKID': HKID.string}))) > 0:
                    results = patients.find({'HKID': HKID.string})
                    return render_template('search.html', results=results, form=form)
                else:
                    pnot_found()
            elif mobile is not None:
                if len(list(patients.find({'mobile': mobile.string}))) > 0:
                    results = patients.find({'mobile': mobile.string})
                    return render_template('search.html', results=results, form=form)
                else:
                    pnot_found()
            elif name is not None:
                if len(list(patients.find({'name': name.string}))) > 0:
                    results = patients.find({'name': name.string})
                    return render_template('search.html', results=results, form=form)
                else:
                    pnot_found()
            else:
                pnot_found()
        return redirect(url_for('index'))

    @searches.route('/search', methods=['GET', 'POST'])
    @login_required
    def search():
        form = SearchForm()
        if form.validate_on_submit():
            HKID = re.search("(^[A-Z])(\d{7})", form.search_form.data.strip().upper())
            mobile = re.search("(\d{8})", form.search_form.data.strip())
            name = re.search("(\w.+\s).+", form.search_form.data.strip().upper())
            if HKID is not None:
                if len(list(patients.find({'HKID': HKID.string}))) > 0:
                    results = patients.find({'HKID': HKID.string})
                    return render_template('searchmini.html', results=results, form=form)
                else:
                    pnot_found()
            elif mobile is not None:
                if len(list(patients.find({'mobile': mobile.string}))) > 0:
                    results = patients.find({'mobile': mobile.string})
                    return render_template('searchmini.html', results=results, form=form)
                else:
                    pnot_found()
            elif name is not None:
                if len(list(patients.find({'name': name.string}))) > 0:
                    results = patients.find({'name': name.string})
                    return render_template('searchmini.html', results=results, form=form)
                else:
                    pnot_found()
            else:
                pnot_found()
        return render_template('searchform.html', form=form)





