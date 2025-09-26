from django.db import models
from django.contrib.auth import get_user_model
import uuid
from .validators import BR_STATE_CHOICES, validate_state_code


User = get_user_model()


class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=2, blank=True, choices=BR_STATE_CHOICES, validators=[validate_state_code])
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.strip().upper()
        if self.state:
            self.state = self.state.strip().upper()
        super().save(*args, **kwargs)


class StoreSection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_store_sections")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_store_sections")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("store", "name")
        ordering = ["store__code", "name"]

    def __str__(self) -> str:
        return f"{self.store.code} / {self.name}"


def store_photo_upload_path(instance: "Photo", filename: str) -> str:
    from uuid import uuid4
    from datetime import datetime
    ext = "jpg"
    now = datetime.now()
    return f"stores/{instance.store.code}/{now.strftime('%Y/%m')}/{uuid4()}.{ext}"


def store_thumb_upload_path(instance: "Photo", filename: str) -> str:
    from uuid import uuid4
    from datetime import datetime
    ext = "jpg"
    now = datetime.now()
    return f"stores/{instance.store.code}/{now.strftime('%Y/%m')}/thumbs/{uuid4()}.{ext}"


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="photos")
    section = models.ForeignKey(StoreSection, on_delete=models.PROTECT, related_name="photos")
    image = models.ImageField(upload_to=store_photo_upload_path)
    thumbnail = models.ImageField(upload_to=store_thumb_upload_path, blank=True)
    description = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="uploaded_photos")
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    format = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.store.code} / {self.section.name} ({self.created_at:%Y-%m-%d})"

# Create your models here.
