# Young Professionals — Backend (Headless CMS)

A Django + PostgreSQL backend that powers the **Young Professionals** home page
as a **Headless CMS**. Content editors use the Django admin; the Next.js
frontend reads everything over a REST API.

> No HTML templates are served from Django (other than the admin itself).
> All page content is delivered as JSON.

---

## 1. Tech Stack

| Layer            | Choice                                     |
|------------------|--------------------------------------------|
| Web framework    | Django 5.x                                 |
| API              | Django REST Framework                      |
| Database         | PostgreSQL (local)                         |
| Config           | `python-decouple` + `.env` file            |
| Media uploads    | `Pillow` + Django `MEDIA_ROOT` / `MEDIA_URL` |
| CORS             | `django-cors-headers` (for Next.js dev)    |

---

## 2. Folder Structure

```
young-professionals/
├── manage.py
├── requirements.txt
├── .env.example                  ← copy to .env locally
├── .gitignore
├── media/                        ← user uploads land here
├── static/                       ← static assets (admin extras, etc.)
│
├── young_professionals/          ← project package (settings + URLs)
│   ├── __init__.py
│   ├── settings.py               ← reads .env via python-decouple
│   ├── urls.py                   ← /admin/ + /api/home/
│   ├── wsgi.py
│   └── asgi.py
│
└── home/                         ← the "home page" CMS app
    ├── __init__.py
    ├── apps.py
    ├── models.py                 ← Hero, Nav, Feature, Stat, Testimonial, Opportunity
    ├── admin.py                  ← CMS-style admin (search/filter/order/inline)
    ├── serializers.py            ← DRF serializers (per-section + aggregate)
    ├── views.py                  ← read-only ViewSets + aggregate APIView
    ├── urls.py                   ← router-mounted endpoints
    ├── validators.py             ← shared image size + extension validators
    ├── tests.py
    └── migrations/
```

### What lives where (in plain English)

- **`models.py`** — the *shape* of content. Each section has its own table.
  All sections inherit `created_at`, `updated_at`, `order`, `is_active` from
  shared abstract bases (`TimeStampedModel`, `OrderedModel`, `CMSSection`),
  so a future "About" or "Contact" page can reuse them with no copy-paste.
- **`admin.py`** — the *editor*. Lists show thumbnails, you can re-order
  inline, search, filter, and bulk activate/deactivate.
- **`serializers.py`** — the *shape of the JSON* the frontend will receive.
- **`views.py`** — read-only viewsets + an aggregate `/api/home/` endpoint
  so Next.js can fetch the whole page in one request.
- **`urls.py`** — wires everything together via DRF's `DefaultRouter`.

---

## 3. PostgreSQL Setup (Step by Step)

### 3.1 Install PostgreSQL

**Windows** — download the installer from <https://www.postgresql.org/download/windows/>
and run it. Pick a password for the `postgres` superuser and remember it.

**macOS** —
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Ubuntu / WSL** —
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

Verify it's running:
```bash
psql --version
```

### 3.2 Create the database and a user

Open `psql` (on Windows: "SQL Shell (psql)" from the Start menu; elsewhere
`sudo -u postgres psql`) and run:

```sql
CREATE DATABASE young_professionals;
CREATE USER yp_user WITH PASSWORD 'yp_password';
ALTER ROLE yp_user SET client_encoding TO 'utf8';
ALTER ROLE yp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE yp_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE young_professionals TO yp_user;
\q
```

> If you'd rather use the default `postgres` user, you can skip `CREATE USER`
> — just put `postgres` and your superuser password in `.env`.

### 3.3 Tell Django about it

```bash
cp .env.example .env
```

Edit `.env` so the DB block matches what you just created:

```env
DB_NAME=young_professionals
DB_USER=yp_user
DB_PASSWORD=yp_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 4. Project Setup (Step by Step)

### 4.1 Create a virtual environment and install deps

```bash
# from the project root
python -m venv .venv

# activate it
#   Windows (PowerShell): .venv\Scripts\Activate.ps1
#   macOS/Linux/WSL:       source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` already contains `psycopg2-binary`, `python-decouple`,
`Pillow`, `Django`, `djangorestframework`, and `django-cors-headers`.

### 4.2 Run migrations

```bash
python manage.py makemigrations home
python manage.py migrate
```

### 4.3 Create an admin user

```bash
python manage.py createsuperuser
```

### 4.4 Run the server

```bash
python manage.py runserver
```

Open:

- Admin: <http://127.0.0.1:8000/admin/>
- API root: <http://127.0.0.1:8000/api/home/>

---

## 5. Content Model

| Section       | Model              | Highlights                                          |
|---------------|--------------------|------------------------------------------------------|
| Hero / Banner | `HeroSection`      | title, subtitle, description, bg image, 2 CTA buttons, slug |
| Navigation    | `NavigationMenu`   | nested via optional `parent` FK, `open_in_new_tab`  |
| Features row  | `Feature`          | icon image + title + description                    |
| Stats         | `Stat`             | big number + label                                  |
| Testimonials  | `Testimonial`      | name, designation, message, profile photo           |
| Opportunities | `Opportunity`      | company, job title, slug, banner, logo, salary type, apply URL |

Every section inherits:

- `created_at`, `updated_at` (audit)
- `order` (drag-friendly integer used for sorting)
- `is_active` (hide from API without deleting)

### Image rules

- Max 5 MB per image
- Allowed extensions: `jpg`, `jpeg`, `png`, `webp`, `svg`, `gif`
- Stored under `media/home/<section>/`

---

## 6. API Endpoints

Mounted under `/api/home/`. All endpoints are **read-only** for now and
filter out `is_active=False` rows automatically.

| Endpoint                                  | Returns                                   |
|-------------------------------------------|-------------------------------------------|
| `GET /api/home/`                          | Aggregate payload — every section at once |
| `GET /api/home/hero/`                     | List of hero banners                      |
| `GET /api/home/hero/<slug>/`              | One hero banner                           |
| `GET /api/home/navigation/`               | Top-level nav with nested `children`      |
| `GET /api/home/features/`                 | List of features                          |
| `GET /api/home/stats/`                    | List of stats                             |
| `GET /api/home/testimonials/`             | List of testimonials                      |
| `GET /api/home/opportunities/`            | List of opportunities                     |
| `GET /api/home/opportunities/<slug>/`     | One opportunity                           |

Example aggregate response shape:

```json
{
  "hero":          [ { "id": 1, "title": "...", ... } ],
  "navigation":    [ { "id": 1, "menu_name": "...", "children": [...] } ],
  "features":      [ ... ],
  "stats":         [ ... ],
  "testimonials":  [ ... ],
  "opportunities": [ ... ]
}
```

> Pagination is enabled by default on the per-section list endpoints
> (`PageNumberPagination`, page size 20). The aggregate endpoint returns
> all active rows in one call — convenient for a single home-page render.

---

## 7. Calling the API from Next.js

```ts
// next.js (app router)
export async function getHome() {
  const res = await fetch("http://127.0.0.1:8000/api/home/", {
    next: { revalidate: 60 },
  });
  if (!res.ok) throw new Error("Failed to load home content");
  return res.json();
}
```

`CORS_ALLOWED_ORIGINS` in `.env` already permits `http://localhost:3000`
and `http://127.0.0.1:3000` for the Next.js dev server.

Image URLs in the JSON are relative paths under `/media/`. Either prefix them
with the API origin in your frontend, or configure Next.js's `images.remotePatterns`
to allow `127.0.0.1:8000`.

---

## 8. Adding a New Page Later (e.g. About)

The codebase is set up for this:

1. Create a new app: `python manage.py startapp about`
2. Define section models that inherit from `home.models.CMSSection` (or
   `TimeStampedModel` + `OrderedModel`) so you get timestamps + ordering for free.
3. Mirror the `home` app's `admin.py` / `serializers.py` / `views.py` / `urls.py`.
4. Mount under `/api/about/` in `young_professionals/urls.py`.

The shared validators, abstract bases, and admin mixin (`CMSAdminMixin`)
are designed to be reused across any future page.

---

## 9. Common Commands

```bash
# create a new migration after model changes
python manage.py makemigrations

# apply pending migrations
python manage.py migrate

# open a Django shell
python manage.py shell

# collect static (production)
python manage.py collectstatic
```
