"""Per-resource-type storage selectors.

Cloudinary tracks `image` and `video` assets in separate resource buckets.
The default `MediaCloudinaryStorage` is hard-coded to `resource_type='image'`,
so uploading a video through it (and later deleting it) targets the wrong
bucket. These helpers return the appropriate Cloudinary storage class when
Cloudinary is configured, and fall back to the default storage otherwise.
"""

from django.conf import settings
from django.core.files.storage import default_storage


def _cloudinary_enabled() -> bool:
    return bool(getattr(settings, "CLOUDINARY_CLOUD_NAME", ""))


def video_storage():
    """Return the storage backend used for video FileFields."""
    if _cloudinary_enabled():
        from cloudinary_storage.storage import VideoMediaCloudinaryStorage

        return VideoMediaCloudinaryStorage()
    return default_storage
