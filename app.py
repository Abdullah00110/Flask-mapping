from flask import Flask, jsonify , request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(20) , unique=True , nullable = False)
    email = db.Column(db.String(120) , unique=True , nullable=False)
    profile = db.relationship('UserProfile' , backref='user' , uselist=False)


class UserProfile(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    bio = db.Column(db.String(200))
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'), unique=True , nullable=False)


# Crud Operations for user

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify({'users': users_list})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {'id': user.id, 'username': user.username, 'email': user.email}
    return jsonify({'user': user_data})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# Crud Operations for UserProfile


@app.route('/user_profile/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    profile = user.profile

    if not profile:
        return jsonify({'message': 'UserProfile not found for the user'}), 404

    profile_data = {'id': profile.id, 'bio': profile.bio, 'user_id': profile.user_id}
    return jsonify({'user_profile': profile_data}), 200

@app.route('/user_profile', methods=['POST'])
def create_user_profile():
    data = request.get_json()
    user_id = data.get('user_id')
    user = User.query.get_or_404(user_id)

    # Check if UserProfile already exists for the user
    if user.profile:
        return jsonify({'message': 'UserProfile already exists for the user'}), 400

    new_profile = UserProfile(bio=data['bio'], user=user)
    db.session.add(new_profile)
    db.session.commit()

    return jsonify({'message': 'UserProfile created successfully', 'user_profile_id': new_profile.id}), 201

@app.route('/user_profile/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    profile = user.profile

    if not profile:
        return jsonify({'message': 'UserProfile not found for the user'}), 404

    data = request.get_json()
    profile.bio = data['bio']
    db.session.commit()

    return jsonify({'message': 'UserProfile updated successfully'}), 200

@app.route('/user_profile/<int:user_id>', methods=['DELETE'])
def delete_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    profile = user.profile

    if not profile:
        return jsonify({'message': 'UserProfile not found for the user'}), 404

    db.session.delete(profile)
    db.session.commit()

    return jsonify({'message': 'UserProfile deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
