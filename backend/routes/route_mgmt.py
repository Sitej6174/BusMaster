from flask import Blueprint, request, jsonify
from models import db, Route, BusStop

routes_bp = Blueprint('route_mgmt', __name__)


@routes_bp.route('/', methods=['GET'])
def get_routes():
    routes = Route.query.all()
    return jsonify({'success': True, 'data': [r.to_dict() for r in routes]})


@routes_bp.route('/<int:route_id>', methods=['GET'])
def get_route(route_id):
    route = Route.query.get_or_404(route_id)
    return jsonify({'success': True, 'data': route.to_dict()})


@routes_bp.route('/', methods=['POST'])
def create_route():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    required = ['route_name', 'route_number', 'start_location', 'end_location']
    for field in required:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing field: {field}'}), 400

    if Route.query.filter_by(route_number=data['route_number']).first():
        return jsonify({'success': False, 'message': 'Route number already exists'}), 409

    route = Route(
        route_name=data['route_name'],
        route_number=data['route_number'],
        start_location=data['start_location'],
        end_location=data['end_location'],
        start_lat=data.get('start_lat'),
        start_lng=data.get('start_lng'),
        end_lat=data.get('end_lat'),
        end_lng=data.get('end_lng'),
        distance_km=data.get('distance_km'),
        estimated_duration_min=data.get('estimated_duration_min'),
        status=data.get('status', 'Active')
    )
    db.session.add(route)
    db.session.flush()  # get route.id

    # Add bus stops if provided
    stops_data = data.get('stops', [])
    for i, stop in enumerate(stops_data):
        bus_stop = BusStop(
            route_id=route.id,
            stop_name=stop.get('stop_name', f'Stop {i+1}'),
            stop_order=stop.get('stop_order', i + 1),
            lat=stop.get('lat'),
            lng=stop.get('lng')
        )
        db.session.add(bus_stop)

    db.session.commit()
    return jsonify({'success': True, 'data': route.to_dict(), 'message': 'Route created successfully'}), 201


@routes_bp.route('/<int:route_id>', methods=['PUT'])
def update_route(route_id):
    route = Route.query.get_or_404(route_id)
    data = request.get_json()

    route.route_name = data.get('route_name', route.route_name)
    route.route_number = data.get('route_number', route.route_number)
    route.start_location = data.get('start_location', route.start_location)
    route.end_location = data.get('end_location', route.end_location)
    route.start_lat = data.get('start_lat', route.start_lat)
    route.start_lng = data.get('start_lng', route.start_lng)
    route.end_lat = data.get('end_lat', route.end_lat)
    route.end_lng = data.get('end_lng', route.end_lng)
    route.distance_km = data.get('distance_km', route.distance_km)
    route.estimated_duration_min = data.get('estimated_duration_min', route.estimated_duration_min)
    route.status = data.get('status', route.status)

    db.session.commit()
    return jsonify({'success': True, 'data': route.to_dict(), 'message': 'Route updated successfully'})


@routes_bp.route('/<int:route_id>', methods=['DELETE'])
def delete_route(route_id):
    route = Route.query.get_or_404(route_id)
    db.session.delete(route)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Route deleted successfully'})


# Bus Stop endpoints
@routes_bp.route('/<int:route_id>/stops', methods=['POST'])
def add_stop(route_id):
    route = Route.query.get_or_404(route_id)
    data = request.get_json()

    stop = BusStop(
        route_id=route.id,
        stop_name=data['stop_name'],
        stop_order=data.get('stop_order', len(route.stops) + 1),
        lat=data.get('lat'),
        lng=data.get('lng')
    )
    db.session.add(stop)
    db.session.commit()
    return jsonify({'success': True, 'data': stop.to_dict(), 'message': 'Stop added'}), 201


@routes_bp.route('/<int:route_id>/stops/<int:stop_id>', methods=['DELETE'])
def delete_stop(route_id, stop_id):
    stop = BusStop.query.filter_by(id=stop_id, route_id=route_id).first_or_404()
    db.session.delete(stop)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Stop deleted'})
