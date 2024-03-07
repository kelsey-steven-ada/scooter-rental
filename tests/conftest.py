import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from app.models.user import User
from app.models.scooter import Scooter
from app.models.rental import Rental

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def three_scooters(app):
    one = Scooter()
    two = Scooter()
    three = Scooter()

    db.session.add_all([one, two, three])
    db.session.commit()

@pytest.fixture
def scooter_rented_twice(app, three_scooters):
    user_one = User(name="User One")
    db.session.add(user_one)

    rental_one = Rental(user=user_one, scooter_id=1, is_returned=True)
    rental_two = Rental(user=user_one, scooter_id=1)
    db.session.add_all([rental_one, rental_two])

    db.session.commit()

@pytest.fixture
def two_users(app, scooter_rented_twice):
    user_two = User(name="User One")
    db.session.add(user_two)    
    db.session.commit()
