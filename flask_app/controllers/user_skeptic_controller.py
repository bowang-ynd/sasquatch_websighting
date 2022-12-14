from flask import render_template, request, redirect, flash, session
from flask_app import app

from flask_app.models.user_model import User
from flask_app.models.sighting_model import Sighting
from flask_app.models.skeptic_model import Skeptic

#? ==================== UPDATE ONE SIGHTING ====================
@app.route('/skeptical/<int:sighting_id>')
def change_skeptical(sighting_id):

    # get the instance of current user and current sighting
    user = User.get_by_id({'id' : session['uid']})
    
    data = {
        'id' : sighting_id
    }
    
    sighting = Sighting.get_one_sighting(data)

    
    # check and change the skeptical bool value for current user
    user.set_skeptical(data)
    user.change_skeptical(user.is_skeptical)

    # update current sighting's skeptics list accordingly
    sighting.update_skeptics(user.is_skeptical, user.get_name())

    # update the skeptics in database
    Skeptic.update_skeptics(user.is_skeptical, user.id, sighting.id)

    return redirect(f'/show/{sighting_id}')
