from flask import Blueprint, jsonify, request, abort, make_response
from ..db import db
from ..models.scooter import Scooter
from ..models.rental import Rental
from ..models.user import User
from sqlalchemy import func, union, except_

bp = Blueprint("scooters", __name__, url_prefix="/scooters")

@bp.get("")
def get_scooters():
    filter_query = bool(request.args.get("available_only"))
    scooter_query = db.select(Scooter)

    if filter_query:
        # Scooters with no rental history and acceptable battery charge
        no_rental_history = scooter_query.where(
                                ~Scooter.rentals.has()
                            ).where(
                                Scooter.charge_percent >= 15.0
                            )

        # For scooters with a rental history:
        # Determine which scooters have outstanding rentals or low battery
        unreturned = scooter_query.join(Scooter.rentals).where(
                        Rental.is_returned == False
                    )
        uncharged = scooter_query.where(Scooter.charge_percent <= 15.0)
        uncharged_or_unreturned = union(unreturned, uncharged)

        # Use set operations to get all scooters except uncharged or unreturned
        returned_and_charged = except_(scooter_query, uncharged_or_unreturned)
        all_available_scooters = union(no_rental_history, returned_and_charged)
        scooter_query = scooter_query.from_statement(all_available_scooters)

    scooters = db.session.scalars(scooter_query)

    response = []
    for scooter in scooters:
        is_available = is_scooter_available(scooter)
        response.append(
            {
                "id": scooter.id,
                "model": scooter.model,
                "charge_percent": scooter.charge_percent,
                "is_available": is_available,
            }
        )
    return jsonify(response)

@bp.patch("/<scooter_id>/rent")
def rent_scooter(scooter_id):
    scooter = validate_model(Scooter, scooter_id)
    if not is_scooter_available(scooter):
        return {"message": f"Scooter #{scooter_id} is not available"}

    request_body = request.get_json()
    user_id = request_body.get("user_id")
    if not user_id:
        response = {"message": "User id must be supplied"}
        abort(make_response(response , 400))

    user = validate_model(User, user_id)
    is_user_eligible = is_user_eligible_to_rent(user_id)
    if not is_user_eligible:
        return {"message": "User cannot rent a scooter at this time"}

    new_rental = Rental(user=user, scooter=scooter)
    db.session.add(new_rental)
    db.session.commit()

    return {
        "rental_id": new_rental.id,
        "user_id": user.id,
        "scooter_id": scooter.id,
        "model": scooter.model,
        "is_returned": False
    }

@bp.patch("/<scooter_id>/return")
def return_scooter(scooter_id):
    # Does the scooter exist
    scooter = validate_model(Scooter, scooter_id)

    # Does the user exist
    request_body = request.get_json()
    user_id = request_body.get("user_id")
    if not user_id:
        response = {"message": "User id must be supplied"}
        abort(make_response(response , 400))
    user = validate_model(User, user_id)

    # Is this scooter rented out to the user supplied?
    rental_query = db.select(Rental).where(
                                        Rental.scooter_id == scooter_id
                                    ).where(
                                        Rental.user_id == user_id
                                    ).where(
                                        Rental.is_returned == False
                                    )
    rental = db.session.scalar(rental_query)
    if not rental:
        response = {"message": "The requested transaction could not be completed"}
        abort(make_response(response , 400))

    # Return the scooter
    rental.is_returned = True
    db.session.commit()

    return {
        "rental_id": rental.id,
        "user_id": user.id,
        "scooter_id": scooter.id,
        "model": scooter.model,
        "is_returned": True
    }

def validate_model(cls, id):
    try:
        id = int(id)
    except:
        response = {"message": f"{cls.__name__} {id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == id)
    scooter = db.session.scalar(query)
    if scooter:
        return scooter

    response = {"message": f"{cls.__name__} {id} not found"}
    abort(make_response(response, 404))

def is_scooter_available(scooter):
    # A scooter is unavailable if the charge is 15% or less
    if scooter.charge_percent <= 15.0:
        return False

    rentals_query = db.select(
                            func.count()
                        ).select_from(
                            Rental
                        ).where(
                            Rental.scooter_id == scooter.id
                        ).where(Rental.is_returned == False)
    unreturned_rental_count = db.session.scalar(rentals_query)
    return unreturned_rental_count == 0

def is_user_eligible_to_rent(id):
    rentals_query = db.select(
                            func.count()
                        ).select_from(
                            Rental
                        ).where(
                            Rental.user_id == id
                        ).where(Rental.is_returned == False)
    unreturned_rental_count = db.session.scalar(rentals_query)
    return unreturned_rental_count == 0