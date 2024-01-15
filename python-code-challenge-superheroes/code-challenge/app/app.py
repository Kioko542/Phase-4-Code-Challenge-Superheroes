import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('db/app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/add-dummy')
def add_dummy():
    hero = Hero(name='Jojo', super_name='bamwilu')
    db.session.add(hero)
    db.session.commit()
    return "Hero added successfully!"

@app.route('/heroes', methods=['GET', 'POST'])
def handle_heroes():
    if request.method == 'GET':
        # Retrieve all heroes
        all_heroes = Hero.query.all()
        heroes_list = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in all_heroes]
        return jsonify(heroes_list)
    
    elif request.method == 'POST':
        # Add a new hero
        data = request.get_json()
        new_hero = Hero(name=data.get('name'), super_name=data.get('super_name'))

        try:
            db.session.add(new_hero)
            db.session.commit()
            return jsonify({"message": "Hero added successfully!", "id": new_hero.id}), 201  # 201 Created status
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to add hero. {str(e)}"}), 500  # Internal Server Error

@app.route('/heroes/<int:hero_id>', methods=['GET', 'PATCH'])
def handle_hero(hero_id):
    hero = Hero.query.get(hero_id)

    if hero:
        if request.method == 'GET':
            # Retrieve hero details
            hero_data = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [
                    {"id": hero_power.power.id, "name": hero_power.power.name, "description": hero_power.power.description}
                    for hero_power in hero.hero_powers
                ]
            }
            return jsonify(hero_data)
        
        elif request.method == 'PATCH':
            # Update hero details
            data = request.get_json()
            hero.name = data.get('name', hero.name)
            hero.super_name = data.get('super_name', hero.super_name)

            try:
                db.session.commit()
                return jsonify({"message": "Hero updated successfully!"})
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": f"Failed to update hero. {str(e)}"}), 500  # Internal Server Error
    else:
        return jsonify({"error": "Hero not found"}), 404

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    if 'strength' not in data or 'power_id' not in data or 'hero_id' not in data:
        return jsonify({"error": "Missing required fields"}), 400  # 400 Bad Request

    new_hero_power = HeroPower(strength=data.get('strength'), power_id=data.get('power_id'), hero_id=data.get('hero_id'))

    try:
        db.session.add(new_hero_power)
        db.session.commit()
        return jsonify({"message": "HeroPower created successfully!"}), 201  # 201 Created status
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create HeroPower. {str(e)}"}), 500  # Internal Server Error

if __name__ == '__main__':
    app.run(port=4000, debug=True)
