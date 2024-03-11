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
    one = Scooter(model="Speedster VII", charge_percent=25.0)
    two = Scooter(model="Nimbus Sparkle", charge_percent=100.0)
    three = Scooter(model="Thunderbolt III", charge_percent=78.5)

    db.session.add_all([one, two, three])
    db.session.commit()

@pytest.fixture
def scooter_rented_twice(app, three_scooters):
    user_one = User(name="User One", email="one@email.com", phone="(555) 555-1234")
    db.session.add(user_one)

    rental_one = Rental(user=user_one, scooter_id=1, is_returned=True)
    rental_two = Rental(user=user_one, scooter_id=1)
    db.session.add_all([rental_one, rental_two])

    db.session.commit()

@pytest.fixture
def two_users(app, scooter_rented_twice):
    user_two = User(name="User Two", email="two@email.com", phone="(555) 555-4321")
    db.session.add(user_two)    
    db.session.commit()

@pytest.fixture
def three_scooters_two_rentals_one_returned(app, two_users):
    rental = Rental(user_id=2, scooter_id=2, is_returned=True)
    db.session.add_all([rental])

    db.session.commit()

@pytest.fixture
def low_charge_scooter(app, three_scooters_two_rentals_one_returned):
    scooter = Scooter(model="Nauseator X", charge_percent=10.5)
    db.session.add(scooter)    
    db.session.commit()