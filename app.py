from flask import Flask, request, jsonify
from database import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
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
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not (username and password):
        return jsonify({"message": "Credenciais inválidas"}), 400

    user = User.query.filter_by(username=username).first()
    
    if (not user) or (password != user.password):
        return jsonify({"message": "Credenciais inválidas"}), 400
    
    login_user(user)    
    return jsonify({"message": "Autenticação realizada com sucesso"})

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"})

@app.route("/user", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not(username and password):
        return jsonify({"message": "Dados inválidos"}), 401

    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({"message": "Usuário já existe no sistema"}), 409
        
    new_user = User(username=username, password = password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso"})
    
@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)
    
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
        
    return jsonify({"username": user.username})
    
@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):    
    data = request.json
    user = User.query.get(id_user)
    
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    user.password = data.get("password")
    db.session.commit()
    
    return jsonify({"message": f"Usuário {id_user} atualizado com sucesso"})
    
@app.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):   
    if current_user.id == id_user:
        return jsonify({"message": "Deleção não permitida"}), 403
    
    user = User.query.get(id_user)
    
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": f"Usuário {id_user} deletado com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)