## 🚌 TransitFlowPro(BusMaster) 
### Automated Bus Scheduling & Route Management System

BusMaster is a full-stack web application that replaces manual transit scheduling with an automated system that manages buses, drivers, routes, and duty schedules — with real-time map visualization via Leaflet.js and OpenStreetMap.

---

## ✨ Features

| Module | Capabilities |
|---|---|
| **Fleet Management** | Add, view, edit, delete buses with type & status tracking |
| **Driver Management** | Crew registry with license, contact, and availability tracking |
| **Route Management** | Create routes with coordinates, visualize on interactive map with bus stops |
| **Scheduling System** | Linked/Unlinked duty scheduling with **automatic conflict detection** |
| **Dashboard** | Real-time stats for buses, drivers, routes, and daily schedules |
| **Map Integration** | Leaflet.js + OpenStreetMap — plot, toggle, and inspect all routes |

---

## 🏗 Project Structure

```
busmaster/
├── backend/
│   ├── app.py                  # Flask app factory & page routes
│   ├── models.py               # SQLAlchemy ORM models
│   └── routes/
│       ├── __init__.py
│       ├── buses.py            # Bus CRUD API
│       ├── drivers.py          # Driver CRUD API
│       ├── route_mgmt.py       # Route + Bus Stop API
│       ├── schedules.py        # Schedule API with conflict detection
│       └── dashboard.py        # Stats & summary API
├── frontend/
│   ├── static/
│   │   ├── css/style.css       # Industrial transit design system
│   │   └── js/main.js          # API helpers, modals, toasts
│   └── templates/
│       ├── base.html           # Base layout with sidebar nav
│       ├── dashboard.html      # System overview
│       ├── buses.html          # Fleet management
│       ├── drivers.html        # Driver management
│       ├── routes.html         # Routes + Leaflet map
│       └── schedules.html      # Schedule management
├── database/
│   └── schema.sql              # Reference schema + seed data
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone / Download the project
```bash
git clone https://github.com/sitej6174/busmaster.git
cd busmaster
```

### 2. Create a Python virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
cd backend
python app.py
```

The app will be available at: **http://localhost:5000**

The SQLite database (`busmaster.db`) is auto-created on first run inside `/database/`.

---

## 🗄 Database Schema

### `buses`
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| bus_number | VARCHAR UNIQUE | e.g. `BUS-001` |
| plate_number | VARCHAR UNIQUE | e.g. `ABC-1234` |
| capacity | INTEGER | Passenger seats |
| bus_type | VARCHAR | Standard / Express / Mini |
| status | VARCHAR | Active / Maintenance / Retired |
| manufactured_year | INTEGER | Year of manufacture |

### `drivers`
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| name | VARCHAR | Full name |
| license_number | VARCHAR UNIQUE | Driver's license |
| phone / email | VARCHAR | Contact info |
| status | VARCHAR | Available / On Duty / Off Duty |
| hire_date | DATE | Employment start date |

### `routes`
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| route_number | VARCHAR UNIQUE | e.g. `R-001` |
| route_name | VARCHAR | Human-readable name |
| start/end_location | VARCHAR | Location names |
| start/end_lat/lng | FLOAT | GPS coordinates for map |
| distance_km | FLOAT | Route length |
| estimated_duration_min | INTEGER | Time in minutes |

### `bus_stops`
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| route_id | FK → routes | Parent route |
| stop_name | VARCHAR | Stop label |
| stop_order | INTEGER | Sequence position |
| lat / lng | FLOAT | GPS coordinates |

### `schedules`
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| bus_id | FK → buses | Assigned bus |
| driver_id | FK → drivers | Assigned driver |
| route_id | FK → routes | Assigned route |
| departure_time | VARCHAR | HH:MM format |
| arrival_time | VARCHAR | HH:MM format |
| schedule_date | DATE | Service date |
| schedule_type | VARCHAR | Linked / Unlinked duty |
| status | VARCHAR | Scheduled / In Progress / Completed / Cancelled |

---

## 🔌 API Reference

### Buses
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/buses/` | List all buses |
| GET | `/api/buses/<id>` | Get single bus |
| POST | `/api/buses/` | Create bus |
| PUT | `/api/buses/<id>` | Update bus |
| DELETE | `/api/buses/<id>` | Delete bus |

### Drivers
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/drivers/` | List all drivers |
| GET | `/api/drivers/available` | Only available drivers |
| POST | `/api/drivers/` | Create driver |
| PUT | `/api/drivers/<id>` | Update driver |
| DELETE | `/api/drivers/<id>` | Delete driver |

### Routes
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/routes/` | List all routes |
| POST | `/api/routes/` | Create route |
| PUT | `/api/routes/<id>` | Update route |
| DELETE | `/api/routes/<id>` | Delete route |
| POST | `/api/routes/<id>/stops` | Add bus stop to route |
| DELETE | `/api/routes/<id>/stops/<stop_id>` | Remove bus stop |

### Schedules
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/schedules/` | List all schedules |
| POST | `/api/schedules/` | Create schedule (with conflict check) |
| PUT | `/api/schedules/<id>` | Update schedule |
| DELETE | `/api/schedules/<id>` | Delete schedule |
| GET | `/api/schedules/by-date/<YYYY-MM-DD>` | Schedules for a date |

### Dashboard
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/dashboard/stats` | System summary counts |
| GET | `/api/dashboard/recent-schedules` | Last 5 schedules |

---

## 📡 Example API Requests

```bash
# Add a bus
curl -X POST http://localhost:5000/api/buses/ \
  -H "Content-Type: application/json" \
  -d '{"bus_number":"BUS-001","plate_number":"ABC-1234","capacity":52,"bus_type":"Standard"}'

# Create a route with coordinates
curl -X POST http://localhost:5000/api/routes/ \
  -H "Content-Type: application/json" \
  -d '{
    "route_number":"R-001",
    "route_name":"City Centre Express",
    "start_location":"Central Terminal",
    "end_location":"Airport",
    "start_lat":3.1390,"start_lng":101.6869,
    "end_lat":3.1200,"end_lng":101.7500,
    "distance_km":25.5,
    "estimated_duration_min":45
  }'

# Create a schedule (conflict detection auto-applied)
curl -X POST http://localhost:5000/api/schedules/ \
  -H "Content-Type: application/json" \
  -d '{
    "schedule_name":"Morning Run Alpha",
    "bus_id":1,"driver_id":1,"route_id":1,
    "schedule_date":"2024-12-01",
    "departure_time":"07:00",
    "arrival_time":"08:00",
    "schedule_type":"Linked"
  }'
```

---

## 🗺 Map Usage

1. Navigate to **Routes & Map**
2. Create routes with GPS coordinates (start/end latitude & longitude)
3. Click **Show All Routes** to display all routes simultaneously
4. Click the 🗺 button on any row to isolate that route on the map
5. Bus stops are shown as intermediate dots on the route line
6. Click any marker for location details

---

## 🛡 Conflict Detection

BusMaster prevents double-booking automatically:
- **Bus conflicts** — same bus cannot be scheduled for overlapping time windows on the same date
- **Driver conflicts** — same driver cannot be assigned overlapping shifts on the same date
- Conflicts return HTTP `409 Conflict` with a descriptive error message

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+ / Flask 3.0 |
| ORM | Flask-SQLAlchemy |
| Database | SQLite |
| Frontend | HTML5 / CSS3 / Vanilla JavaScript |
| Maps | Leaflet.js + OpenStreetMap |
| Fonts | Barlow Condensed + Barlow + JetBrains Mono |

---

## 📄 License

MIT License — free for educational and commercial use.
