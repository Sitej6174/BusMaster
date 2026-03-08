from flask import Flask, send_from_directory
from flask_cors import CORS
from models import db
from routes.buses import buses_bp
from routes.drivers import drivers_bp
from routes.route_mgmt import routes_bp
from routes.schedules import schedules_bp
from routes.dashboard import dashboard_bp
import os

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static')
    )

    # Config
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'busmaster.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'busmaster-secret-2024'

    CORS(app)
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(buses_bp, url_prefix='/api/buses')
    app.register_blueprint(drivers_bp, url_prefix='/api/drivers')
    app.register_blueprint(routes_bp, url_prefix='/api/routes')
    app.register_blueprint(schedules_bp, url_prefix='/api/schedules')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    # Frontend routes
    from flask import render_template
    @app.route('/')
    def index():
        return render_template('dashboard.html')

    @app.route('/buses')
    def buses_page():
        return render_template('buses.html')

    @app.route('/drivers')
    def drivers_page():
        return render_template('drivers.html')

    @app.route('/routes')
    def routes_page():
        return render_template('routes.html')

    @app.route('/schedules')
    def schedules_page():
        return render_template('schedules.html')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
