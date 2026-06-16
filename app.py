from flask import Flask, request, jsonify
from database import db
from flask_login import LoginManager, login_user
from models.user import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
#view login
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not (username and password):
        return jsonify({"message": "Credenciais inválidas"}), 400

    user = User.query.filter_by(username=username).first()
    
    if (not user) or (password != user.password):
        return jsonify({"message": "Credenciais inválidas"}), 400
    
    login_user(user)    
    return jsonify({"message": "Autenticação realizada com sucesso"})

@app.route("/hello_world", methods=["GET"])
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)