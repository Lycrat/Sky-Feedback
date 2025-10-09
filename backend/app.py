import flask
from routes import questionnaire_route

def create_app():
    # Initialize the Flask application
    app = flask.Flask(__name__)
    
    app.register_blueprint(questionnaire_route.questionnaire_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)