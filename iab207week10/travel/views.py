from flask import Blueprint, render_template, request, redirect, url_for
from .models import Events
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    event = db.session.scalars(db.select(Events)).all()    
    return render_template('index.html', event=event)

@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        event = db.session.scalars(db.select(Events).where(Events.description.like(query)))
        return render_template('index.html', events=event)
    else:
        return redirect(url_for('main.index'))