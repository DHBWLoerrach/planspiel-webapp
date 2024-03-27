from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from datetime import datetime
from flask_cors import CORS

# Initialize app
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Ensure this is set
jwt = JWTManager(app)
CORS(app, supports_credentials=True)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/<path:filename>')
def frontend_files(filename):
    return send_from_directory('Frontend/test', filename)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/GameSimulationDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT Secret Key
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

# Init db, marshmallow, and JWT
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

GameTeamAssociation = db.Table('gameteams',
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True)
)

# Team Model/Schema
class Team(db.Model):
    __tablename__ = 'teams'  # Specify the table name here
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class TeamSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)


# Game Model/Schema
class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(100))

    # Define the many-to-many relationship
    teams = db.relationship('Team', secondary=GameTeamAssociation, lazy='subquery',
                            backref=db.backref('games', lazy=True))


class GameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'status')

game_schema = GameSchema()
games_schema = GameSchema(many=True)

# Turn Model/Schema
class Turn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    turn_number = db.Column(db.Integer)
    submission_time = db.Column(db.DateTime, default=datetime.utcnow)

class TurnSchema(ma.Schema):
    class Meta:
        fields = ('id', 'game_id', 'turn_number', 'submission_time')

turn_schema = TurnSchema()
turns_schema = TurnSchema(many=True)

# Register Team
@app.route('/team', methods=['POST'])
def register_team():
    name = request.json['name']
    password = request.json['password']

    new_team = Team(name=name, password=password)

    db.session.add(new_team)
    db.session.commit()

    return team_schema.jsonify(new_team)

# Team Login
@app.route('/login', methods=['POST'])
def login():
    name = request.json.get('name', None)
    password = request.json.get('password', None)

    team = Team.query.filter_by(name=name).first()
    if team and team.password == password:
        access_token = create_access_token(identity=name)
        is_gamemaster = name.lower() == "gamemaster"
        return jsonify(access_token=access_token, is_gamemaster=is_gamemaster), 200

    return jsonify({"msg": "Invalid team name or password"}), 401

@app.route('/gamemaster', methods=['GET'])
@jwt_required()
def gamemaster():
    current_user = get_jwt_identity()
    if current_user.lower() != 'gamemaster':
        return jsonify({"msg": "Unauthorized access"}), 401

    # Prepare data for Game Master, like a list of teams, games, etc.
    # This is an example. Modify according to your application's needs.
    games = Game.query.all()
    return jsonify(games=games_schema.dump(games))


@app.route('/gamemaster/register_team', methods=['POST'])
@jwt_required()
def register_team_by_gamemaster():
    current_user = get_jwt_identity()
    if current_user.lower() != 'gamemaster':
        return jsonify({"msg": "Unauthorized access"}), 401

    # Get team data from the request
    name = request.json['name']
    # Optionally set a default password or create one
    password = 'defaultPassword'  # It's better to generate a random password

    # Check if team already exists
    existing_team = Team.query.filter_by(name=name).first()
    if existing_team:
        return jsonify({"msg": "Team already exists"}), 409

    # Create new team
    new_team = Team(name=name, password=password)
    db.session.add(new_team)
    db.session.commit()

    return jsonify({"msg": "Team registered successfully"}), 201

@app.route('/gamemaster/register_game', methods=['POST'])
@jwt_required()
def register_game():
    # Check if the logged-in user is the Game Master
    current_user = get_jwt_identity()
    if current_user.lower() != 'gamemaster':
        return jsonify({"msg": "Unauthorized access"}), 401

    # Extract game details and team IDs from the request
    name = request.json.get('name')
    status = request.json.get('status', 'pending')  # Default status
    team_ids = request.json.get('team_ids', [])  # List of team IDs

    # Create new game instance
    new_game = Game(name=name, status=status)

    # Attach teams to the game
    for team_id in team_ids:
        team = Team.query.get(team_id)
        if team:
            new_game.teams.append(team)

    # Save the new game to the database
    db.session.add(new_game)
    db.session.commit()

    return jsonify({"msg": "Game created successfully", "game_id": new_game.id}), 201


# Create a Game
@app.route('/game', methods=['POST'])
def add_game():
    name = request.json['name']
    status = request.json['status']

    new_game = Game(name=name, status=status)

    db.session.add(new_game)
    db.session.commit()

    return game_schema.jsonify(new_game)

@app.route('/game/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
        return jsonify({'message': 'Game deleted successfully'}), 200
    else:
        return jsonify({'message': 'Game not found'}), 404


@app.route('/games', methods=['GET'])
@jwt_required()
def get_games():
    games = Game.query.all()
    games_data = []
    for game in games:
        games_data.append({
            'id': game.id,
            'name': game.name,
            'status': game.status,
            'teams': [{'id': team.id, 'name': team.name} for team in game.teams]
        })
    return jsonify(games_data)


@app.route('/teams', methods=['GET'])
@jwt_required()
def get_teams():
    # Assuming 'gamemaster' is the name of the Game Master's team
    teams = Team.query.filter(Team.name != 'gamemaster').all()
    teams_data = []
    for team in teams:
        team_info = {
            'id': team.id,
            'name': team.name,
            'games': [{'id': game.id, 'name': game.name} for game in team.games]
        }
        teams_data.append(team_info)
    return jsonify(teams_data)

@app.route('/teams/<int:team_id>', methods=['DELETE'])
@jwt_required()
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return jsonify({'message': 'Team deleted successfully'}), 200

# Create a Turn
@app.route('/turn', methods=['POST'])
@jwt_required()
def add_turn():
    game_id = request.json['game_id']
    turn_number = request.json['turn_number']

    new_turn = Turn(game_id=game_id, turn_number=turn_number)

    db.session.add(new_turn)
    db.session.commit()

    return turn_schema.jsonify(new_turn)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)