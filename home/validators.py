"""Reusable file/image/video validators."""

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

MAX_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "svg", "gif"}

MAX_VIDEO_SIZE_MB = 100
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "mov", "m4v", "ogg", "ogv"}


def validate_image_size(file):
    if not isinstance(file, UploadedFile):
        return
    if file.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError(
            f"Image too large. Max size is {MAX_IMAGE_SIZE_MB} MB."
        )


def validate_image_extension(file):
    if not isinstance(file, UploadedFile):
        return
    ext = file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file type '.{ext}'. "
            f"Allowed: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}."
        )


def validate_video_size(file):
    if not isinstance(file, UploadedFile):
        return
    if file.size > MAX_VIDEO_SIZE_MB * 1024 * 1024:
        raise ValidationError(
            f"Video too large. Max size is {MAX_VIDEO_SIZE_MB} MB."
        )


def validate_video_extension(file):
    if not isinstance(file, UploadedFile):
        return
    ext = file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        raise ValidationError(
            f"Unsupported video format '.{ext}'. "
            f"Allowed: {', '.join(sorted(ALLOWED_VIDEO_EXTENSIONS))}."
        )
