from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import pandas as pd
from io import BytesIO
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
    db.Column('teams_name', db.String(100), db.ForeignKey('teams.name'), primary_key=True),
    db.Column('locked', db.Boolean, default=False)
)

# Team Model/Schema
class Team(db.Model):
    __tablename__ = 'teams'  # Specify the table name here
    name = db.Column(db.String(100), unique=True, primary_key=True)
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
    num_companies = db.Column(db.Integer)
    num_periods = db.Column(db.Integer)
    offset = db.Column(db.Integer)
    num_markets = db.Column(db.Integer)
    num_cells = db.Column(db.Integer)
    market_0_activation = db.Column(db.Integer)
    market_1_activation = db.Column(db.Integer)
    market_2_activation = db.Column(db.Integer)
    market_3_activation = db.Column(db.Integer)
    ideal_rd = db.Column(db.Integer)
    cost_industry_report = db.Column(db.Float)
    cost_market_report = db.Column(db.Float)
    current_period = db.Column(db.Integer, default=0)

    # Relationships
    teams = db.relationship('Team', secondary=GameTeamAssociation, lazy='subquery',
                            backref=db.backref('games', lazy=True))
    turns = db.relationship('Turn', back_populates='game')


class GameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'status', 'current_period')

game_schema = GameSchema()
games_schema = GameSchema(many=True)

# Turn Model/Schema
class Turn(db.Model):
    __tablename__ = 'turns'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    turn_number = db.Column(db.Integer, nullable=False)
    submission_time = db.Column(db.DateTime, default=func.current_timestamp())
    team_name = db.Column(db.String(100), db.ForeignKey('teams.name'))
    inputSolidVerkaufspreisInland = db.Column(db.Float)
    inputIdealVerkaufspreisInland = db.Column(db.Float)
    inputSolidVerkaufspreisAusland = db.Column(db.Float)
    inputIdealVerkaufspreisAusland = db.Column(db.Float)
    inputSolidFETechnik = db.Column(db.Float)
    inputIdealFETechnik = db.Column(db.Float)
    inputSolidFEHaptik = db.Column(db.Float)
    inputIdealFEHaptik = db.Column(db.Float)
    inputSolidProduktwerbungInland = db.Column(db.Float)
    inputIdealProduktwerbungInland = db.Column(db.Float)
    inputSolidProduktwerbungAusland = db.Column(db.Float)
    inputIdealProduktwerbungAusland = db.Column(db.Float)
    inputSolidPR = db.Column(db.Float)
    inputIdealPR = db.Column(db.Float)
    inputSolidLiefermengeSondermarkt = db.Column(db.Float)
    inputIdealLiefermengeSondermarkt = db.Column(db.Float)
    inputSolidLiefermengeAusland = db.Column(db.Float)
    inputIdealLiefermengeAusland = db.Column(db.Float)
    inputSolidVertriebspersonalInland = db.Column(db.Float)
    inputIdealVertriebspersonalInland = db.Column(db.Float)
    inputSolidVertriebspersonalAusland = db.Column(db.Float)
    inputIdealVertriebspersonalAusland = db.Column(db.Float)
    inputSolidHilfsstoffe = db.Column(db.Float)
    inputIdealHilfsstoffe = db.Column(db.Float)
    inputSolidMaterialS = db.Column(db.Float)
    inputMaterialI = db.Column(db.Float)
    inputFertigungspersonal = db.Column(db.Float)
    inputPersonalentwicklung = db.Column(db.Float)
    inputGehaltsaufschlag = db.Column(db.Float)
    inputInvestitionenBGA = db.Column(db.Float)
    sumFETechnik = db.Column(db.Float)
    sumFEHaptik = db.Column(db.Float)
    sumProduktbewerbungInland = db.Column(db.Float)
    sumProduktbewerbungAusland = db.Column(db.Float)
    sumPR = db.Column(db.Float)
    sumLiefermengeSondermarkt = db.Column(db.Float)
    sumLiefermengeAusland = db.Column(db.Float)
    sumVertriebspersonalInland = db.Column(db.Float)
    sumVertriebspersonalAusland = db.Column(db.Float)
    sumBetriebsstoffe = db.Column(db.Float)
    sumMaterialS = db.Column(db.Float)
    sumMaterialI = db.Column(db.Float)
    gesamtFertigungspersonal = db.Column(db.Float)
    gesamtPersonalentwicklung = db.Column(db.Float)
    gesamtGehaltsaufschlag = db.Column(db.Float)
    gesamtInvestitionenBGA = db.Column(db.Float)
    is_template = db.Column(db.Boolean, default=False, nullable=False)

    # Define the relationship with the Game model
    game = db.relationship('Game', back_populates='turns')

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
    password = request.json.get('password', 'defaultPassword')  # It's better to generate a random password

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

    # Extract game details from the request
    name = request.json.get('name')
    status = request.json.get('status', 'pending')
    num_companies = request.json.get('num_companies')
    num_periods = request.json.get('num_periods')
    offset = request.json.get('offset')
    num_markets = request.json.get('num_markets')
    num_cells = request.json.get('num_cells')
    market_0_activation = request.json.get('market_0_activation')
    market_1_activation = request.json.get('market_1_activation')
    market_2_activation = request.json.get('market_2_activation')
    market_3_activation = request.json.get('market_3_activation')
    ideal_rd = request.json.get('ideal_rd')
    cost_industry_report = request.json.get('cost_industry_report')
    cost_market_report = request.json.get('cost_market_report')

    # Create new game instance with all the fields
    new_game = Game(
        name=name,
        status=status,
        num_companies=num_companies,
        num_periods=num_periods,
        offset=offset,
        num_markets=num_markets,
        num_cells=num_cells,
        market_0_activation=market_0_activation,
        market_1_activation=market_1_activation,
        market_2_activation=market_2_activation,
        market_3_activation=market_3_activation,
        ideal_rd=ideal_rd,
        cost_industry_report=cost_industry_report,
        cost_market_report=cost_market_report
    )

    # Save the new game to the database
    db.session.add(new_game)
    db.session.flush()

    # Retrieve team IDs from the request and associate them with the game
    team_names = request.json.get('team_names', [])
    for team_name in team_names:
        team = Team.query.get(team_name)
        if team:
            new_game.teams.append(team)

    db.session.commit()

    return jsonify({"msg": "Game created successfully", "game_id": new_game.id}), 201

@app.route('/game/<int:game_id>', methods=['PUT'])
@jwt_required()
def update_game(game_id):
    game = Game.query.get_or_404(game_id)

    # Update fields
    game.name = request.json.get('name', game.name)
    game.status = request.json.get('status', game.status)
    game.num_companies = request.json.get('num_companies', game.num_companies)
    game.num_periods = request.json.get('num_periods', game.num_periods)
    game.offset = request.json.get('offset', game.offset)
    game.num_markets = request.json.get('num_markets', game.num_markets)
    game.num_cells = request.json.get('num_cells', game.num_cells)
    game.market_0_activation = request.json.get('market_0_activation', game.market_0_activation)
    game.market_1_activation = request.json.get('market_1_activation', game.market_1_activation)
    game.market_2_activation = request.json.get('market_2_activation', game.market_2_activation)
    game.market_3_activation = request.json.get('market_3_activation', game.market_3_activation)
    game.ideal_rd = request.json.get('ideal_rd', game.ideal_rd)
    game.cost_industry_report = request.json.get('cost_industry_report', game.cost_industry_report)
    game.cost_market_report = request.json.get('cost_market_report', game.cost_market_report)

    db.session.commit()

    return game_schema.jsonify(game)


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
            'teams': [{'name': team.name} for team in game.teams]
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
            'name': team.name,
            'games': [{'id': game.id, 'name': game.name} for game in team.games]
        }
        teams_data.append(team_info)
    return jsonify(teams_data)

@app.route('/teams/<string:team_name>', methods=['DELETE'])
@jwt_required()
def delete_team(team_name):
    team = Team.query.get_or_404(team_name)
    db.session.delete(team)
    db.session.commit()
    return jsonify({'message': 'Team deleted successfully'}), 200

@app.route('/teams/<string:team_name>/change_password', methods=['PUT'])
@jwt_required()
def change_team_password(team_name):
    team = Team.query.filter_by(name=team_name).first_or_404()

    # Extract new password from the request
    new_password = request.json.get('password', None)

    if new_password is None:
        return jsonify({'message': 'New password not provided'}), 400

    # Update the team's password
    team.password = new_password
    db.session.commit()

    return jsonify({'message': f'Password for team {team_name} updated successfully'}), 200


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

# player routes
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        data = pd.read_excel(uploaded_file)
        return jsonify(data.to_dict(orient='records'))

@app.route('/save', methods=['POST'])
def save_file():
    data = request.json
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, attachment_filename='updated_file.xlsx', as_attachment=True)

@app.route('/games-for-team', methods=['GET'])
@jwt_required()
def get_games_for_team():
    current_user = get_jwt_identity()
    team = Team.query.filter_by(name=current_user).first()
    if team:
        games = Game.query.filter(Game.teams.any(name=team.name)).all()
        return jsonify(games_schema.dump(games))
    else:
        return jsonify({"msg": "Team not found"}), 404

@app.route('/check-lock-status', methods=['GET'])
@jwt_required()
def check_lock_status():
    current_team = request.args.get('teamname')
    game_id = request.args.get('game_id')

    # Query the GameTeamAssociation
    game_team = db.session.query(GameTeamAssociation).filter(
        GameTeamAssociation.c.teams_name == current_team,
        GameTeamAssociation.c.game_id == game_id
    ).first()

    if game_team:
        return jsonify({'locked': game_team.locked})
    else:
        return jsonify({'message': 'Game or team not found'}), 404


@app.route('/lock-team', methods=['POST'])
@jwt_required()
def lock_team():
    team_name = request.json.get('team_name')
    game_id = request.json.get('game_id')

    try:
        sql = text("UPDATE gameteams SET locked = 1 WHERE game_id = :game_id AND teams_name = :team_name")
        with db.engine.begin() as connection:  # This ensures a transaction is begun and committed
            connection.execute(sql, {'game_id': game_id, 'team_name': team_name})

        return jsonify({'message': 'Team locked successfully'}), 200
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")  # Log the error
        return jsonify({'error': 'Database update failed'}), 500

@app.route('/unlock-team', methods=['POST'])
@jwt_required()
def unlock_team():
    team_name = request.json.get('team_name')
    game_id = request.json.get('game_id')

    sql = text("UPDATE gameteams SET locked = 0 WHERE game_id = :game_id AND teams_name = :team_name")
    with db.engine.connect() as connection:
        connection.execute(sql, {'game_id': game_id, 'team_name': team_name})

    return jsonify({'message': 'Team unlocked successfully'}), 200

@app.route('/submit-turn', methods=['POST'])
@jwt_required()
def submit_turn():
    current_team = get_jwt_identity()  # Get the team name from the JWT token
    game_id = request.json.get('game_id')  # Extract the game ID from the request

    # Check the lock status for the team and game combination
    game_team = db.session.query(GameTeamAssociation).filter(
        GameTeamAssociation.c.teams_name == current_team,
        GameTeamAssociation.c.game_id == game_id
    ).first()

    if game_team and game_team.locked:
        return jsonify({"message": "Submission locked for this team"}), 403

    new_turn = Turn(
        game_id=game_id,
        turn_number=request.json.get('turn_number'),
        team_name=current_team,
        inputSolidVerkaufspreisAusland=request.json.get('inputSolidVerkaufspreisAusland'),
        inputIdealVerkaufspreisAusland=request.json.get('inputIdealVerkaufspreisAusland'),
        inputSolidVerkaufspreisInland=request.json.get('inputSolidVerkaufspreisInland'),
        inputIdealVerkaufspreisInland=request.json.get('inputIdealVerkaufspreisInland'),
        inputSolidFETechnik=request.json.get('inputSolidFETechnik'),
        inputIdealFETechnik=request.json.get('inputIdealFETechnik'),
        inputSolidFEHaptik=request.json.get('inputSolidFEHaptik'),
        inputIdealFEHaptik=request.json.get('inputIdealFEHaptik'),
        inputSolidProduktwerbungInland=request.json.get('inputSolidProduktwerbungInland'),
        inputIdealProduktwerbungInland=request.json.get('inputIdealProduktwerbungInland'),
        inputSolidProduktwerbungAusland=request.json.get('inputSolidProduktwerbungAusland'),
        inputIdealProduktwerbungAusland=request.json.get('inputIdealProduktwerbungAusland'),
        inputSolidPR=request.json.get('inputSolidPR'),
        inputIdealPR=request.json.get('inputIdealPR'),
        inputSolidLiefermengeSondermarkt=request.json.get('inputSolidLiefermengeSondermarkt'),
        inputIdealLiefermengeSondermarkt=request.json.get('inputIdealLiefermengeSondermarkt'),
        inputSolidLiefermengeAusland=request.json.get('inputSolidLiefermengeAusland'),
        inputIdealLiefermengeAusland=request.json.get('inputIdealLiefermengeAusland'),
        inputSolidVertriebspersonalInland=request.json.get('inputSolidVertriebspersonalInland'),
        inputIdealVertriebspersonalInland=request.json.get('inputIdealVertriebspersonalInland'),
        inputSolidVertriebspersonalAusland=request.json.get('inputSolidVertriebspersonalAusland'),
        inputIdealVertriebspersonalAusland=request.json.get('inputIdealVertriebspersonalAusland'),
        inputSolidHilfsstoffe=request.json.get('inputSolidHilfsstoffe'),
        inputIdealHilfsstoffe=request.json.get('inputIdealHilfsstoffe'),
        inputSolidMaterialS=request.json.get('inputSolidMaterialS'),
        inputMaterialI=request.json.get('inputMaterialI'),
        inputFertigungspersonal=request.json.get('inputFertigungspersonal'),
        inputPersonalentwicklung=request.json.get('inputPersonalentwicklung'),
        inputGehaltsaufschlag=request.json.get('inputGehaltsaufschlag'),
        inputInvestitionenBGA=request.json.get('inputInvestitionenBGA'),
        sumFETechnik=request.json.get('sumFETechnik'),
        sumFEHaptik=request.json.get('sumFEHaptik'),
        sumProduktbewerbungInland=request.json.get('sumProduktbewerbungInland'),
        sumProduktbewerbungAusland=request.json.get('sumProduktbewerbungAusland'),
        sumPR=request.json.get('sumPR'),
        sumLiefermengeSondermarkt=request.json.get('sumLiefermengeSondermarkt'),
        sumLiefermengeAusland=request.json.get('sumLiefermengeAusland'),
        sumVertriebspersonalInland=request.json.get('sumVertriebspersonalInland'),
        sumVertriebspersonalAusland=request.json.get('sumVertriebspersonalAusland'),
        sumBetriebsstoffe=request.json.get('sumBetriebsstoffe'),
        sumMaterialS=request.json.get('sumMaterialS'),
        sumMaterialI=request.json.get('sumMaterialI'),
        gesamtFertigungspersonal=request.json.get('gesamtFertigungspersonal'),
        gesamtPersonalentwicklung=request.json.get('gesamtPersonalentwicklung'),
        gesamtGehaltsaufschlag=request.json.get('gesamtGehaltsaufschlag'),
        gesamtInvestitionenBGA=request.json.get('gesamtInvestitionenBGA'),
    )

    db.session.add(new_turn)
    db.session.commit()

    return jsonify({"message": "Turn submitted successfully"}), 201



# Run Server
if __name__ == '__main__':
    app.run(debug=True)