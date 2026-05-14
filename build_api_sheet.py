"""Generate two CSV files documenting the public REST API.

Open them in Google Sheets via File → Import → Upload, or paste them
into separate tabs of an existing sheet.

Output files (saved next to this script):
  - api_endpoints.csv   one row per endpoint (URL, method, returns…)
  - api_payload.csv     one row per field in every endpoint's response

The data is hand-curated from the DRF serializers in each app, so it
captures the actual shape returned by the public API.
"""
from __future__ import annotations

import csv
import os
from typing import List, Tuple

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# Endpoints overview
# Tuple shape: (Page, Section, Method, URL, Auth, Description)
# --------------------------------------------------------------------------
ENDPOINTS: List[Tuple[str, str, str, str, str, str]] = [
    # Home
    ("Home", "Page payload",      "GET", "/api/home/",                "Public", "Full Home page payload — every section + header + footer in one response."),
    ("Home", "Header",            "GET", "/api/home/header/",         "Public", "Site header (logo, CTA button, navigation tabs)."),
    ("Home", "Footer",            "GET", "/api/home/footer/",         "Public", "Site footer (logo, title, address, email, copyright, links)."),
    ("Home", "Hero",              "GET", "/api/home/hero/",           "Public", "Hero section — headline, buttons, rating, images."),
    ("Home", "Features",          "GET", "/api/home/features/",       "Public", "Feature section — title/description + cards array."),
    ("Home", "About",             "GET", "/api/home/about/",          "Public", "About/Mission section — label/title/description + images + 2 buttons."),
    ("Home", "Network",           "GET", "/api/home/network/",        "Public", "Network/Stats section — title, video URL, statistics."),
    ("Home", "Talent Pool",       "GET", "/api/home/talent-pool/",    "Public", "Talent Pool section — label/title/subtitle/description + images + 2 buttons."),
    ("Home", "Apply",             "GET", "/api/home/apply/",          "Public", "Apply section — title/subtitle + company cards + employer logos + bottom button."),
    ("Home", "Social Media",      "GET", "/api/home/social-media/",   "Public", "Social Media section — label/heading/subtitle + icon cards."),
    ("Home", "Testimonials",      "GET", "/api/home/testimonials/",   "Public", "Testimonials section — title + images + users."),
    ("Home", "App",               "GET", "/api/home/app/",            "Public", "App promo section — title/description + buttons + bottom note + images."),

    # About Us
    ("About Us", "Page payload",  "GET", "/api/about-us/",                "Public", "Full About Us page payload — every section in one response."),
    ("About Us", "Hero",          "GET", "/api/about-us/hero/",           "Public", "About Us hero — label, title, description, images."),
    ("About Us", "Mission",       "GET", "/api/about-us/mission/",        "Public", "Mission section — label/title/description + images + stats."),
    ("About Us", "Founder",       "GET", "/api/about-us/founder/",        "Public", "Founder section — name, designation, description, message, button, images."),
    ("About Us", "Values",        "GET", "/api/about-us/values/",         "Public", "Values section — label/title/subtitle + value cards."),
    ("About Us", "Journey",       "GET", "/api/about-us/journey/",        "Public", "Journey section — label/title/subtitle + milestone cards."),
    ("About Us", "Pledge",        "GET", "/api/about-us/pledge/",         "Public", "Pledge section — label/title/description + images."),
    ("About Us", "Team",          "GET", "/api/about-us/team/",           "Public", "Team section — label/title/subtitle + team members."),
    ("About Us", "Community",     "GET", "/api/about-us/community/",      "Public", "Community section — label/title/subtitle + cards."),
    ("About Us", "Social Media",  "GET", "/api/about-us/social-media/",   "Public", "About Us social media — label/heading/subtitle + icon cards."),

    # Schools
    ("Schools", "Page payload",   "GET", "/api/schools/",                 "Public", "Full Schools page payload — every section in one response."),
    ("Schools", "Hero",           "GET", "/api/schools/hero/",            "Public", "Schools hero — label/title/description + 2 buttons + images."),
    ("Schools", "Help",           "GET", "/api/schools/help/",            "Public", "Help section — label/title + help cards."),
    ("Schools", "Employer",       "GET", "/api/schools/employer/",        "Public", "Employer section — label/title/description + button + employer logos."),
    ("Schools", "Benchmark",      "GET", "/api/schools/benchmark/",       "Public", "Benchmark section — label/title/description + benchmark cards."),
    ("Schools", "Subscribe",      "GET", "/api/schools/subscribe/",       "Public", "Subscribe section — label/title/description + button + form fields + images."),
    ("Schools", "FAQ",            "GET", "/api/schools/faq/",             "Public", "FAQ section — label/title/description + Q&A items."),

    # Employers
    ("Employers", "Page payload", "GET", "/api/employers/",               "Public", "Full Employers page payload — every section in one response."),
    ("Employers", "Hero",         "GET", "/api/employers/hero/",          "Public", "Employers hero — label/title/description + 2 buttons + images."),
    ("Employers", "Network",      "GET", "/api/employers/network/",       "Public", "Network section (shared with Home) — title + video + stats."),
    ("Employers", "Mission",      "GET", "/api/employers/mission/",       "Public", "Mission section — label/title/description + button + points + images."),
    ("Employers", "Offer",        "GET", "/api/employers/offer/",         "Public", "Offer section — label/title/description + cards."),
    ("Employers", "Events",       "GET", "/api/employers/events/",        "Public", "Events section — label/title/description + button + images."),

    # Partners
    ("Partners", "Page payload",  "GET", "/api/partners/",                "Public", "Full Partners page payload — every section in one response."),
    ("Partners", "Hero",          "GET", "/api/partners/hero/",           "Public", "Partners hero — label/title/description + stats."),
    ("Partners", "Partner",       "GET", "/api/partners/partner/",        "Public", "Partner section — search placeholder + explore button + categories + employer cards."),
    ("Partners", "Family",        "GET", "/api/partners/family/",         "Public", "Family section — label/title/description + employer cards + load-more button."),
    ("Partners", "Review",        "GET", "/api/partners/review/",         "Public", "Review section — label/title + review cards."),
    ("Partners", "Founder",       "GET", "/api/partners/founder/",        "Public", "Founder section — label/title/description + 2 buttons + images."),

    # Events
    ("Events", "Page payload",    "GET", "/api/events/",                  "Public", "Full Events page payload — every section in one response."),
    ("Events", "Hero",            "GET", "/api/events/hero/",             "Public", "Events hero — label/title/description + 2 buttons."),
    ("Events", "Featured",        "GET", "/api/events/featured/",         "Public", "Featured event — label/datetime/title/description/category + button + images."),
    ("Events", "Upcoming",        "GET", "/api/events/upcoming/",         "Public", "Upcoming events — label/title + shared card button + categories + event cards."),
    ("Events", "Missed",          "GET", "/api/events/missed/",           "Public", "Missed events — label/title/description + shared card button + video cards."),
    ("Events", "Submit",          "GET", "/api/events/submit/",           "Public", "Submit-an-event section — label/title/description + button + images."),

    # Insight
    ("Insight", "Page payload",   "GET", "/api/insight/",                 "Public", "Full Insight page payload — every section in one response."),
    ("Insight", "Hero",           "GET", "/api/insight/hero/",            "Public", "Insight hero — label/title/description + search placeholder."),
    ("Insight", "Founder",        "GET", "/api/insight/founder/",         "Public", "Founder spotlight — labels/date/title/description/meta + button + categories + images."),
    ("Insight", "Article",        "GET", "/api/insight/article/",         "Public", "Article section — title + shared card button + article cards."),
    ("Insight", "Lane",           "GET", "/api/insight/lane/",            "Public", "Lanes section — label/title + lane cards."),
    ("Insight", "Subscribe",      "GET", "/api/insight/subscribe/",       "Public", "Subscribe section — label/title/description + email placeholder + button + bottom note + images."),
]


# --------------------------------------------------------------------------
# Per-field payload reference
# Tuple shape: (URL, Field path, Type, Notes)
# --------------------------------------------------------------------------
# Reusable groups
HEADER_FIELDS = [
    ("logo",         "string|null (absolute URL)",  "Header logo image."),
    ("button_text",  "string",                     "CTA button label."),
    ("button_url",   "string",                     "CTA button URL (path or full URL)."),
    ("tabs[].label", "string",                     "Tab label."),
    ("tabs[].url",   "string",                     "Tab URL (path or full URL)."),
]
FOOTER_FIELDS = [
    ("logo",            "string|null", "Footer logo image."),
    ("title",           "string",      "Footer title."),
    ("address",         "string",      "Postal address."),
    ("email",           "string",      "Contact email."),
    ("copyright_text",  "string",      "Copyright string."),
    ("links[].label",   "string",      "Link label."),
    ("links[].url",     "string (URL)", "Link URL."),
]
HERO_FIELDS = [
    ("id",                          "integer",        "Hero record id."),
    ("title",                       "string",         "Headline."),
    ("description",                 "string",         "Subheadline / paragraph."),
    ("highlight_text",              "string",         "Word/phrase highlighted in headline."),
    ("primary_button.text",         "string",         "Primary CTA text."),
    ("primary_button.url",          "string",         "Primary CTA URL."),
    ("secondary_button.text",       "string",         "Secondary CTA text."),
    ("secondary_button.url",        "string",         "Secondary CTA URL."),
    ("rating",                      "number|null",    "Out of 5, decimal."),
    ("bottom_note",                 "string",         "Small note under the buttons."),
    ("images[]",                    "string (URL)[]", "Array of absolute image URLs from SectionImage."),
]
FEATURE_FIELDS = [
    ("title",                  "string",        "Section title."),
    ("description",            "string",        "Section description."),
    ("button_text",            "string",        "Shared CTA text used on every card."),
    ("cards[].position",       "integer",       "1-based position."),
    ("cards[].title",          "string",        "Card title."),
    ("cards[].icon",           "string|null",   "Card icon URL."),
    ("cards[].button_url",     "string (URL)",  "Per-card URL."),
]
ABOUT_HOME_FIELDS = [
    ("label",                  "string",        "Small label/eyebrow text."),
    ("title",                  "string",        "Section title."),
    ("description",            "string",        "Section body copy."),
    ("images[]",               "string (URL)[]","Section images."),
    ("primary_button.text",    "string",        "Primary CTA text."),
    ("primary_button.url",     "string",        "Primary CTA URL."),
    ("secondary_button.text",  "string",        "Secondary CTA text."),
    ("secondary_button.url",   "string",        "Secondary CTA URL."),
]
NETWORK_FIELDS = [
    ("title",          "string",        "Section title."),
    ("video_url",      "string|null",   "Background video URL."),
    ("stats[]",        "object[]",      "List of selected Statistic rows ({value, label})."),
]
TALENT_FIELDS = [
    ("label",                  "string",        "Small label."),
    ("title",                  "string",        "Section title."),
    ("subtitle",               "string",        "Sub-tagline."),
    ("description",            "string",        "Section body copy."),
    ("images[]",               "string (URL)[]","Section images."),
    ("primary_button.text",    "string",        "Primary CTA text."),
    ("primary_button.url",     "string",        "Primary CTA URL."),
    ("secondary_button.text",  "string",        "Secondary CTA text."),
    ("secondary_button.url",   "string",        "Secondary CTA URL."),
]
APPLY_FIELDS = [
    ("title",                            "string",       "Section title."),
    ("subtitle",                         "string",       "Section subtitle."),
    ("companies[].position",             "integer",      "1-based position."),
    ("companies[].label",                "string",       "Tag/eyebrow text."),
    ("companies[].title",                "string",       "Company name."),
    ("companies[].description",          "string",       "Description text."),
    ("companies[].button_text",          "string",       "CTA text."),
    ("companies[].button_url",           "string (URL)", "CTA URL."),
    ("companies[].image",                "string|null",  "Large company image URL."),
    ("companies[].logo",                 "string|null",  "Small company logo URL."),
    ("employer_logos[].position",        "integer",      "1-based position."),
    ("employer_logos[].name",            "string",       "Employer name."),
    ("employer_logos[].logo",            "string|null",  "Employer logo URL."),
    ("employer_logos[].description",     "string",       "Employer description."),
    ("employer_logos[].url",             "string (URL)", "Employer site URL."),
    ("bottom_button.text",               "string",       "Bottom button text."),
    ("bottom_button.url",                "string",       "Bottom button URL."),
]
SOCIAL_HOME_FIELDS = [
    ("label",                "string",       "Small label."),
    ("heading",              "string",       "Section title."),
    ("subtitle",             "string",       "Section subtitle."),
    ("cards[].position",     "integer",      "1-based position."),
    ("cards[].name",         "string",       "Social platform name."),
    ("cards[].icon",         "string|null",  "Icon URL."),
]
TESTIMONIALS_FIELDS = [
    ("title",                     "string",        "Section title."),
    ("images[]",                  "string (URL)[]","Background images."),
    ("users[].position",          "integer",       "1-based position."),
    ("users[].name",              "string",        "Person's name."),
    ("users[].profile_image",     "string|null",   "Profile photo URL."),
    ("users[].message",           "string",        "Testimonial message."),
]
APP_FIELDS = [
    ("title",                "string",        "Section title."),
    ("description",          "string",        "Description body."),
    ("buttons[].position",   "integer",       "1-based position."),
    ("buttons[].text",       "string",        "Button label."),
    ("buttons[].url",        "string (URL)",  "Button URL."),
    ("bottom_note",          "string",        "Small note under the buttons."),
    ("images[]",             "string (URL)[]","Section images (e.g. phone mockup, barcode)."),
]

# About Us section field lists
ABOUTUS_HERO = [
    ("id", "integer", "Hero record id."),
    ("label", "string", "Small label."),
    ("title", "string", "Hero title."),
    ("description", "string", "Hero description."),
    ("images[]", "string (URL)[]", "Hero images."),
]
ABOUTUS_MISSION = [
    ("label", "string", "Small label."),
    ("title", "string", "Title."),
    ("description", "string", "Description."),
    ("images[]", "string (URL)[]", "Mission images."),
    ("stats[]", "object[]", "Selected Statistic rows ({value, label})."),
]
ABOUTUS_FOUNDER = [
    ("label", "string", "Small label."),
    ("founder_name", "string", "Founder's name."),
    ("designation", "string", "Job title."),
    ("description", "string", "Bio paragraph."),
    ("founder_message", "string", "Personal quote/message."),
    ("images[]", "string (URL)[]", "Founder photos."),
    ("button.text", "string", "CTA text."),
    ("button.url", "string", "CTA URL."),
]
ABOUTUS_VALUES = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("subtitle", "string", "Subtitle."),
    ("cards[].position", "integer", "1-based position."),
    ("cards[].icon", "string|null", "Icon URL."),
    ("cards[].label", "string", "Card label."),
    ("cards[].note", "string", "Card note/body."),
]
ABOUTUS_JOURNEY = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("subtitle", "string", "Subtitle."),
    ("cards[].position", "integer", "1-based position."),
    ("cards[].image", "string|null", "Card image URL."),
    ("cards[].title", "string", "Milestone title."),
    ("cards[].description", "string", "Milestone description."),
]
ABOUTUS_PLEDGE = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Pledge text."),
    ("images[]", "string (URL)[]", "Section images."),
]
ABOUTUS_TEAM = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("subtitle", "string", "Subtitle."),
    ("members[].position", "integer", "1-based position."),
    ("members[].profile_image", "string|null", "Profile photo URL."),
    ("members[].name", "string", "Full name."),
    ("members[].designation", "string", "Designation."),
    ("members[].email_url", "string", "mailto: link."),
    ("members[].view_profile_text", "string", "View-profile link label."),
    ("members[].view_profile_url", "string (URL)", "View-profile link URL."),
]
ABOUTUS_COMMUNITY = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("subtitle", "string", "Subtitle."),
    ("cards[].position", "integer", "1-based position."),
    ("cards[].image", "string|null", "Card image URL."),
    ("cards[].name", "string", "Card name."),
    ("cards[].description", "string", "Card description."),
    ("cards[].button.text", "string", "Card button text."),
    ("cards[].button.url", "string", "Card button URL."),
]
ABOUTUS_SOCIAL = [
    ("label", "string", "Small label."),
    ("heading", "string", "Section title."),
    ("subtitle", "string", "Subtitle."),
    ("cards[].position", "integer", "1-based position."),
    ("cards[].name", "string", "Platform name."),
    ("cards[].icon", "string|null", "Icon URL."),
]

# Schools
SCHOOLS_HERO = [
    ("label", "string", "Small label."),
    ("title", "string", "Hero title."),
    ("description", "string", "Hero description."),
    ("primary_button.text", "string", "Primary CTA text."),
    ("primary_button.url", "string", "Primary CTA URL."),
    ("secondary_button.text", "string", "Secondary CTA text."),
    ("secondary_button.url", "string", "Secondary CTA URL."),
    ("images[]", "string (URL)[]", "Hero images."),
]
SCHOOLS_HELP = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("cards[].position", "integer", "1-based position."),
    ("cards[].title", "string", "Card title."),
    ("cards[].description", "string", "Card description."),
]
SCHOOLS_EMPLOYER = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Section description."),
    ("button.text", "string", "CTA text."),
    ("button.url", "string", "CTA URL."),
    ("employers[].position", "integer", "1-based position."),
    ("employers[].name", "string", "Employer name."),
    ("employers[].logo", "string|null", "Employer logo URL."),
]
SCHOOLS_BENCHMARK = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Section description."),
    ("cards[].position", "integer", "1-based position."),
    ("cards[].title", "string", "Card title."),
    ("cards[].description", "string", "Card description."),
]
SCHOOLS_SUBSCRIBE = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Section description."),
    ("button.text", "string", "Subscribe button text."),
    ("button.url", "string", "Subscribe button URL."),
    ("fields[].position", "integer", "1-based position."),
    ("fields[].field_name", "string", "Display name of the field."),
    ("fields[].placeholder", "string", "Input placeholder."),
    ("images[]", "string (URL)[]", "Section images."),
]
SCHOOLS_FAQ = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Section description."),
    ("items[].position", "integer", "1-based position."),
    ("items[].question", "string", "FAQ question."),
    ("items[].answer", "string", "FAQ answer."),
]

# Employers
EMP_HERO = SCHOOLS_HERO  # same shape
EMP_MISSION = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Section description."),
    ("button.text", "string", "CTA text."),
    ("button.url", "string", "CTA URL."),
    ("points[].position", "integer", "1-based position."),
    ("points[].text", "string", "Bullet point text."),
    ("images[]", "string (URL)[]", "Section images."),
]
EMP_OFFER = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Section description."),
    ("cards[].position", "integer", "1-based position."),
    ("cards[].icon", "string|null", "Icon URL."),
    ("cards[].title", "string", "Card title."),
    ("cards[].description", "string", "Card description."),
]
EMP_EVENTS = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Section description."),
    ("button.text", "string", "CTA text."),
    ("button.url", "string", "CTA URL."),
    ("images[].position", "integer", "1-based position."),
    ("images[].image", "string|null", "Image URL."),
]

# Partners
PRT_HERO = [
    ("label", "string", "Small label."),
    ("title", "string", "Hero title."),
    ("description", "string", "Hero description."),
    ("stats[]", "object[]", "Selected Statistic rows ({value, label})."),
]
PRT_PARTNER = [
    ("search_placeholder", "string", "Placeholder for the partner search box."),
    ("explore_button_text", "string", "Explore button label."),
    ("categories[].position", "integer", "1-based position."),
    ("categories[].name", "string", "Category name."),
    ("employers[].position", "integer", "1-based position."),
    ("employers[].name", "string", "Partner name."),
    ("employers[].logo", "string|null", "Partner logo URL."),
    ("employers[].description", "string", "Partner description."),
    ("employers[].url", "string (URL)", "Partner site URL."),
]
PRT_FAMILY = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Section description."),
    ("employers[].position", "integer", "1-based position."),
    ("employers[].name", "string", "Partner name."),
    ("employers[].logo", "string|null", "Partner logo URL."),
    ("employers[].description", "string", "Partner description."),
    ("employers[].url", "string (URL)", "Partner site URL."),
    ("load_more_button.text", "string", "Load-more button text."),
    ("load_more_button.url", "string", "Load-more button URL."),
]
PRT_REVIEW = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("cards[].position", "integer", "1-based position."),
    ("cards[].name", "string", "Reviewer name."),
    ("cards[].designation", "string", "Reviewer designation."),
    ("cards[].message", "string", "Review message."),
]
PRT_FOUNDER = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Section description."),
    ("primary_button.text", "string", "Primary CTA text."),
    ("primary_button.url", "string", "Primary CTA URL."),
    ("secondary_button.text", "string", "Secondary CTA text."),
    ("secondary_button.url", "string", "Secondary CTA URL."),
    ("images[]", "string (URL)[]", "Section images."),
]

# Events
EVT_HERO = [
    ("label", "string", "Small label."),
    ("title", "string", "Hero title."),
    ("description", "string", "Hero description."),
    ("primary_button.text", "string", "Primary CTA text."),
    ("primary_button.url", "string", "Primary CTA URL."),
    ("secondary_button.text", "string", "Secondary CTA text."),
    ("secondary_button.url", "string", "Secondary CTA URL."),
]
EVT_FEATURED = [
    ("label", "string", "Small label."),
    ("datetime_label", "string", "Date/time line."),
    ("title", "string", "Event title."),
    ("description", "string", "Event description."),
    ("category_label", "string", "Category tag."),
    ("button.text", "string", "CTA text."),
    ("button.url", "string", "CTA URL."),
    ("images[]", "string (URL)[]", "Section images."),
]
EVT_UPCOMING = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("card_button_text", "string", "Shared button text used on every card."),
    ("categories[].position", "integer", "1-based position."),
    ("categories[].name", "string", "Category name."),
    ("cards[].position", "integer", "1-based position."),
    ("cards[].image", "string|null", "Card image URL."),
    ("cards[].label", "string", "Card label."),
    ("cards[].title", "string", "Event title."),
    ("cards[].description", "string", "Event description."),
    ("cards[].years_label", "string", "Year-group label, e.g. 'Years 12+'."),
    ("cards[].price_label", "string", "Price label, e.g. 'Free'."),
    ("cards[].button_url", "string (URL)", "Card-level URL."),
]
EVT_MISSED = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Section description."),
    ("card_button_text", "string", "Shared button text used on every card."),
    ("cards[].position", "integer", "1-based position."),
    ("cards[].video", "string|null", "Recap video URL."),
    ("cards[].title", "string", "Recap title."),
    ("cards[].date_label", "string", "Date label, e.g. 'AUG 2025'."),
    ("cards[].button_url", "string (URL)", "Card-level URL."),
]
EVT_SUBMIT = EMP_EVENTS[:5]  # same shape as Employers Events without the image array

# Insight
INS_HERO = [
    ("label", "string", "Small label."),
    ("title", "string", "Hero title."),
    ("description", "string", "Hero description."),
    ("search_placeholder", "string", "Placeholder for the article search box."),
]
INS_FOUNDER = [
    ("label_1", "string", "First label."),
    ("label_2", "string", "Second label."),
    ("date_label", "string", "Date line."),
    ("title", "string", "Article title."),
    ("description", "string", "Article excerpt."),
    ("meta_data", "string", "Byline / read-time line."),
    ("button.text", "string", "CTA text."),
    ("button.url", "string", "CTA URL."),
    ("categories[].position", "integer", "1-based position."),
    ("categories[].name", "string", "Category name."),
    ("images[]", "string (URL)[]", "Section images."),
]
INS_ARTICLE = [
    ("title", "string", "Section title."),
    ("card_button_text", "string", "Shared card-button label."),
    ("cards[].position", "integer", "1-based position."),
    ("cards[].label", "string", "Card label."),
    ("cards[].image", "string|null", "Card image URL."),
    ("cards[].date_label", "string", "Date label."),
    ("cards[].title", "string", "Article title."),
    ("cards[].description", "string", "Article excerpt."),
    ("cards[].tag", "string", "Tag/category."),
    ("cards[].button_url", "string (URL)", "Card-level URL."),
]
INS_LANE = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("lanes[].position", "integer", "1-based position."),
    ("lanes[].name", "string", "Lane name."),
    ("lanes[].article_count", "integer", "Number of articles."),
    ("lanes[].url", "string (URL)", "Lane URL."),
]
INS_SUBSCRIBE = [
    ("label", "string", "Small label."),
    ("title", "string", "Section title."),
    ("description", "string", "Section description."),
    ("email_placeholder", "string", "Email input placeholder."),
    ("button.text", "string", "Subscribe button text."),
    ("button.url", "string", "Subscribe button URL."),
    ("bottom_note", "string", "Small note under the form."),
    ("images[]", "string (URL)[]", "Section images."),
]


# Map URL → field list
PAYLOAD_BY_URL = {
    "/api/home/header/":         HEADER_FIELDS,
    "/api/home/footer/":         FOOTER_FIELDS,
    "/api/home/hero/":           HERO_FIELDS,
    "/api/home/features/":       FEATURE_FIELDS,
    "/api/home/about/":          ABOUT_HOME_FIELDS,
    "/api/home/network/":        NETWORK_FIELDS,
    "/api/home/talent-pool/":    TALENT_FIELDS,
    "/api/home/apply/":          APPLY_FIELDS,
    "/api/home/social-media/":   SOCIAL_HOME_FIELDS,
    "/api/home/testimonials/":   TESTIMONIALS_FIELDS,
    "/api/home/app/":            APP_FIELDS,

    "/api/about-us/hero/":           ABOUTUS_HERO,
    "/api/about-us/mission/":        ABOUTUS_MISSION,
    "/api/about-us/founder/":        ABOUTUS_FOUNDER,
    "/api/about-us/values/":         ABOUTUS_VALUES,
    "/api/about-us/journey/":        ABOUTUS_JOURNEY,
    "/api/about-us/pledge/":         ABOUTUS_PLEDGE,
    "/api/about-us/team/":           ABOUTUS_TEAM,
    "/api/about-us/community/":      ABOUTUS_COMMUNITY,
    "/api/about-us/social-media/":   ABOUTUS_SOCIAL,

    "/api/schools/hero/":      SCHOOLS_HERO,
    "/api/schools/help/":      SCHOOLS_HELP,
    "/api/schools/employer/":  SCHOOLS_EMPLOYER,
    "/api/schools/benchmark/": SCHOOLS_BENCHMARK,
    "/api/schools/subscribe/": SCHOOLS_SUBSCRIBE,
    "/api/schools/faq/":       SCHOOLS_FAQ,

    "/api/employers/hero/":    EMP_HERO,
    "/api/employers/network/": NETWORK_FIELDS,
    "/api/employers/mission/": EMP_MISSION,
    "/api/employers/offer/":   EMP_OFFER,
    "/api/employers/events/":  EMP_EVENTS,

    "/api/partners/hero/":     PRT_HERO,
    "/api/partners/partner/":  PRT_PARTNER,
    "/api/partners/family/":   PRT_FAMILY,
    "/api/partners/review/":   PRT_REVIEW,
    "/api/partners/founder/":  PRT_FOUNDER,

    "/api/events/hero/":      EVT_HERO,
    "/api/events/featured/":  EVT_FEATURED,
    "/api/events/upcoming/":  EVT_UPCOMING,
    "/api/events/missed/":    EVT_MISSED,
    "/api/events/submit/":    EVT_SUBMIT,

    "/api/insight/hero/":      INS_HERO,
    "/api/insight/founder/":   INS_FOUNDER,
    "/api/insight/article/":   INS_ARTICLE,
    "/api/insight/lane/":      INS_LANE,
    "/api/insight/subscribe/": INS_SUBSCRIBE,
}

# For the combined "Page payload" endpoints, document the top-level keys so
# users can drill into the per-section row above for full detail.
PAGE_PAYLOAD_KEYS = {
    "/api/home/": [
        ("header",       "object", "See /api/home/header/."),
        ("hero",         "object", "See /api/home/hero/."),
        ("features",     "object", "See /api/home/features/."),
        ("about",        "object", "See /api/home/about/."),
        ("network",      "object", "See /api/home/network/."),
        ("talent_pool",  "object", "See /api/home/talent-pool/."),
        ("apply",        "object", "See /api/home/apply/."),
        ("social_media", "object", "See /api/home/social-media/."),
        ("testimonials", "object", "See /api/home/testimonials/."),
        ("app",          "object", "See /api/home/app/."),
        ("footer",       "object", "See /api/home/footer/."),
    ],
    "/api/about-us/": [
        ("hero",         "object", "See /api/about-us/hero/."),
        ("mission",      "object", "See /api/about-us/mission/."),
        ("founder",      "object", "See /api/about-us/founder/."),
        ("values",       "object", "See /api/about-us/values/."),
        ("journey",      "object", "See /api/about-us/journey/."),
        ("pledge",       "object", "See /api/about-us/pledge/."),
        ("team",         "object", "See /api/about-us/team/."),
        ("community",    "object", "See /api/about-us/community/."),
        ("social_media", "object", "See /api/about-us/social-media/."),
    ],
    "/api/schools/": [
        ("hero",       "object", "See /api/schools/hero/."),
        ("help",       "object", "See /api/schools/help/."),
        ("employer",   "object", "See /api/schools/employer/."),
        ("benchmark",  "object", "See /api/schools/benchmark/."),
        ("subscribe",  "object", "See /api/schools/subscribe/."),
        ("faq",        "object", "See /api/schools/faq/."),
    ],
    "/api/employers/": [
        ("hero",     "object", "See /api/employers/hero/."),
        ("network",  "object", "See /api/employers/network/."),
        ("mission",  "object", "See /api/employers/mission/."),
        ("offer",    "object", "See /api/employers/offer/."),
        ("events",   "object", "See /api/employers/events/."),
    ],
    "/api/partners/": [
        ("hero",     "object", "See /api/partners/hero/."),
        ("partner",  "object", "See /api/partners/partner/."),
        ("family",   "object", "See /api/partners/family/."),
        ("review",   "object", "See /api/partners/review/."),
        ("founder",  "object", "See /api/partners/founder/."),
    ],
    "/api/events/": [
        ("hero",     "object", "See /api/events/hero/."),
        ("featured", "object", "See /api/events/featured/."),
        ("upcoming", "object", "See /api/events/upcoming/."),
        ("missed",   "object", "See /api/events/missed/."),
        ("submit",   "object", "See /api/events/submit/."),
    ],
    "/api/insight/": [
        ("hero",      "object", "See /api/insight/hero/."),
        ("founder",   "object", "See /api/insight/founder/."),
        ("article",   "object", "See /api/insight/article/."),
        ("lane",      "object", "See /api/insight/lane/."),
        ("subscribe", "object", "See /api/insight/subscribe/."),
    ],
}


# --------------------------------------------------------------------------
# Write the CSVs
# --------------------------------------------------------------------------
def write_endpoints(path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fp:
        w = csv.writer(fp)
        w.writerow(["#", "Page", "Section", "Method", "URL", "Auth", "Request Payload", "Description"])
        for i, (page, section, method, url, auth, desc) in enumerate(ENDPOINTS, start=1):
            w.writerow([i, page, section, method, url, auth, "(none — GET only)", desc])


def write_payload(path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fp:
        w = csv.writer(fp)
        w.writerow(["Page", "Endpoint", "Field", "Type", "Description"])
        # Page-payload composite endpoints first
        for page, _section, _method, url, _auth, _desc in ENDPOINTS:
            if url in PAGE_PAYLOAD_KEYS:
                for field, ftype, note in PAGE_PAYLOAD_KEYS[url]:
                    w.writerow([page, url, field, ftype, note])
        # Per-section endpoints
        for page, _section, _method, url, _auth, _desc in ENDPOINTS:
            if url in PAYLOAD_BY_URL:
                for field, ftype, note in PAYLOAD_BY_URL[url]:
                    w.writerow([page, url, field, ftype, note])


if __name__ == "__main__":
    endpoints_csv = os.path.join(OUT_DIR, "api_endpoints.csv")
    payload_csv = os.path.join(OUT_DIR, "api_payload.csv")
    write_endpoints(endpoints_csv)
    write_payload(payload_csv)
    print("Wrote:")
    print(" ", endpoints_csv)
    print(" ", payload_csv)
