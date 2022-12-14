from flask import render_template, request, redirect, flash, session
from flask_app import app, bcrypt

from flask_app.models.user_model import User
from flask_app.models.sighting_model import Sighting
from flask_app.models.skeptic_model import Skeptic

#? ==================== USER PAGE after LOGIN ====================
@app.route('/dashboard')
def welcome():
    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')

    # pass user into html to display current user's name
    user = User.get_by_id({'id' : session['uid']})
    
    # pass sighting into html to display selected sighting info
    sightings = Sighting.get_all()

    return render_template('dashboard.html', user=user, sightings=sightings)

#? ==================== CREATE ONE SIGHTING ====================
@app.route('/new/sighting')
def direct_to_report():
    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')
    
    user = User.get_by_id({'id' : session['uid']})

    return render_template('new_sighting.html', user=user)

@app.route('/new/sighting/process', methods=["POST"])
def report_sighting():
    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')

    # checks valid input
    is_valid = Sighting.validate_sighting(request.form)
    if not is_valid:
        return redirect('/new/sighting')

    # manually create data to pass owner_id into sighting instance
    data = {
        **request.form,
        'owner_id' : session['uid']
    }

    Sighting.create(data)

    return redirect('/dashboard')

#? ==================== READ ONE SIGHTING ====================
@app.route('/show/<int:sighting_id>')
def show_one_sighting(sighting_id):
    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')
    
    # pass user into html to display current user's name
    user = User.get_by_id({'id' : session['uid']})

    data = {
        'id' : sighting_id
    }

    # pass sighting into html to display selected sighting info
    sighting = Sighting.get_one_sighting(data)

    # check if current user is in the skeptical list of current sighting
    user.set_skeptical(data)

    # set a bool value to prevent current user being skeptical
    bool = False
    if sighting.owner_id != session['uid']:
        bool = True

    return render_template('one_sighting.html', user=user, sighting=sighting, bool=bool)

#? ==================== UPDATE ONE SIGHTING ====================
@app.route('/edit/<int:sighting_id>')
def direct_to_edit(sighting_id):
    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')
    
    # pass user into html to display current user's name
    # pass the sighting into html to pre-populate information
    user = User.get_by_id({'id' : session['uid']})
    sighting = Sighting.get_one_sighting({'id' : sighting_id})
    return render_template('edit_sighting.html', user=user, sighting=sighting)

@app.route('/edit_sighting_process', methods=["POST"])
def edit_one_sighting():
    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')

    # checks valid input
    is_valid = Sighting.validate_sighting(request.form)
    if not is_valid:
        id = request.form['id']
        return redirect(f'/edit/{id}')

    Sighting.edit_sighting_with_id(request.form)
    return redirect('/dashboard')

#? ==================== DELETE ONE SIGHTING ====================
@app.route('/delete/<int:sighting_id>')
def delete_one_sighting(sighting_id):

    # if uid does not exist in session, deny access
    if 'uid' not in session:
        return redirect('/')

    # manually creates data for later search or input
    data = {
        'id' : sighting_id
    }

    # prevent other users to delete
    sighting = Sighting.get_one_sighting(data)
    if session['uid'] != sighting.owner_id:
        return redirect('/dashboard')

    # first delete any skeptics associated with this sighting
    Skeptic.delete_sighting_skeptic(data)
    # then delete this sighting
    Sighting.delete_sighting_with_id(data)

    return redirect('/dashboard')


