from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from PIL import Image, ExifTags
from .models import Photo


MAX_LONG_EDGE = 3840
THUMB_MAX_EDGE = 400


def _fix_orientation(img: Image.Image) -> Image.Image:
    try:
        exif = img.getexif()
        orientation_key = None
        for k, v in ExifTags.TAGS.items():
            if v == 'Orientation':
                orientation_key = k
                break

        if exif and orientation_key and orientation_key in exif:
            orientation = exif[orientation_key]
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # Cases: image doesn't have getexif or getexif throws error
        pass
    return img


@receiver(pre_save, sender=Photo)
def process_photo_on_save(sender, instance: Photo, **kwargs):
    if not instance.image:
        return

    instance.image.file.seek(0)
    with Image.open(instance.image.file) as img:
        img = _fix_orientation(img)

        # Resize main image if too large
        if max(img.width, img.height) > MAX_LONG_EDGE:
            img.thumbnail((MAX_LONG_EDGE, MAX_LONG_EDGE))

        # Save main image
        out_io = BytesIO()
        # Convert to RGB to ensure JPEG compatibility
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(out_io, format='JPEG', quality=80, optimize=True)
        instance.width = img.width
        instance.height = img.height
        instance.format = 'JPEG'
        instance.image.save(instance.image.name, ContentFile(out_io.getvalue()), save=False)

        # Create and save thumbnail
        img.thumbnail((THUMB_MAX_EDGE, THUMB_MAX_EDGE))
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=75, optimize=True)
        instance.thumbnail.save(instance.image.name.replace('.jpg', '_thumb.jpg'), ContentFile(thumb_io.getvalue()), save=False)


@receiver(post_delete, sender=Photo)
def delete_files_on_photo_delete(sender, instance: Photo, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)


