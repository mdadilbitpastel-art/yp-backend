# Young Professionals — Backend (Headless CMS)

A Django + PostgreSQL backend that powers the **Young Professionals** website
as a **Headless CMS**. Content editors manage the site through a fully custom
AdminLTE-style dashboard at `/dashboard/`; the Next.js frontend reads every
section over a read-only REST API mounted under `/api/<page>/` (one
namespace per public page — `home`, `about-us`, `schools`, `employers`,
`partners`, `events`, `insight`, plus shared `data`).

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
│   ├── urls.py                    ← /, /dashboard/, /api/<page>/
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
├── about_us/                      ← About Us page CMS app
├── schools/                       ← Schools page CMS app
├── employers/                     ← Employers page CMS app
├── partners/                      ← Partners page CMS app
├── events/                        ← Events page CMS app
├── insight/                       ← Insight page CMS app
├── data_management/               ← Shared dynamic data (Statistics, Employers,
│                                    Team Members, Social Media Icons,
│                                    SectionImage generic image attachments)
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

- **Per-page apps (`home/`, `about_us/`, `schools/`, `employers/`,
  `partners/`, `events/`, `insight/`)** — each public page has its own
  Django app following the same shape: `models.py` holds one
  `SingletonModel` per section, `serializers.py` shapes the JSON,
  `views.py` exposes read-only `RetrieveAPIView`s, `urls.py` mounts them
  under `/api/<page>/`. Sections with repeating sub-items (cards, points,
  categories, lanes, …) use a child model with a `ForeignKey` back to the
  singleton.
- **`home/models.py`** — also defines the shared `SingletonModel` abstract
  base (pk=1, `delete()` is a no-op, `load()` get-or-creates) plus the
  site-wide `HeaderSettings` / `FooterSettings` singletons and the home
  page's own section models.
- **`data_management/`** — shared rows (`Statistic`, `Employer`,
  `TeamMember`, `SocialMediaIcon`) that consumer sections pick from via
  `ManyToManyField`. `SectionImage` is a generic-FK image row any
  singleton section can own, used by every section's dashboard "Images"
  card so admins upload `image-1`, `image-2`, … rather than fighting
  hard-coded `background_image` / `side_image` slots.
- **`dashboard/sections.py`** — the registry of dashboard modules and their
  sections. Adding an entry here makes it appear in the sidebar, the module
  landing page, and the dashboard overview's "x of y configured" stat.
- **`dashboard/views.py`** — one `UpdateView` per section across every
  module. Sections with child rows post both the parent form and an
  `InlineFormSet`; sections that pick from `data_management` use a JSON
  picker endpoint (`/dashboard/data/<resource>/picker.json`).

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
- Home API:  <http://127.0.0.1:8000/api/home/>
- Other public-page APIs: `/api/about-us/`, `/api/schools/`,
  `/api/employers/`, `/api/partners/`, `/api/events/`, `/api/insight/`
- Shared data API: <http://127.0.0.1:8000/api/data/>

Visiting `/` redirects to `/dashboard/`.

---

## 5. Content Model

Every section is a **singleton** (`SingletonModel`, pk=1, `delete()` is a
no-op, `load()` get-or-creates). Sections with repeating sub-items use a
child model linked by `ForeignKey`. Sections that need imagery use
`data_management.SectionImage` (a generic-FK row) instead of hard-coded
image fields — every section's dashboard exposes the same "Images" card.

### Site-wide

| Section          | Model              | Highlights                                              |
|------------------|--------------------|---------------------------------------------------------|
| Header           | `HeaderSettings`   | logo + single CTA button, plus dynamic `HeaderTab` rows |
| Footer           | `FooterSettings`   | logo, title, address, email, copyright, dynamic `FooterLink` rows |

### Home (`home/models.py`)

| Section          | Model                 | Highlights                                                                 |
|------------------|-----------------------|----------------------------------------------------------------------------|
| Hero             | `HeroSection`         | title, description, highlight text, 2 CTAs, rating, bottom note            |
| Features         | `FeatureSection`      | heading + shared button label + dynamic `FeatureCard` rows (icon, title, URL) |
| About / Mission  | `AboutSection`        | label, title, description, 2 CTAs                                          |
| Network          | `NetworkSection`      | title, optional video, plus selectable statistics from `data_management.Statistic` |
| Talent Pool      | `TalentPoolSection`   | label, title, subtitle, description, 2 CTAs                                |
| Apply            | `ApplySection`        | title, subtitle, selectable employers, dynamic `ApplyCompany` cards, bottom CTA |
| Social Media     | `SocialMediaSection`  | label, heading, subtitle, plus selectable icons from `data_management.SocialMediaIcon` |
| Testimonials     | `TestimonialsSection` | title; testimonials are `TestimonialUser` rows that FK to `data_management.TeamMember` and carry a per-section `message` |
| App promotion    | `AppSection`          | title, description, 3 CTAs, bottom note                                    |

### About Us (`about_us/models.py`)

| Section       | Model                          | Highlights                                                        |
|---------------|--------------------------------|-------------------------------------------------------------------|
| Hero          | `AboutUsHeroSection`           | label, title, description                                         |
| Mission       | `AboutUsMissionSection`        | label, title, description, plus selectable statistics from `data_management.Statistic` (independent of Home Network) |
| Founder       | `AboutUsFounderSection`        | label, founder name, designation, description, founder message, single CTA |
| Values        | `AboutUsValuesSection`         | label, title, subtitle, plus dynamic `AboutUsValueCard` rows (icon, label, note) |
| Journey       | `AboutUsJourneySection`        | label, title, subtitle, plus dynamic `AboutUsJourneyCard` rows (image, title, description) |
| Pledge        | `AboutUsPledgeSection`         | label, title, description                                         |
| Team          | `AboutUsTeamSection`           | label, title, subtitle, plus selectable members from `data_management.TeamMember` |
| Community     | `AboutUsCommunitySection`      | label, title, subtitle, plus dynamic `AboutUsCommunityCard` rows (image, name, description, CTA) |
| Social Media  | `AboutUsSocialMediaSection`    | label, heading, subtitle, plus selectable icons from `data_management.SocialMediaIcon` (independent of Home Social Media) |

### Schools (`schools/models.py`)

| Section    | Model                       | Highlights                                                                 |
|------------|-----------------------------|----------------------------------------------------------------------------|
| Hero       | `SchoolsHeroSection`        | label, title, description, 2 CTAs                                          |
| Help       | `SchoolsHelpSection`        | label, title, plus dynamic `SchoolsHelpCard` rows (title + description)    |
| Employer   | `SchoolsEmployerSection`    | label, title, description, single CTA, plus selectable employers from `data_management.Employer` |
| Benchmark  | `SchoolsBenchmarkSection`   | label, title, description, plus dynamic `SchoolsBenchmarkCard` rows        |
| Subscribe  | `SchoolsSubscribeSection`   | label, title, description, single CTA, plus dynamic `SchoolsSubscribeField` form fields |
| FAQ        | `SchoolsFaqSection`         | label, title, description, plus dynamic `SchoolsFaqItem` Q&A rows          |

### Employers (`employers/models.py`)

| Section  | Model                          | Highlights                                                                |
|----------|--------------------------------|---------------------------------------------------------------------------|
| Hero     | `EmployersHeroSection`         | label, title, description, 2 CTAs                                         |
| Network  | (shared `home.NetworkSection`) | re-uses the Home Network singleton and its selected statistics            |
| Mission  | `EmployersMissionSection`      | label, title, description, single CTA, plus dynamic `EmployersMissionPoint` bullet points |
| Offers   | `EmployersOfferSection`        | label, title, description, plus dynamic `EmployersOfferCard` rows (icon, title, description) |
| Events   | `EmployersEventsSection`       | label, title, description, single CTA, plus dynamic `EmployersEventImage` rows |

### Partners (`partners/models.py`)

| Section          | Model                       | Highlights                                                                       |
|------------------|-----------------------------|----------------------------------------------------------------------------------|
| Hero             | `PartnersHeroSection`       | label, title, description, plus selectable statistics from `data_management.Statistic` |
| Partner Section  | `PartnersPartnerSection`    | search placeholder, explore button text, dynamic `PartnersCategory` rows, plus selectable employers |
| Family           | `PartnersFamilySection`     | label, title, description, selectable employers, Load More CTA                   |
| Review           | `PartnersReviewSection`     | label, title, plus dynamic `PartnersReviewCard` rows (name, designation, message) |
| Founder          | `PartnersFounderSection`    | label, title, description, 2 CTAs                                                |

### Events (`events/models.py`)

| Section    | Model                       | Highlights                                                                          |
|------------|-----------------------------|-------------------------------------------------------------------------------------|
| Hero       | `EventsHeroSection`         | label, title, description, 2 CTAs                                                   |
| Featured   | `EventsFeaturedSection`     | label, free-form datetime label, title, description, category label, single CTA     |
| Upcoming   | `EventsUpcomingSection`     | label, title, shared card button label, plus dynamic `EventsUpcomingCategory` and `EventsUpcomingCard` rows (image, title, description, years, price, URL) |
| Missed     | `EventsMissedSection`       | label, title, description, shared card button label, plus dynamic `EventsMissedCard` rows (video, title, date label, URL) |
| Submit     | `EventsSubmitSection`       | label, title, description, single CTA                                               |

### Insight (`insight/models.py`)

| Section           | Model                          | Highlights                                                                       |
|-------------------|--------------------------------|----------------------------------------------------------------------------------|
| Hero              | `InsightHeroSection`           | label, title, description, search placeholder                                    |
| Founder Section   | `InsightFounderSection`        | dynamic `InsightFounderCategory` labels, label-1, label-2, date label, title, description, meta data line, single CTA |
| Article Section   | `InsightArticleSection`        | title, shared card button text, plus dynamic `InsightArticleCard` rows (label, image, date, title, description, tag, URL) |
| Lane Section      | `InsightLaneSection`           | label, title, plus dynamic `InsightLane` rows (name, article count, URL)         |
| Subscribe Section | `InsightSubscribeSection`      | label, title, description, email placeholder, subscribe CTA, bottom note         |

### Data Management (`data_management/models.py`)

Shared dynamic data — each section above that says "selectable X from
`data_management`" reads from these tables. Edited at
`/dashboard/data/...`.

| Resource           | Model              | Highlights                                                       |
|--------------------|--------------------|------------------------------------------------------------------|
| Statistics         | `Statistic`        | value, label, global order (used by Home Network, About Us Mission, Partners Hero) |
| Employers          | `Employer`         | name, logo, description, URL (used by Home Apply, Schools Employer, Partners Partner / Family) |
| Team Members       | `TeamMember`       | name, profile image, designation, email URL, view-profile link (used by About Us Team and Home Testimonials) |
| Social Media Icons | `SocialMediaIcon`  | name, icon (used by Home Social Media and About Us Social Media) |
| Section Images     | `SectionImage`     | generic-FK image attached to any singleton section; powers the dashboard "Images" card for every section that needs imagery |

### Upload rules

- **Images**: max 5 MB. Allowed extensions: `jpg`, `jpeg`, `png`, `webp`, `svg`, `gif`.
- **Videos** (Home Network section + Events Missed cards): size + extension
  validated by `home/validators.py`. Always stored on the local filesystem
  via `home/storage.py` — Cloudinary is bypassed for videos.
- In **development**: media lives under `media/<section>/`.
- In **production**: when `CLOUDINARY_CLOUD_NAME` is set, image uploads
  switch to `cloudinary_storage.storage.MediaCloudinaryStorage`
  automatically (configured in `settings.STORAGES`).

---

## 6. API Endpoints

Every public page has its own URL namespace under `/api/`. Each namespace
exposes one aggregate endpoint (the page's full payload in one call) plus
one read-only endpoint per section. All endpoints are **GET-only** and
return the singleton row for each section.

### Home (`/api/home/`)

| Endpoint                          | Returns                                       |
|-----------------------------------|-----------------------------------------------|
| `GET /api/home/`                  | Aggregate payload — every homepage section    |
| `GET /api/home/header/`           | Site-wide header settings + tabs              |
| `GET /api/home/footer/`           | Site-wide footer settings + links             |
| `GET /api/home/hero/`             | Hero section                                  |
| `GET /api/home/features/`         | Feature section + feature cards               |
| `GET /api/home/about/`            | About / Mission section                       |
| `GET /api/home/network/`          | Network section + selected statistics         |
| `GET /api/home/talent-pool/`      | Talent Pool section                           |
| `GET /api/home/apply/`            | Apply section + company cards + bottom button |
| `GET /api/home/social-media/`     | Social Media section + selected icons         |
| `GET /api/home/testimonials/`     | Testimonials section + picked members' messages |
| `GET /api/home/app/`              | App promotion section                         |

### About Us (`/api/about-us/`)

| Endpoint                              | Returns                                |
|---------------------------------------|----------------------------------------|
| `GET /api/about-us/`                  | Aggregate payload                      |
| `GET /api/about-us/hero/`             | Hero section                           |
| `GET /api/about-us/mission/`          | Mission section + selected statistics  |
| `GET /api/about-us/founder/`          | Founder section                        |
| `GET /api/about-us/values/`           | Values section + value cards           |
| `GET /api/about-us/journey/`          | Journey section + journey cards        |
| `GET /api/about-us/pledge/`           | Pledge section                         |
| `GET /api/about-us/team/`             | Team section + selected team members   |
| `GET /api/about-us/community/`        | Community section + community cards    |
| `GET /api/about-us/social-media/`     | Social Media section + selected icons  |

### Schools (`/api/schools/`)

| Endpoint                          | Returns                                |
|-----------------------------------|----------------------------------------|
| `GET /api/schools/`               | Aggregate payload                      |
| `GET /api/schools/hero/`          | Hero section                           |
| `GET /api/schools/help/`          | Help section + help cards              |
| `GET /api/schools/employer/`      | Employer section + selected employers  |
| `GET /api/schools/benchmark/`     | Benchmark section + benchmark cards    |
| `GET /api/schools/subscribe/`     | Subscribe section + form fields        |
| `GET /api/schools/faq/`           | FAQ section + Q&A items                |

### Employers (`/api/employers/`)

| Endpoint                          | Returns                                          |
|-----------------------------------|--------------------------------------------------|
| `GET /api/employers/`             | Aggregate payload                                |
| `GET /api/employers/hero/`        | Hero section                                     |
| `GET /api/employers/network/`     | Network section (shared with Home) + statistics  |
| `GET /api/employers/mission/`     | Mission section + bullet points                  |
| `GET /api/employers/offer/`       | Offers section + offer cards                     |
| `GET /api/employers/events/`      | Events section + event images                    |

### Partners (`/api/partners/`)

| Endpoint                          | Returns                                                      |
|-----------------------------------|--------------------------------------------------------------|
| `GET /api/partners/`              | Aggregate payload                                            |
| `GET /api/partners/hero/`         | Hero section + selected statistics                           |
| `GET /api/partners/partner/`      | Partner Section — categories + selected employers            |
| `GET /api/partners/family/`       | Family section + selected employers + load-more CTA          |
| `GET /api/partners/review/`       | Review section + review cards                                |
| `GET /api/partners/founder/`      | Founder section                                              |

### Events (`/api/events/`)

| Endpoint                          | Returns                                |
|-----------------------------------|----------------------------------------|
| `GET /api/events/`                | Aggregate payload                      |
| `GET /api/events/hero/`           | Hero section                           |
| `GET /api/events/featured/`       | Featured section                       |
| `GET /api/events/upcoming/`       | Upcoming section + categories + cards  |
| `GET /api/events/missed/`         | Missed section + cards (with videos)   |
| `GET /api/events/submit/`         | Submit section                         |

### Insight (`/api/insight/`)

| Endpoint                          | Returns                                       |
|-----------------------------------|-----------------------------------------------|
| `GET /api/insight/`               | Aggregate payload                             |
| `GET /api/insight/hero/`          | Hero section                                  |
| `GET /api/insight/founder/`       | Founder section + categories                  |
| `GET /api/insight/article/`       | Article section + article cards               |
| `GET /api/insight/lane/`          | Lane section + lanes                          |
| `GET /api/insight/subscribe/`     | Subscribe section                             |

### Shared data (`/api/data/`)

Plain lists of the shared dynamic rows that consumer sections pick from.

| Endpoint                              | Returns                                |
|---------------------------------------|----------------------------------------|
| `GET /api/data/statistics/`           | All `Statistic` rows                   |
| `GET /api/data/employers/`            | All `Employer` rows                    |
| `GET /api/data/team-members/`         | All `TeamMember` rows                  |
| `GET /api/data/social-media/`         | All `SocialMediaIcon` rows             |

> DRF defaults: `PageNumberPagination` (page size 20), JSON + Browsable API
> renderers, `AllowAny` permission on the public API. Per-page aggregate
> endpoints return the full payload in a single call — convenient for
> one-shot Next.js page rendering.

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

### Auth + overview

| URL                                  | What it edits                            |
|--------------------------------------|------------------------------------------|
| `/dashboard/login/`                  | Login (any user with `is_staff=True`)    |
| `/dashboard/logout/`                 | Logout                                   |
| `/dashboard/`                        | Overview — module summary + config stats |

### Site-wide

| URL                                  | What it edits                            |
|--------------------------------------|------------------------------------------|
| `/dashboard/header/`                 | Header settings + tabs                   |
| `/dashboard/footer/`                 | Footer settings + links                  |

### Home Management

| URL                                  | What it edits                            |
|--------------------------------------|------------------------------------------|
| `/dashboard/home/`                   | Home module landing page                 |
| `/dashboard/home/hero/`              | Hero section                             |
| `/dashboard/home/features/`          | Feature section + cards                  |
| `/dashboard/home/about/`             | About / Mission section                  |
| `/dashboard/home/network/`           | Network section + selected statistics    |
| `/dashboard/home/talent-pool/`       | Talent Pool section                      |
| `/dashboard/home/apply/`             | Apply section + companies                |
| `/dashboard/home/social-media/`      | Social Media section + selected icons    |
| `/dashboard/home/testimonials/`      | Testimonials section + picked members    |
| `/dashboard/home/app/`               | App promotion section                    |

### About Us Management

| URL                                  | What it edits                            |
|--------------------------------------|------------------------------------------|
| `/dashboard/about-us/`               | About Us module landing page             |
| `/dashboard/about-us/hero/`          | Hero section                             |
| `/dashboard/about-us/mission/`       | Mission section + selected statistics    |
| `/dashboard/about-us/founder/`       | Founder section                          |
| `/dashboard/about-us/values/`        | Values section + value cards             |
| `/dashboard/about-us/journey/`       | Journey section + journey cards          |
| `/dashboard/about-us/pledge/`        | Pledge section                           |
| `/dashboard/about-us/team/`          | Team section + selected team members     |
| `/dashboard/about-us/community/`     | Community section + community cards      |
| `/dashboard/about-us/social-media/`  | Social Media section + selected icons    |

### Schools Management

| URL                                  | What it edits                            |
|--------------------------------------|------------------------------------------|
| `/dashboard/schools/`                | Schools module landing page              |
| `/dashboard/schools/hero/`           | Hero section                             |
| `/dashboard/schools/help/`           | Help section + help cards                |
| `/dashboard/schools/employer/`       | Employer section + selected employers    |
| `/dashboard/schools/benchmark/`      | Benchmark section + benchmark cards      |
| `/dashboard/schools/subscribe/`      | Subscribe section + form fields          |
| `/dashboard/schools/faq/`            | FAQ section + Q&A items                  |

### Employers Management

| URL                                  | What it edits                            |
|--------------------------------------|------------------------------------------|
| `/dashboard/employers/`              | Employers module landing page            |
| `/dashboard/employers/hero/`         | Hero section                             |
| `/dashboard/employers/network/`      | Network section (shared with Home)       |
| `/dashboard/employers/mission/`      | Mission section + bullet points          |
| `/dashboard/employers/offer/`        | Offers section + offer cards             |
| `/dashboard/employers/events/`       | Events section + event images            |

### Partner Management

| URL                                       | What it edits                            |
|-------------------------------------------|------------------------------------------|
| `/dashboard/partners/`                    | Partners module landing page             |
| `/dashboard/partners/hero/`               | Hero section + selected statistics       |
| `/dashboard/partners/partner-section/`    | Partner Section — categories + employers |
| `/dashboard/partners/family-section/`     | Family section + selected employers      |
| `/dashboard/partners/review-section/`     | Review section + review cards            |
| `/dashboard/partners/founder-section/`    | Founder section                          |

### Events Management

| URL                                  | What it edits                            |
|--------------------------------------|------------------------------------------|
| `/dashboard/events/`                 | Events module landing page               |
| `/dashboard/events/hero/`            | Hero section                             |
| `/dashboard/events/featured/`        | Featured section                         |
| `/dashboard/events/upcoming/`        | Upcoming section + categories + cards    |
| `/dashboard/events/missed/`          | Missed section + cards (videos)          |
| `/dashboard/events/submit/`          | Submit section                           |

### Insight Management

| URL                                          | What it edits                            |
|----------------------------------------------|------------------------------------------|
| `/dashboard/insight/`                        | Insight module landing page              |
| `/dashboard/insight/hero/`                   | Hero section                             |
| `/dashboard/insight/founder-section/`        | Founder section + categories             |
| `/dashboard/insight/article-section/`        | Article section + article cards          |
| `/dashboard/insight/lane-section/`           | Lane section + lanes                     |
| `/dashboard/insight/subscribe-section/`      | Subscribe section                        |

### Data Management

Shared dynamic rows that consumer sections pick from.

| URL                                            | What it edits                            |
|------------------------------------------------|------------------------------------------|
| `/dashboard/data/`                             | Data module landing page                 |
| `/dashboard/data/statistics/`                  | Statistics (value + label)               |
| `/dashboard/data/employers/`                   | Employers (name, logo, description, URL) |
| `/dashboard/data/team-members/`                | Team Members                             |
| `/dashboard/data/social-media/`                | Social Media Icons                       |
| `/dashboard/data/team-members/picker.json`     | JSON picker used by Team / Testimonial selectors |
| `/dashboard/data/employers/picker.json`        | JSON picker used by Employer selectors   |

The login page lives at `dashboard:login`; `LOGIN_URL`, `LOGIN_REDIRECT_URL`,
and `LOGOUT_REDIRECT_URL` in `settings.py` already point Django's auth
machinery at it.

---

## 9. Adding a New Section Later

The section model + dashboard registry pattern is designed for extension.
New sections in any module (Home, About Us, Schools, Employers, Partners,
Events, Insight, …) follow the same shape — substitute the relevant
per-app `models.py` / `serializers.py` / `views.py` / `urls.py`:

1. **Model** — add a `SingletonModel` subclass in the target app's
   `models.py` (subclass `home.models.SingletonModel`). If it has
   repeating sub-items, add a child model with a `ForeignKey` back to it.
2. **Serializer + view + URL** — add a serializer in the app's
   `serializers.py`, a `RetrieveAPIView` (subclass the app's singleton
   mixin) in `views.py`, and wire it into the app's `urls.py`. Don't
   forget to include it in the page's aggregate serializer so it's part
   of the aggregate payload.
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
