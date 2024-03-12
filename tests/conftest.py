import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from app.models.customer import Customer
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
    user_one = Customer(name="User One", email="one@email.com", phone="(555) 555-1234")
    db.session.add(user_one)

    rental_one = Rental(customer=user_one, scooter_id=1, is_returned=True)
    rental_two = Rental(customer=user_one, scooter_id=1)
    db.session.add_all([rental_one, rental_two])

    db.session.commit()

@pytest.fixture
def two_users(app, scooter_rented_twice):
    user_two = Customer(name="User Two", email="two@email.com", phone="(555) 555-4321")
    db.session.add(user_two)    
    db.session.commit()

@pytest.fixture
def three_scooters_two_rentals_one_returned(app, two_users):
    rental = Rental(customer_id=2, scooter_id=2, is_returned=True)
    db.session.add_all([rental])

    db.session.commit()

@pytest.fixture
def low_charge_scooter(app, three_scooters_two_rentals_one_returned):
    scooter = Scooter(model="Nauseator X", charge_percent=10.5)
    db.session.add(scooter)    
    db.session.commit()

@pytest.fixture
def create_challenge_data(app):
    scooters = [
        Scooter(model="Thunderbolt DX", charge_percent=25.6),
        Scooter(model="Thunderbolt DX", charge_percent=15.3),
        Scooter(model="Thunderbolt DX", charge_percent=89.2),
        Scooter(model="Thunderbolt DX+", charge_percent=14.0),
        Scooter(model="Thunderbolt DX+", charge_percent=58.4),

        Scooter(model="Speedster IV", charge_percent=52.0),
        Scooter(model="Speedster IV", charge_percent=27.3),
        Scooter(model="Speedster V", charge_percent=76.0),
        Scooter(model="Speedster VI", charge_percent=42.2),
        Scooter(model="Speedster VII", charge_percent=61.0),

        Scooter(model="Nimbus Sparkle", charge_percent=92.5),
        Scooter(model="Nimbus Sparkle", charge_percent=88.0),
        Scooter(model="Nimbus Sparkle+", charge_percent=74.2),
        Scooter(model="Nimbus Rocket", charge_percent=70.0),
        Scooter(model="Nimbus Rocket", charge_percent=53.7),

        Scooter(model="Starlight V70", charge_percent=7.5),
        Scooter(model="Starlight V70", charge_percent=82.5),
        Scooter(model="Starlight V75", charge_percent=50.8),
        Scooter(model="Starlight V75", charge_percent=28.0),
        Scooter(model="Starlight V80", charge_percent=36.7),

        Scooter(model="Shadow Scream", charge_percent=9.2),
        Scooter(model="Shadow Scream", charge_percent=12.5),
        Scooter(model="Shadow Scream", charge_percent=45.0),
        Scooter(model="Shadow Scream", charge_percent=48.9),
        Scooter(model="Shadow Scream", charge_percent=34.6),
                
        Scooter(model="Trail Blazer A", charge_percent=33.3),
        Scooter(model="Trail Blazer A", charge_percent=47.2),
        Scooter(model="Trail Blazer XY", charge_percent=75.4),
        Scooter(model="Trail Blazer Z", charge_percent=35.2),
        Scooter(model="Trail Blazer Z+", charge_percent=84.6),
    ]
    db.session.add_all(scooters)

    users = [
        Customer(name="User One", email="One@email.com", phone="(555) 555-1111"),
        Customer(name="User Two", email="Two@email.com", phone="(555) 555-2222"),
        Customer(name="User Three", email="Three@email.com", phone="(555) 555-3333"),
        Customer(name="User Four", email="Four@email.com", phone="(555) 555-4444"),
        Customer(name="User Five", email="Five@email.com", phone="(555) 555-5555"),
        Customer(name="User Six", email="Six@email.com", phone="(555) 555-6666"),
        Customer(name="User Seven", email="Seven@email.com", phone="(555) 555-7777"),
        Customer(name="User Eight", email="Eight@email.com", phone="(555) 555-8888"),
        Customer(name="User Nine", email="Nine@email.com", phone="(555) 555-9999"),
        Customer(name="User Ten", email="Ten@email.com", phone="(555) 555-0000"),
    ]
    db.session.add_all(users)

    rentals = [
        Rental(customer_id=1, scooter_id=2, is_returned=True),
        Rental(customer_id=1, scooter_id=3, is_returned=True),
        Rental(customer_id=1, scooter_id=4, is_returned=True),
        Rental(customer_id=1, scooter_id=5, is_returned=False),

        Rental(customer_id=2, scooter_id=13, is_returned=True),
        Rental(customer_id=2, scooter_id=15, is_returned=True),
        Rental(customer_id=2, scooter_id=18, is_returned=True),

        Rental(customer_id=3, scooter_id=15, is_returned=True),
        Rental(customer_id=3, scooter_id=22, is_returned=False),

        Rental(customer_id=4, scooter_id=8, is_returned=True),
        Rental(customer_id=4, scooter_id=27, is_returned=True),
        Rental(customer_id=4, scooter_id=3, is_returned=True),

        Rental(customer_id=5, scooter_id=9, is_returned=True),
        Rental(customer_id=5, scooter_id=16, is_returned=False),

        Rental(customer_id=6, scooter_id=1, is_returned=True),
        Rental(customer_id=6, scooter_id=20, is_returned=True),

        Rental(customer_id=7, scooter_id=28, is_returned=False),

        Rental(customer_id=8, scooter_id=11, is_returned=True),
        Rental(customer_id=8, scooter_id=14, is_returned=False),

        Rental(customer_id=10, scooter_id=6, is_returned=True),
    ]
    db.session.add_all(rentals)

    db.session.commit()
