# Credifiel Collection System

https://www.canva.com/design/DAGoeLobxhg/k6tCZKcSkELvSd5OSeZjBA/edit?utm_content=DAGoeLobxhg&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

A Django and Python-based system for managing credit collections and bank transactions.

## Project Structure

The project is divided into two main components:

- `server/`: Django backend with multiple apps for handling different aspects of the system
- `client/`: Python scripts for data processing and analysis

## Features

- Collection statistics tracking across multiple years (2022-2025)
- Bank transaction processing with different fee structures
- Credit scoring system based on payment history
- RESTful API endpoints for data access
- Automated report generation in Excel format

## Prerequisites

- Python 3.12+
- PostgreSQL database
- Virtual environment (recommended)

## Installation

### Server Setup

1. Create and activate a virtual environment:

```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   Create a `.env` file in the server directory with:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Start the server:

```bash
python manage.py runserver
```

### Client Setup

1. Create and activate a virtual environment:

```bash
cd client
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Ensure the Django server is running
2. Run the data processing script:

```bash
cd client
python datathon.py
```

The script will:

- Fetch collection statistics from the API
- Process credit data and calculate scores
- Generate an Excel report (`processed_credits.xlsx`)

## API Endpoints

- `/api/collection-stats/`: Returns collection statistics grouped by year and month

## Database Models

The system uses separate tables for each year's collection details:

- `ListaCobroDetalle2022`
- `ListaCobroDetalle2023`
- `ListaCobroDetalle2024`
- `ListaCobroDetalle2025`

Each table tracks:

- Collection IDs
- Credit IDs
- Bank information
- Transaction amounts
- Collection dates
- Bank response IDs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
