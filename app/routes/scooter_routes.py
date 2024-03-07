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
        no_rentals_scooters = db.select(Scooter).where(~Scooter.rentals.has())
        unreturned_scooters = db.select(Scooter).join(Scooter.rentals).where(Rental.is_returned == False)
        returned_scooters = except_(scooter_query, unreturned_scooters)
        united = union(no_rentals_scooters, returned_scooters)
        scooter_query = scooter_query.from_statement(united)

    scooters = db.session.scalars(scooter_query)

    response = []
    for scooter in scooters:
        is_available = is_scooter_available(scooter.id)
        response.append(
            {
                "id": scooter.id,
                "is_available": is_available,
            }
        )
    return jsonify(response)

@bp.patch("/<scooter_id>/rent")
def rent_scooter(scooter_id):
    scooter = validate_model(Scooter, scooter_id)
    if not is_scooter_available(scooter_id):
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
        "scooter_id": scooter.id,
        "user_id": user.id,
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
        and Rental.user_id == user_id 
        and not Rental.is_returned
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
        "scooter_id": scooter.id,
        "user_id": user.id,
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

def is_scooter_available(id):
    rentals_query = db.select(
                            func.count()
                        ).select_from(
                            Rental
                        ).where(
                            Rental.scooter_id == id and not Rental.is_returned
                        )
    unreturned_rental_count = db.session.scalar(rentals_query)
    return unreturned_rental_count == 0

def is_user_eligible_to_rent(id):
    rentals_query = db.select(
                            func.count()
                        ).select_from(
                            Rental
                        ).where(
                            Rental.user_id == id and not Rental.is_returned
                        )
    unreturned_rental_count = db.session.scalar(rentals_query)
    return unreturned_rental_count == 0