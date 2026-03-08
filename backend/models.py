from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Bus(db.Model):
    __tablename__ = 'buses'

    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(20), unique=True, nullable=False)
    plate_number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    bus_type = db.Column(db.String(50), default='Standard')  # Standard, Express, Mini
    status = db.Column(db.String(20), default='Active')      # Active, Maintenance, Retired
    manufactured_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    schedules = db.relationship('Schedule', backref='bus', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'bus_number': self.bus_number,
            'plate_number': self.plate_number,
            'capacity': self.capacity,
            'bus_type': self.bus_type,
            'status': self.status,
            'manufactured_year': self.manufactured_year,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Available')  # Available, On Duty, Off Duty
    hire_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    schedules = db.relationship('Schedule', backref='driver', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'license_number': self.license_number,
            'phone': self.phone,
            'email': self.email,
            'status': self.status,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(100), nullable=False)
    route_number = db.Column(db.String(20), unique=True, nullable=False)
    start_location = db.Column(db.String(200), nullable=False)
    end_location = db.Column(db.String(200), nullable=False)
    start_lat = db.Column(db.Float)
    start_lng = db.Column(db.Float)
    end_lat = db.Column(db.Float)
    end_lng = db.Column(db.Float)
    distance_km = db.Column(db.Float)
    estimated_duration_min = db.Column(db.Integer)
    status = db.Column(db.String(20), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    stops = db.relationship('BusStop', backref='route', lazy=True, cascade='all, delete-orphan')
    schedules = db.relationship('Schedule', backref='route', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'route_name': self.route_name,
            'route_number': self.route_number,
            'start_location': self.start_location,
            'end_location': self.end_location,
            'start_lat': self.start_lat,
            'start_lng': self.start_lng,
            'end_lat': self.end_lat,
            'end_lng': self.end_lng,
            'distance_km': self.distance_km,
            'estimated_duration_min': self.estimated_duration_min,
            'status': self.status,
            'stops': [s.to_dict() for s in self.stops],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class BusStop(db.Model):
    __tablename__ = 'bus_stops'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    stop_name = db.Column(db.String(100), nullable=False)
    stop_order = db.Column(db.Integer, nullable=False)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'route_id': self.route_id,
            'stop_name': self.stop_name,
            'stop_order': self.stop_order,
            'lat': self.lat,
            'lng': self.lng
        }


class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    schedule_name = db.Column(db.String(100), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    departure_time = db.Column(db.String(10), nullable=False)   # HH:MM format
    arrival_time = db.Column(db.String(10), nullable=False)
    schedule_date = db.Column(db.Date, nullable=False)
    schedule_type = db.Column(db.String(20), default='Linked')   # Linked, Unlinked
    status = db.Column(db.String(20), default='Scheduled')       # Scheduled, In Progress, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'schedule_name': self.schedule_name,
            'bus_id': self.bus_id,
            'bus_number': self.bus.bus_number if self.bus else None,
            'driver_id': self.driver_id,
            'driver_name': self.driver.name if self.driver else None,
            'route_id': self.route_id,
            'route_name': self.route.route_name if self.route else None,
            'route_number': self.route.route_number if self.route else None,
            'departure_time': self.departure_time,
            'arrival_time': self.arrival_time,
            'schedule_date': self.schedule_date.isoformat() if self.schedule_date else None,
            'schedule_type': self.schedule_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
