#!/usr/bin/env python3

import random
from app import app, db
from models import Hero, Power, HeroPower

def seed_powers():
    # Implement your power seeding logic here
    powers_data = [
        {"name": "Super Strength", "description": "Gives the wielder super-human strengths"},
        {"name": "Flight", "description": "Gives the wielder the ability to fly at supersonic speed"},
        {"name": "Super Human Senses", "description": "Allows the wielder to use senses at a super-human level"},
        {"name": "Elasticity", "description": "Can stretch the human body to extreme lengths"}
    ]

    for power_data in powers_data:
        new_power = Power(**power_data)
        db.session.add(new_power)

    db.session.commit()

def seed_heroes():
    # Implement your hero seeding logic here
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    for hero_data in heroes_data:
        new_hero = Hero(**hero_data)
        db.session.add(new_hero)

    db.session.commit()

def add_powers_to_heroes():
    print("🦸‍♀️ Adding powers to heroes...")
    strengths = ["Strong", "Weak", "Average"]

    # Query all heroes and powers
    heroes = Hero.query.all()
    powers = Power.query.all()

    for hero in heroes:
        for _ in range(random.randint(1, 3)):
            # get a random power
            power = random.choice(powers)
            strength = random.choice(strengths)

            hero_power = HeroPower(hero=hero, power=power, strength=strength)
            db.session.add(hero_power)

    db.session.commit()

def main():
    with app.app_context():
        # Uncomment the following line if you need to create the tables
        db.create_all()

        seed_powers()
        seed_heroes()
        add_powers_to_heroes()
        print("🦸‍♀️ Done seeding!")

if __name__ == '__main__':
    main()
