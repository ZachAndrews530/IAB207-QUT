from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    
    bootstrap = Bootstrap5(app)

    bcrypt = Bcrypt(app)

    app.secret_key = 'somerandomvalue'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)

    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import views
    app.register_blueprint(views.mainbp)
    from . import events
    app.register_blueprint(events.evntbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    return app

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html", error=e)

@app.context_processor
def get_context():
   year = datetime.datetime.today().year
   return dict(year=year)