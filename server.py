from flask_app import app
from flask_app.controllers import register_login_controller, user_controller, user_skeptic_controller

if __name__ == '__main__':
    app.run(debug=True)