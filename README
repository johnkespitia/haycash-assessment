# Haycash — Customer Management

Technical assessment implementing a customer management API and a responsive customer dashboard.

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic
- **Frontend:** SvelteKit, Svelte 5, TypeScript
- **Styling:** Tailwind CSS v4
- **Testing:** Pytest, Vitest, Playwright
- **Development:** Docker Compose

## Features

- List customers and filter by status.
- Search customers by name or email.
- View customer details.
- Handle loading, error, and empty states.
- Responsive dashboard UI.
- REST API for customer management.

Customer statuses: `ACTIVE`, `PENDING`, `BLOCKED`.

## Requirements

- Docker and Docker Compose
- Git

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd haycash-test
```

### 2. Configure environment variables

Create the required environment files based on the provided examples.

Configure the frontend API URL using `VITE_API_BASE_URL`. It must point to the backend address accessible from the browser.

Example:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Replace the placeholder with the actual backend port configured in Docker Compose.

### 3. Start the applications

From the repository root:

```bash
docker compose up --build -d
```

Check running services:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs -f
```

Stop the applications:

```bash
docker compose down
```

## Backend API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/customers` | Create a customer |
| `GET` | `/customers` | List customers |
| `GET` | `/customers/{customer_id}` | Get customer details |
| `PATCH` | `/customers/{customer_id}/status` | Update customer status |

The list endpoint supports filtering by status.

If enabled by the backend configuration, interactive API documentation is available at `/docs`.

## Frontend Commands

Run from the frontend container:

```bash
npm run check
npm run lint
npm run test:unit -- --run
npm run test:e2e
npm run build
```

## Project Structure

```text
haycash-test/
├── apps/
│   ├── backend/
│   └── frontend/
├── docker-compose.yml
└── README.md
```

The frontend uses feature-based organization, separating API access, domain types, services, state management, and UI components.

## Notes

- Configure the API URL before starting the frontend.
- Ensure the backend is reachable from the browser.
- Use Docker Compose to run the applications consistently.
