from flask import Flask
from faker import Faker
import random
from sqlalchemy.orm import sessionmaker
from models import Hero, Power, Hero_Power, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Adjust the URI based on your database setup
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        # Use the Flask-SQLAlchemy engine from the app
        engine = db.engine

        # Create a session using the Flask-SQLAlchemy sessionmaker
        Session = sessionmaker(bind=engine)
        session = Session()

        # Delete existing data
        session.query(Hero).delete()
        session.query(Power).delete()
        session.query(Hero_Power).delete()
        session.commit()

        fake = Faker()

        # Create and commit heroes
        heroes = [
            Hero(name=fake.name(), super_name=fake.name())
            for _ in range(50)
        ]
        session.bulk_save_objects(heroes)
        session.commit()

        # Create and commit powers
        powers = [
            Power(name=fake.word())
            for _ in range(12)
        ]
        session.bulk_save_objects(powers)
        session.commit()

        # Create hero_powers
        hero_powers = []
        for hero in heroes:
            for _ in range(random.randint(1, 3)):
                power = random.choice(powers)
                hero_power = Hero_Power(
                    power=power,
                    hero=hero,
                    strength=fake.word()
                )
                session.add(hero_power)
                session.commit()

        session.close()