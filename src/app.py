# app.py

from flask import Flask
import flask_session
from settings import config_by_name
from routes.main import main
from routes.login import login_bp
from routes.logout import logout_bp
from routes.smc import smc_bp
from routes.oef import oef_bp
from routes.roi import roi_bp


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.secret_key = app.config.get('SECRET_KEY', 'mysecretkey')
    app.config['SESSION_TYPE'] = 'filesystem'
    session = flask_session.Session()
    session.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(smc_bp)
    app.register_blueprint(oef_bp)
    app.register_blueprint(roi_bp)

    return app


env_name = "dev"  # or "prod"
app = create_app(env_name)

if __name__ == '__main__':
    app.run(debug=True)
