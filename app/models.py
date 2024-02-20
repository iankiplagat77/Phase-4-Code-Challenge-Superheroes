from flask_sqlalchemy import SQLAlchemy  


db = SQLAlchemy()


class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    powers = db.relationship('Hero_Power', back_populates='hero', cascade='all, delete-orphan')

    def to_dict(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return {'id': self.id}  # or any other representation to break the recursion
        visited.add(self)
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'powers': [hero_power.to_dict(visited) for hero_power in self.powers]
        }


class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    heroes = db.relationship('Hero_Power', back_populates='power', cascade='all, delete-orphan')

    def to_dict(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return {'id': self.id}  # or any other representation to break the recursion
        visited.add(self)
        return {
            'id': self.id,
            'name': self.name,
            'heroes': [hero_power.to_dict(visited) for hero_power in self.heroes]
        }


class Hero_Power(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    strength = db.Column(db.String)
    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    def to_dict(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return {'id': self.id}  # or any other representation to break the recursion
        visited.add(self)
        return {
            'id': self.id,
            'power_id': self.power_id,
            'hero_id': self.hero_id,
            'strength': self.strength,
            'hero': self.hero.to_dict(visited),
            'power': self.power.to_dict(visited)
        }
