from flask import Blueprint, request, jsonify
from models import db, Bus

buses_bp = Blueprint('buses', __name__)


@buses_bp.route('/', methods=['GET'])
def get_buses():
    buses = Bus.query.all()
    return jsonify({'success': True, 'data': [b.to_dict() for b in buses]})


@buses_bp.route('/<int:bus_id>', methods=['GET'])
def get_bus(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    return jsonify({'success': True, 'data': bus.to_dict()})


@buses_bp.route('/', methods=['POST'])
def create_bus():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    required = ['bus_number', 'plate_number', 'capacity']
    for field in required:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing field: {field}'}), 400

    # Check duplicates
    if Bus.query.filter_by(bus_number=data['bus_number']).first():
        return jsonify({'success': False, 'message': 'Bus number already exists'}), 409
    if Bus.query.filter_by(plate_number=data['plate_number']).first():
        return jsonify({'success': False, 'message': 'Plate number already exists'}), 409

    bus = Bus(
        bus_number=data['bus_number'],
        plate_number=data['plate_number'],
        capacity=data['capacity'],
        bus_type=data.get('bus_type', 'Standard'),
        status=data.get('status', 'Active'),
        manufactured_year=data.get('manufactured_year')
    )
    db.session.add(bus)
    db.session.commit()
    return jsonify({'success': True, 'data': bus.to_dict(), 'message': 'Bus created successfully'}), 201


@buses_bp.route('/<int:bus_id>', methods=['PUT'])
def update_bus(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    data = request.get_json()

    bus.bus_number = data.get('bus_number', bus.bus_number)
    bus.plate_number = data.get('plate_number', bus.plate_number)
    bus.capacity = data.get('capacity', bus.capacity)
    bus.bus_type = data.get('bus_type', bus.bus_type)
    bus.status = data.get('status', bus.status)
    bus.manufactured_year = data.get('manufactured_year', bus.manufactured_year)

    db.session.commit()
    return jsonify({'success': True, 'data': bus.to_dict(), 'message': 'Bus updated successfully'})


@buses_bp.route('/<int:bus_id>', methods=['DELETE'])
def delete_bus(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    db.session.delete(bus)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Bus deleted successfully'})
