from flask import Blueprint, request, jsonify
from models import db, Driver
from datetime import datetime

drivers_bp = Blueprint('drivers', __name__)


@drivers_bp.route('/', methods=['GET'])
def get_drivers():
    drivers = Driver.query.all()
    return jsonify({'success': True, 'data': [d.to_dict() for d in drivers]})


@drivers_bp.route('/<int:driver_id>', methods=['GET'])
def get_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    return jsonify({'success': True, 'data': driver.to_dict()})


@drivers_bp.route('/', methods=['POST'])
def create_driver():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    required = ['name', 'license_number']
    for field in required:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing field: {field}'}), 400

    if Driver.query.filter_by(license_number=data['license_number']).first():
        return jsonify({'success': False, 'message': 'License number already exists'}), 409

    hire_date = None
    if data.get('hire_date'):
        try:
            hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    driver = Driver(
        name=data['name'],
        license_number=data['license_number'],
        phone=data.get('phone'),
        email=data.get('email'),
        status=data.get('status', 'Available'),
        hire_date=hire_date
    )
    db.session.add(driver)
    db.session.commit()
    return jsonify({'success': True, 'data': driver.to_dict(), 'message': 'Driver created successfully'}), 201


@drivers_bp.route('/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    data = request.get_json()

    driver.name = data.get('name', driver.name)
    driver.license_number = data.get('license_number', driver.license_number)
    driver.phone = data.get('phone', driver.phone)
    driver.email = data.get('email', driver.email)
    driver.status = data.get('status', driver.status)

    if data.get('hire_date'):
        try:
            driver.hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid date format'}), 400

    db.session.commit()
    return jsonify({'success': True, 'data': driver.to_dict(), 'message': 'Driver updated successfully'})


@drivers_bp.route('/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Driver deleted successfully'})


@drivers_bp.route('/available', methods=['GET'])
def get_available_drivers():
    drivers = Driver.query.filter_by(status='Available').all()
    return jsonify({'success': True, 'data': [d.to_dict() for d in drivers]})
