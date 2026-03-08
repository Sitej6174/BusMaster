from flask import Blueprint, request, jsonify
from models import db, Schedule, Bus, Driver, Route
from datetime import datetime

schedules_bp = Blueprint('schedules', __name__)


def check_conflict(bus_id, driver_id, schedule_date, departure_time, arrival_time, exclude_id=None):
    """Check for scheduling conflicts for bus and driver on same date/time."""
    date_obj = datetime.strptime(schedule_date, '%Y-%m-%d').date()

    # Check bus conflict
    bus_query = Schedule.query.filter(
        Schedule.bus_id == bus_id,
        Schedule.schedule_date == date_obj,
        Schedule.status != 'Cancelled'
    )
    if exclude_id:
        bus_query = bus_query.filter(Schedule.id != exclude_id)

    for existing in bus_query.all():
        if times_overlap(departure_time, arrival_time, existing.departure_time, existing.arrival_time):
            return f"Bus is already scheduled for route {existing.route.route_number} at this time"

    # Check driver conflict
    driver_query = Schedule.query.filter(
        Schedule.driver_id == driver_id,
        Schedule.schedule_date == date_obj,
        Schedule.status != 'Cancelled'
    )
    if exclude_id:
        driver_query = driver_query.filter(Schedule.id != exclude_id)

    for existing in driver_query.all():
        if times_overlap(departure_time, arrival_time, existing.departure_time, existing.arrival_time):
            return f"Driver is already scheduled for route {existing.route.route_number} at this time"

    return None


def times_overlap(dep1, arr1, dep2, arr2):
    """Return True if two time windows overlap."""
    def to_minutes(t):
        h, m = map(int, t.split(':'))
        return h * 60 + m

    start1, end1 = to_minutes(dep1), to_minutes(arr1)
    start2, end2 = to_minutes(dep2), to_minutes(arr2)
    return not (end1 <= start2 or end2 <= start1)


@schedules_bp.route('/', methods=['GET'])
def get_schedules():
    schedules = Schedule.query.order_by(Schedule.schedule_date.desc()).all()
    return jsonify({'success': True, 'data': [s.to_dict() for s in schedules]})


@schedules_bp.route('/<int:schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    return jsonify({'success': True, 'data': schedule.to_dict()})


@schedules_bp.route('/', methods=['POST'])
def create_schedule():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    required = ['schedule_name', 'bus_id', 'driver_id', 'route_id',
                'departure_time', 'arrival_time', 'schedule_date']
    for field in required:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing field: {field}'}), 400

    # Validate references
    if not Bus.query.get(data['bus_id']):
        return jsonify({'success': False, 'message': 'Bus not found'}), 404
    if not Driver.query.get(data['driver_id']):
        return jsonify({'success': False, 'message': 'Driver not found'}), 404
    if not Route.query.get(data['route_id']):
        return jsonify({'success': False, 'message': 'Route not found'}), 404

    # Conflict check
    conflict = check_conflict(
        data['bus_id'], data['driver_id'],
        data['schedule_date'], data['departure_time'], data['arrival_time']
    )
    if conflict:
        return jsonify({'success': False, 'message': f'Scheduling conflict: {conflict}'}), 409

    try:
        schedule_date = datetime.strptime(data['schedule_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid date format'}), 400

    schedule = Schedule(
        schedule_name=data['schedule_name'],
        bus_id=data['bus_id'],
        driver_id=data['driver_id'],
        route_id=data['route_id'],
        departure_time=data['departure_time'],
        arrival_time=data['arrival_time'],
        schedule_date=schedule_date,
        schedule_type=data.get('schedule_type', 'Linked'),
        status=data.get('status', 'Scheduled')
    )
    db.session.add(schedule)
    db.session.commit()
    return jsonify({'success': True, 'data': schedule.to_dict(), 'message': 'Schedule created successfully'}), 201


@schedules_bp.route('/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    data = request.get_json()

    new_bus_id = data.get('bus_id', schedule.bus_id)
    new_driver_id = data.get('driver_id', schedule.driver_id)
    new_date = data.get('schedule_date', schedule.schedule_date.isoformat())
    new_dep = data.get('departure_time', schedule.departure_time)
    new_arr = data.get('arrival_time', schedule.arrival_time)

    conflict = check_conflict(new_bus_id, new_driver_id, new_date, new_dep, new_arr, exclude_id=schedule_id)
    if conflict:
        return jsonify({'success': False, 'message': f'Scheduling conflict: {conflict}'}), 409

    schedule.schedule_name = data.get('schedule_name', schedule.schedule_name)
    schedule.bus_id = new_bus_id
    schedule.driver_id = new_driver_id
    schedule.route_id = data.get('route_id', schedule.route_id)
    schedule.departure_time = new_dep
    schedule.arrival_time = new_arr
    schedule.schedule_type = data.get('schedule_type', schedule.schedule_type)
    schedule.status = data.get('status', schedule.status)

    if data.get('schedule_date'):
        schedule.schedule_date = datetime.strptime(data['schedule_date'], '%Y-%m-%d').date()

    db.session.commit()
    return jsonify({'success': True, 'data': schedule.to_dict(), 'message': 'Schedule updated'})


@schedules_bp.route('/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Schedule deleted'})


@schedules_bp.route('/by-date/<date_str>', methods=['GET'])
def get_schedules_by_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid date'}), 400
    schedules = Schedule.query.filter_by(schedule_date=date_obj).all()
    return jsonify({'success': True, 'data': [s.to_dict() for s in schedules]})
