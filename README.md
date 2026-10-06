# 🏠 LINK - Real Estate Management System

A modern web platform for real estate management with analytics, booking, and personal dashboards for developers and buyers.

## 🚀 Features

### For buyers:
- 📋 Browse the real estate catalog
- 🔍 Search and filter properties
- 🗺️ Interactive map with properties
- 🏠 3D apartment tours
- 📊 View analytics
- 💳 Booking and purchasing real estate
- 👤 Personal dashboard with bookings

### For developers:
- 🏢 Manage residential complexes
- 🏠 Add and edit apartments
- 📊 Detailed sales analytics
- 👥 Manage bookings
- 📈 Property statistics
- 🎯 Conversion tracking

## 🛠️ Technologies

### Backend:
- **FastAPI** - modern web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - primary database
- **Pydantic** - data validation
- **Uvicorn** - ASGI server

### Frontend:
- **Vue.js 3** - progressive JavaScript framework
- **Vite** - fast bundler
- **Axios** - HTTP client
- **CSS3** - modern styles

## 📦 Installation and Launch

### Prerequisites:
- Python 3.11+
- Node.js 18+
- PostgreSQL 12+
- Git

### 1. Clone the repository:
```bash
git clone https://github.com/IvanZhutyaev/json-state-home.git
cd json-state-home
```

### 2. Backend setup:

```bash
# Go to the backend folder
cd backend

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt

# Set up the database
python final_fix.py

# Start the server
uvicorn main:app --reload
```

### 3. Frontend setup:

```bash
# Go to the frontend folder
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

### 4. Database setup:

Create a PostgreSQL database and update the connection settings in `backend/Database/DB_connection.py`:

```python
DATABASE_URL = "postgresql://username:password@localhost:5432/database_name"
```

## 🔧 Fixed Issues

### ✅ Critical fixes:
- **Price error**: Fixed the `price` field type from `Integer` to `BigInteger` to support large values
- **Booking issues**: Fixed relationships between models and data validation
- **Analytics**: Added a complete event tracking system
- **Residential complex relationships**: Fixed the relationship between developers, residential complexes, and apartments

### 📁 New files:
- `backend/Cruds/Analytics_crud.py` - CRUD for analytics
- `backend/Routers/Analytics_router.py` - analytics routes
- `backend/Schemas/Analytics_schema.py` - analytics schemas
- `backend/final_fix.py` - database fix script
- `frontend/src/components/AnalyticsDashboard.vue` - analytics dashboard

## 📊 API Endpoints

### Main endpoints:
- `GET /properties/` - list of real estate
- `POST /properties/` - create real estate
- `GET /zastroys/` - list of developers
- `POST /api/track-event` - track events
- `GET /api/analytics/summary` - analytics summary

### Full API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🎯 Functionality

### Analytics:
- 📈 Apartment view tracking
- 🕒 Time spent on page
- 🎯 Conversion (view → booking)
- 📊 Statistics by developer
- 🔍 Search and filter analytics

### Real estate management:
- 🏢 Create and manage residential complexes
- 🏠 Add apartments to residential complexes
- 💰 Price management
- 📸 Image upload
- 📍 Property geolocation

### Booking:
- 📅 Booking system
- 💳 Purchase process
- 📧 Notifications
- 📊 Sales statistics

## 🤝 Contributing

1. Fork the repository
2. Create a branch for a new feature (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you have questions or issues:
- Create an Issue on GitHub
- Describe the problem in detail
- Attach error logs

## 🚀 Deployment

### Production:
```bash
# Backend
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
npm run build
```

---

**DIMA** - a modern real estate management system for developers and buyers! 🏠✨
