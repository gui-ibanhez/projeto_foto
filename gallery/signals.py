from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from wand.image import Image as WandImage
from .models import Photo


MAX_LONG_EDGE = 3840


@receiver(pre_save, sender=Photo)
def process_photo_on_save(sender, instance: Photo, **kwargs):
    if not instance.image:
        return

    instance.image.file.seek(0)
    with WandImage(file=instance.image.file) as img:
        img.auto_orient()
        if max(img.width, img.height) > MAX_LONG_EDGE:
            if img.width >= img.height:
                img.transform(resize=f"{MAX_LONG_EDGE}x")
            else:
                img.transform(resize=f"x{MAX_LONG_EDGE}")
        img.strip()
        img.format = 'jpeg'
        img.compression_quality = 80

        out_io = BytesIO()
        img.save(file=out_io)
        instance.width = img.width
        instance.height = img.height
        instance.format = 'JPEG'
        instance.image.save(instance.image.name, ContentFile(out_io.getvalue()), save=False)

        # Thumbnail
        thumb = img.clone()
        thumb.transform(resize='400x400>')
        thumb.strip()
        thumb.format = 'jpeg'
        thumb_io = BytesIO()
        thumb.save(file=thumb_io)
        instance.thumbnail.save(instance.image.name.replace('/stores/', '/stores/').replace('.jpg', '_thumb.jpg'), ContentFile(thumb_io.getvalue()), save=False)


@receiver(post_delete, sender=Photo)
def delete_files_on_photo_delete(sender, instance: Photo, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)


