import flask
from routes.questionnaire_route import questionnaire_bp
from routes.user_route import user_bp
from flask_cors import CORS

def create_app():
    # Initialize the Flask application
    app = flask.Flask(__name__)
    
    CORS(app)
    app.register_blueprint(questionnaire_bp)
    app.register_blueprint(user_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)