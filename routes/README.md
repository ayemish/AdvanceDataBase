# Flight Price Tracker

A system to monitor and track flight prices over time with API and web interface.

## Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Configure database
echo "MONGO_URI=mongodb://localhost:27017/" > .env

# Load sample data
python scripts/seed.py
```

### Running the Application
```bash
# Start backend server
python app.py

# In separate terminal, start web interface
streamlit run streamlit_app.py
```

### Access Points
- **API Documentation**: http://localhost:8000/docs
- **Web Interface**: http://localhost:8501

## System Overview

**Core Functionality:**
- Monitor flight routes and airlines
- Record price changes over time
- Analyze price trends and history
- Manage flight tracking data

## Architecture Components

### Backend (FastAPI)
- `app.py` - Main application server
- `models/` - Data models and validation
- `routes/` - API endpoint handlers

### Frontend (Streamlit)
- `streamlit_app.py` - Web-based user interface

### Database (MongoDB)
- `flights` collection - Flight information and metadata
- `price_snapshots` collection - Historical price records

## Key Features

- Flight Management - Add, view, update, and delete tracked flights
- Price Recording - Capture price snapshots at different times
- Historical Analysis - View price trends and changes over time
- Dashboard - Overview of all monitored flights and current prices

## API Usage Examples

```bash
# Retrieve all tracked flights
curl http://localhost:8000/api/flights

# Get price history for specific flight
curl http://localhost:8000/api/flights/F001/prices

# Add new flight to track
curl -X POST http://localhost:8000/api/flights \
  -H "Content-Type: application/json" \
  -d '{"flight_id":"NEW123", "route":{"from":"JFK","to":"LAX"}, "airline":"Test Air"}'
```

## Workflow

1. **Setup** - Add flights you want to monitor
2. **Tracking** - Record prices at regular intervals
3. **Analysis** - Review price trends and patterns
4. **Decision** - Use data to determine optimal purchase timing

## Project Structure

- `requirements.txt` - Python package dependencies
- `scripts/seed.py` - Database seeding with sample data
- `.env` - Environment configuration file
- `app.py` - FastAPI application entry point
- `streamlit_app.py` - Web interface application

## Technical Stack

- **Backend**: FastAPI, Uvicorn, Pydantic
- **Database**: MongoDB with PyMongo
- **Frontend**: Streamlit, Pandas
- **Configuration**: python-dotenv

A comprehensive flight price monitoring solution for tracking and analyzing airfare changes over time.