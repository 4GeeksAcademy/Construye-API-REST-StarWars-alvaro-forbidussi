import os
from flask_admin import Admin
from models import db, Usuario, Personaje, Planeta, Favorito
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Agregamos los 4 modelos al panel de administrador
    admin.add_view(ModelView(Usuario, db.session))
    admin.add_view(ModelView(Personaje, db.session))
    admin.add_view(ModelView(Planeta, db.session))
    admin.add_view(ModelView(Favorito, db.session))