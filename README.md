# Price Comparison Tool

A web application for comparing product prices across multiple platforms. Users can search for products and view price listings from various websites in one place.

## Features

- User authentication (signup, login, logout with email verification)
- Product price comparison search
- Multi-platform price listings with direct purchase links
- User dashboard with statistics
- Personal wishlist with price alerts
- Responsive web interface
- Background email price alert system

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Frontend**: React (Vite) + Bootstrap
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Token-based with email verification
- **Task Queue**: Celery (for background tasks)

## Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8 or higher
- Node.js 16 or higher
- Git

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-github-repo-url>
cd Price_Comparison_Tool
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
# source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Seed initial data (optional)
python manage.py seed_data

# Create superuser (optional, for admin access)
python manage.py createsuperuser
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install Node.js dependencies
npm install
```

### 4. Environment Configuration

Create a `.env` file in the `backend` directory with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

**Note**: For email functionality, you'll need to set up an email service (Gmail, SendGrid, etc.) and configure the settings above.

## Running the Application

### Start Backend Server

```bash
cd backend
.venv\Scripts\activate  # On Windows
python manage.py runserver
```

Backend will be available at: `http://127.0.0.1:8000`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:5173`

### Running Background Tasks (Optional)

For price alert emails, run Celery worker:

```bash
cd backend
.venv\Scripts\activate
celery -A pricecompare worker --loglevel=info
```

## API Endpoints

### Authentication
- `POST /api/auth/signup/` - User registration
- `GET /api/auth/verify-email/?token=<uuid>` - Email verification
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Products
- `GET /api/products/compare/?q=<search_query>` - Compare product prices

### User Data
- `GET /api/dashboard/` - User dashboard data
- `GET /api/profile/` - User profile
- `PUT /api/profile/` - Update user profile
- `GET /api/wishlist/` - User's wishlist
- `POST /api/wishlist/` - Add item to wishlist
- `DELETE /api/wishlist/<id>/` - Remove from wishlist

## Project Structure

```
Price_Comparison_Tool/
├── backend/                 # Django backend
│   ├── apps/
│   │   └── core/           # Main app
│   │       ├── models.py
│   │       ├── views.py
│   │       ├── serializers.py
│   │       └── services/
│   ├── pricecompare/       # Django project settings
│   ├── requirements.txt
│   └── manage.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/
│   │   ├── api.js
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── README.md
└── .gitignore
```

## Development

### Running Tests

```bash
cd backend
python manage.py test
```

### Code Formatting

```bash
# Backend (if black is installed)
black .

# Frontend
cd frontend
npm run lint
```

## Deployment

### Backend Deployment
- Use Gunicorn for production WSGI server
- Configure PostgreSQL database
- Set up Redis for Celery
- Use environment variables for secrets

### Frontend Deployment
- Build production bundle: `npm run build`
- Serve static files from `dist/` directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open an issue on GitHub.
- `GET /api/dashboard/`
- `GET/POST /api/wishlist/`
- `PATCH/DELETE /api/wishlist/<id>/`

## Price alert scheduling (future-ready)

Run manually:

```bash
python manage.py check_price_alerts
```

Then schedule it with Windows Task Scheduler or Celery beat for periodic execution.

## Flexible live-price ingestion (new)

This project now includes a normalized listing pipeline:

- `ProductListing`: latest price per product + platform
- `PriceHistory`: time-series snapshots for each listing
- Adapter layer in `apps/core/services/adapters.py`
- Refresh pipeline in `apps/core/services/price_pipeline.py`

Run manual refresh:

```bash
python manage.py fetch_platform_prices
```

### Celery setup

Start Redis (required), then run:

```bash
celery -A pricecompare worker -l info --pool=solo
celery -A pricecompare beat -l info
```

Beat schedules `refresh_market_prices_task` every 30 minutes.

## Production deployment (Docker)

This project includes a production-ready stack:

- `frontend`: React build served by Nginx
- `backend`: Django + Gunicorn
- `db`: PostgreSQL
- `redis`: broker/cache
- `celery-worker` and `celery-beat` for background jobs

### 1) Create environment file

```bash
copy .env.example .env
```

Update values in `.env` (especially `SECRET_KEY`, DB password, allowed hosts, origins).

### 2) Build and run services

```bash
docker compose up -d --build
```

### 3) Access app

- App: `http://localhost`
- API routed via Nginx: `http://localhost/api/...`

### 4) Useful commands

```bash
docker compose logs -f backend
docker compose logs -f frontend
docker compose ps
docker compose down
```

### Notes for long-term hosting

- Replace `localhost` values in `.env` with your domain.
- Set `DEBUG=False`.
- Add HTTPS at edge/load-balancer (or Cloudflare) for secure cookies and CSRF.
