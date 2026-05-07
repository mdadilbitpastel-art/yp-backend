# Young Professionals — Backend (Headless CMS)

A Django + PostgreSQL backend that powers the **Young Professionals** website
as a **Headless CMS**. Content editors manage the site through a fully custom
AdminLTE-style dashboard at `/dashboard/`; the Next.js frontend reads every
section over a read-only REST API at `/api/home/`.

> Django Admin is intentionally **not mounted** — all editing happens in the
> custom dashboard. No HTML page templates are served from Django other than
> the dashboard itself; all public site content is delivered as JSON.

---

## 1. Tech Stack

| Layer            | Choice                                                      |
|------------------|-------------------------------------------------------------|
| Web framework    | Django 5.x                                                  |
| API              | Django REST Framework                                       |
| Database         | PostgreSQL (local + Render in production)                   |
| Config           | `python-decouple` + `.env`, `dj-database-url` in production |
| Media (dev)      | `Pillow` + Django `MEDIA_ROOT` / `MEDIA_URL`                |
| Media (prod)     | Cloudinary (`django-cloudinary-storage`)                    |
| Static files     | `whitenoise` (compressed manifest storage)                  |
| App server       | `gunicorn`                                                  |
| CORS             | `django-cors-headers` (for the Next.js frontend)            |
| Hosting          | Render (`render.yaml` blueprint included)                   |

---

## 2. Folder Structure

```
young-professionals/
├── manage.py
├── build.sh                       ← Render build hook (install + migrate + superuser)
├── render.yaml                    ← Render Blueprint (web service + Postgres)
├── requirements.txt
├── .env.example                   ← copy to .env locally
├── .gitignore
├── media/                         ← user uploads (local dev only)
├── static/                        ← project-level static assets
├── templates/dashboard/           ← AdminLTE-style dashboard templates
│
├── young_professionals/           ← project package (settings + URLs)
│   ├── settings.py                ← reads .env via python-decouple
│   ├── urls.py                    ← /, /dashboard/, /api/home/
│   ├── wsgi.py
│   └── asgi.py
│
├── home/                          ← homepage CMS app (models + API)
│   ├── models.py                  ← Singleton section models + child rows
│   ├── serializers.py             ← DRF serializers (per-section + aggregate)
│   ├── views.py                   ← read-only RetrieveAPIViews + aggregate
│   ├── urls.py                    ← API routes mounted under /api/home/
│   ├── validators.py              ← image + video size/extension validators
│   ├── storage.py                 ← video storage (always filesystem)
│   ├── signals.py
│   └── migrations/
│
└── dashboard/                     ← custom CMS dashboard app (no Django Admin)
    ├── views.py                   ← LoginRequired UpdateViews per section
    ├── forms.py                   ← ModelForms + InlineFormSets for child rows
    ├── urls.py                    ← /dashboard/login, /dashboard/home/*, etc.
    ├── sections.py                ← central registry of dashboard modules
    ├── context_processors.py      ← sidebar nav context for templates
    ├── templatetags/
    └── management/commands/
        └── ensure_superuser.py    ← idempotent superuser bootstrap (used in build.sh)
```

### What lives where (in plain English)

- **`home/models.py`** — every homepage section is a `SingletonModel` (one
  row, pk=1, `delete()` is a no-op, `load()` get-or-creates). Sections with
  repeating sub-items (feature cards, network stats, apply companies, social
  cards, header tabs, footer links) use a child model with a `ForeignKey`
  back to the singleton.
- **`home/serializers.py`** — shape of the JSON the frontend receives. The
  `HomePageSerializer` reloads every singleton in one response.
- **`home/views.py`** — read-only `RetrieveAPIView`s. `_SingletonMixin`
  resolves `get_object()` via `Model.load()`.
- **`dashboard/sections.py`** — the registry of dashboard modules and their
  sections. Adding an entry here makes it appear in the sidebar, the module
  landing page, and the dashboard overview's "x of y configured" stat.
- **`dashboard/views.py`** — one `UpdateView` per section. Sections with
  child rows (Feature, Network, Apply, Social Media, Header, Footer) post
  both the parent form and an `InlineFormSet`.

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

> In production (Render) `DATABASE_URL` is set automatically and overrides
> the individual `DB_*` vars (parsed by `dj-database-url` with SSL required).

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

`requirements.txt` includes Django, DRF, `psycopg2-binary`, `python-decouple`,
`Pillow`, `django-cors-headers`, `gunicorn`, `whitenoise`, `dj-database-url`,
`cloudinary`, and `django-cloudinary-storage`.

### 4.2 Run migrations

```bash
python manage.py migrate
```

### 4.3 Create a dashboard user

The dashboard's login page authenticates against any Django user with
`is_staff=True`. Create one with:

```bash
python manage.py createsuperuser
```

For automated environments (Render), the included `ensure_superuser`
command reads `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, and
`DJANGO_SUPERUSER_PASSWORD` from env vars and creates / updates the user
idempotently — it's invoked by `build.sh`.

### 4.4 Run the server

```bash
python manage.py runserver
```

Open:

- Dashboard: <http://127.0.0.1:8000/dashboard/>
- API root:  <http://127.0.0.1:8000/api/home/>

Visiting `/` redirects to `/dashboard/`.

---

## 5. Content Model

Every section is a **singleton** (`SingletonModel`, pk=1, `delete()` is a
no-op, `load()` get-or-creates). Sections with repeating sub-items use a
child model linked by `ForeignKey`.

### Site-wide

| Section          | Model              | Highlights                                              |
|------------------|--------------------|---------------------------------------------------------|
| Header           | `HeaderSettings`   | logo + single CTA button, plus dynamic `HeaderTab` rows |
| Footer           | `FooterSettings`   | logo, title, address, email, copyright, dynamic `FooterLink` rows |

### Homepage sections

| Section          | Model                 | Highlights                                                                 |
|------------------|-----------------------|----------------------------------------------------------------------------|
| Hero             | `HeroSection`         | title, description, highlight text, 2 CTAs, background + foreground image  |
| Features         | `FeatureSection`      | heading + shared button label + dynamic `FeatureCard` rows (icon, title, URL) |
| About / Mission  | `AboutSection`        | label, title, description, 2 CTAs, image                                   |
| Network          | `NetworkSection`      | title, optional video, dynamic `NetworkStat` rows (value + label)          |
| Talent Pool      | `TalentPoolSection`   | title, subtitle, description, 2 CTAs, image                                |
| Apply            | `ApplySection`        | title, subtitle, dynamic `ApplyCompany` cards, bottom CTA                  |
| Social Media     | `SocialMediaSection`  | heading + dynamic `SocialMediaCard` rows (name + icon)                     |
| Testimonials     | `TestimonialsSection` | title, background image, 3 fixed user testimonials                         |
| App promotion    | `AppSection`          | title, description, 3 CTAs, side image, barcode image                      |

### Upload rules

- **Images**: max 5 MB. Allowed extensions: `jpg`, `jpeg`, `png`, `webp`, `svg`, `gif`.
- **Videos** (Network section only): size + extension validated by
  `home/validators.py`. Always stored on the local filesystem
  (`home/storage.py`) — Cloudinary is bypassed for videos.
- In **development**: media lives under `media/<section>/`.
- In **production**: when `CLOUDINARY_CLOUD_NAME` is set, image uploads
  switch to `cloudinary_storage.storage.MediaCloudinaryStorage`
  automatically (configured in `settings.STORAGES`).

---

## 6. API Endpoints

Mounted under `/api/home/`. All endpoints are **read-only** (`GET` only) and
return the singleton row for each section.

| Endpoint                       | Returns                                       |
|--------------------------------|-----------------------------------------------|
| `GET /api/home/`               | Aggregate payload — every homepage section    |
| `GET /api/home/hero/`          | Hero section                                  |
| `GET /api/home/features/`      | Feature section + active feature cards        |
| `GET /api/home/about/`         | About / Mission section                       |
| `GET /api/home/network/`       | Network section + stats                       |
| `GET /api/home/talent-pool/`   | Talent Pool section                           |
| `GET /api/home/apply/`         | Apply section + company cards + bottom button |

Aggregate response shape:

```json
{
  "hero":        { "title": "...", "description": "...", "primary_button_text": "...", "background_image": "...", "hero_image": "..." },
  "features":    { "title": "...", "description": "...", "button_text": "...", "cards": [ { "position": 1, "title": "...", "icon": "...", "button_url": "..." } ] },
  "about":       { "label": "...", "title": "...", "description": "...", "image": "...", "primary_button": { "text": "...", "url": "..." }, "secondary_button": { "text": "...", "url": "..." } },
  "network":     { "title": "...", "video_url": "...", "stats": [ { "position": 1, "value": "...", "label": "..." } ] },
  "talent_pool": { "title": "...", "subtitle": "...", "description": "...", "image": "...", "primary_button": { "...": "..." }, "secondary_button": { "...": "..." } },
  "apply":       { "title": "...", "subtitle": "...", "companies": [ { "position": 1, "label": "...", "title": "...", "description": "...", "button_text": "...", "button_url": "...", "large_image": "...", "small_image": "..." } ], "bottom_button": { "text": "...", "url": "..." } }
}
```

> DRF defaults: `PageNumberPagination` (page size 20), JSON + Browsable API
> renderers, `AllowAny` permission on the public API. The aggregate endpoint
> returns the full payload in a single call — convenient for one-shot
> Next.js home-page rendering.

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

- `CORS_ALLOWED_ORIGINS` in `.env` already permits `http://localhost:3000`
  and `http://127.0.0.1:3000` for the Next.js dev server.
- In **dev**, image URLs in the JSON come back as absolute URLs under
  `/media/`. Configure `images.remotePatterns` in `next.config.js` to allow
  `127.0.0.1:8000`.
- In **prod** (when Cloudinary is enabled), image URLs come back as
  `res.cloudinary.com/...` — add that to `images.remotePatterns` too.

---

## 8. The Custom Dashboard

The dashboard at `/dashboard/` is the only editor — Django Admin is not
mounted. Layout: AdminLTE-style sidebar grouped by **module**, with each
module's sections beneath it.

| URL                                  | What it edits                            |
|--------------------------------------|------------------------------------------|
| `/dashboard/login/`                  | Login (any user with `is_staff=True`)    |
| `/dashboard/`                        | Overview — module summary + config stats |
| `/dashboard/header/`                 | Header settings + tabs                   |
| `/dashboard/footer/`                 | Footer settings + links                  |
| `/dashboard/home/`                   | Home module landing page                 |
| `/dashboard/home/hero/`              | Hero section                             |
| `/dashboard/home/features/`          | Feature section + cards                  |
| `/dashboard/home/about/`             | About / Mission section                  |
| `/dashboard/home/network/`           | Network section + stats                  |
| `/dashboard/home/talent-pool/`       | Talent Pool section                      |
| `/dashboard/home/apply/`             | Apply section + companies                |
| `/dashboard/home/social-media/`      | Social Media section + cards             |
| `/dashboard/home/testimonials/`      | Testimonials section                     |
| `/dashboard/home/app/`               | App promotion section                    |

The login page lives at `dashboard:login`; `LOGIN_URL`, `LOGIN_REDIRECT_URL`,
and `LOGOUT_REDIRECT_URL` in `settings.py` already point Django's auth
machinery at it.

---

## 9. Adding a New Section Later

The section model + dashboard registry pattern is designed for extension:

1. **Model** — add a `SingletonModel` subclass in `home/models.py`. If it
   has repeating sub-items, add a child model with a `ForeignKey` back to it.
2. **Serializer + view + URL** — add a serializer in `home/serializers.py`,
   a `RetrieveAPIView` (subclass `_SingletonMixin`) in `home/views.py`, and
   wire it into `home/urls.py`. Don't forget to include it in
   `HomePageSerializer.to_representation` so it's part of the aggregate
   payload.
3. **Form** — add a `ModelForm` (and an `InlineFormSet` if there are child
   rows) in `dashboard/forms.py`.
4. **Dashboard view + URL** — add an `UpdateView` in `dashboard/views.py`
   and a route in `dashboard/urls.py`.
5. **Registry** — append a section dict to the relevant module in
   `dashboard/sections.py`. That single entry adds the section to the
   sidebar, module landing page, and configured-count stats.
6. **Migrate** — `python manage.py makemigrations && python manage.py migrate`.

---

## 10. Deployment (Render)

`render.yaml` is a Render Blueprint that provisions a free Postgres database
plus the web service:

- **Build**: `./build.sh` — `pip install`, `collectstatic`, `migrate`, then
  `ensure_superuser` (which respects `DJANGO_SUPERUSER_*` env vars).
- **Start**: `gunicorn young_professionals.wsgi:application`.
- **Env vars** to set in the Render dashboard (alongside the auto-generated
  `SECRET_KEY` and `DATABASE_URL`):
  - `CORS_ALLOWED_ORIGINS` — your frontend origin(s)
  - `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`,
    `DJANGO_SUPERUSER_EMAIL` — for the initial dashboard user
  - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
    — to switch image uploads to Cloudinary

`whitenoise` serves static files in production with compressed manifest
storage; `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` already cover
`*.onrender.com`.

---

## 11. Common Commands

```bash
# create a new migration after model changes
python manage.py makemigrations

# apply pending migrations
python manage.py migrate

# open a Django shell
python manage.py shell

# collect static (production)
python manage.py collectstatic

# create / update a superuser from env vars (used by build.sh)
python manage.py ensure_superuser
```
