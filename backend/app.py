import flask
from backend.routes.questionnaire_route import questionnaire_bp
from backend.routes.user_route import user_bp

def create_app():
    # Initialize the Flask application
    app = flask.Flask(__name__)
    
    app.register_blueprint(questionnaire_bp)
    app.register_blueprint(user_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)