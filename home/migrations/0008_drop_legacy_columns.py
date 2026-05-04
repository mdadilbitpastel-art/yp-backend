"""Drop columns that earlier in-place migration edits left orphaned.

`feature_N_is_highlighted` was introduced in 0006 and later removed from the
model; `about_section_order` was introduced in 0007 and later removed. If
those original migrations were applied to the DB before being edited, the
columns still exist physically. This migration drops them defensively using
``DROP COLUMN IF EXISTS`` so it's a no-op on fresh DBs.
"""

from django.db import migrations


SQL_DROP = """
ALTER TABLE home_herosection DROP COLUMN IF EXISTS feature_1_is_highlighted;
ALTER TABLE home_herosection DROP COLUMN IF EXISTS feature_2_is_highlighted;
ALTER TABLE home_herosection DROP COLUMN IF EXISTS feature_3_is_highlighted;
ALTER TABLE home_herosection DROP COLUMN IF EXISTS feature_4_is_highlighted;
ALTER TABLE home_herosection DROP COLUMN IF EXISTS feature_5_is_highlighted;
ALTER TABLE home_herosection DROP COLUMN IF EXISTS about_section_order;
"""


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_about_section"),
    ]

    operations = [
        migrations.RunSQL(SQL_DROP, reverse_sql=migrations.RunSQL.noop),
    ]
