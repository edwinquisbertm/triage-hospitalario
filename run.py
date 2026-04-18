from flask import Flask, redirect, url_for
from app.routes.registration import registration_bp
from app.routes.queue_routes import queue_bp
from app.routes.beds_routes import beds_bp
from app.routes.history_routes import history_bp
from app.models.data_store import init_data_store

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.secret_key = 'super_secret_triage_key_for_development'

    # Inicializar el almacenamiento en archivos JSON
    init_data_store()

    # Registrar blueprints
    app.register_blueprint(registration_bp, url_prefix='/')
    app.register_blueprint(queue_bp, url_prefix='/queue')
    app.register_blueprint(beds_bp, url_prefix='/beds')
    app.register_blueprint(history_bp, url_prefix='/history')

    @app.errorhandler(404)
    def not_found(e):
        return redirect(url_for('registration.register'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
