from flask import Blueprint, jsonify
from models import db, Bus, Driver, Route, Schedule
from datetime import date

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/stats', methods=['GET'])
def get_stats():
    total_buses = Bus.query.count()
    active_buses = Bus.query.filter_by(status='Active').count()
    total_drivers = Driver.query.count()
    available_drivers = Driver.query.filter_by(status='Available').count()
    total_routes = Route.query.count()
    active_routes = Route.query.filter_by(status='Active').count()
    total_schedules = Schedule.query.count()
    today_schedules = Schedule.query.filter_by(schedule_date=date.today()).count()

    return jsonify({
        'success': True,
        'data': {
            'buses': {'total': total_buses, 'active': active_buses},
            'drivers': {'total': total_drivers, 'available': available_drivers},
            'routes': {'total': total_routes, 'active': active_routes},
            'schedules': {'total': total_schedules, 'today': today_schedules}
        }
    })


@dashboard_bp.route('/recent-schedules', methods=['GET'])
def recent_schedules():
    schedules = Schedule.query.order_by(Schedule.created_at.desc()).limit(5).all()
    return jsonify({'success': True, 'data': [s.to_dict() for s in schedules]})
