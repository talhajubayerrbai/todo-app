# Todo App

A simple, production-deployed todo application built with Django and PostgreSQL,
running on AWS EC2 behind nginx — provisioned and deployed via GitHub Actions CI/CD.

## Architecture

```
User → nginx (EC2, port 80) → Gunicorn (127.0.0.1:8000) → Django → RDS PostgreSQL
```

See `.udap/architecture.d2` for the full system diagram.

## Features

- Create, complete/uncomplete, and delete todo items
- Persistent storage in PostgreSQL
- Django admin at `/admin/`
- Health check at `/health/`

## Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL (or SQLite for quick start)

### Quick start

```bash
# Clone and enter the project
git clone <repo-url>
cd todo-app

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — set SECRET_KEY and DATABASE_URL

# Run migrations
python manage.py migrate

# Start the dev server
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### Running tests

```bash
python manage.py test
```

## Deployment

Pushes to `main` trigger the CI/CD pipeline automatically:

| Stage | What it does |
|-------|--------------|
| `lint` | Runs flake8 |
| `test` | Runs Django test suite |
| `provision` | Runs `terraform apply` — creates EC2, RDS, security groups |
| `configure` | Runs Ansible — installs app, writes `.env`, runs migrations, starts services |
| `verify` | HTTP health check against `/health/` with retry/backoff |

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DATABASE_URL` | PostgreSQL connection URL | Yes |
| `DEBUG` | Enable debug mode (`True`/`False`) | No (default `False`) |
| `ALLOWED_HOSTS` | Comma-separated allowed hostnames | No (default `*`) |

Secrets (`DB_PASSWORD`, `SSH_PRIVATE_KEY`, `SSH_PUBLIC_KEY`, AWS credentials) are
managed via GitHub repository secrets and injected by the platform at deploy time.

## Operations

### Check service status (on the EC2 instance)

```bash
sudo systemctl status todo-app
sudo systemctl status nginx
journalctl -u todo-app -f
```

### Restart the app

```bash
sudo systemctl restart todo-app
```

### Run a migration manually

```bash
cd /opt/todo-app
source venv/bin/activate
python manage.py migrate
```

### Destroy infrastructure

Trigger the **Destroy** workflow from the GitHub Actions tab to tear down all AWS resources.

## App URL

`http://<EC2_PUBLIC_IP>` — the public IP is shown in the GitHub Actions `provision` step
output after the first deploy.
