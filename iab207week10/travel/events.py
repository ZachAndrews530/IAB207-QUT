from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Events, Comment
from .forms import EventsForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

evntbp = Blueprint('event', __name__, url_prefix='/event')

@evntbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Events).where(Events.id==id))
    form = CommentForm()    
    return render_template('event/show.html', event=event, form=form)

@evntbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventsForm()
  if form.validate_on_submit():
    db_file_path = check_upload_file(form)
    event = Events(name=form.name.data,description=form.description.data, 
    image=db_file_path, tickets=form.tickets.data)
    db.session.add(event)
    db.session.commit()
    flash('Successfully created new Music Event', 'success')
    return redirect(url_for('event.create'))
  return render_template('event/create.html', form=form)

def check_upload_file(form):
  fp = form.image.data
  filename = fp.filename 
  BASE_PATH = os.path.dirname(__file__)
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  db_upload_path = '/static/image/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path

@evntbp.route('/<event>/comment', methods=['GET', 'POST'])  
@login_required
def comment(event):  
    form = CommentForm()  
    event_obj = db.session.scalar(db.select(Events).where(Events.id==event))
    if form.validate_on_submit():  
      comment = Comment(text=form.text.data, event=event_obj,
                        user=current_user) 
      db.session.add(comment) 
      db.session.commit() 

      flash('Your comment has been added', 'success')  
    return redirect(url_for('event.show', id=event.id))
