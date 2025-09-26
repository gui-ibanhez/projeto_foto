from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from gallery.models import Store, StoreSection, Photo


class Command(BaseCommand):
    help = "Create 'Manager' group with CRUD permissions for Store, StoreSection, and Photo."

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name='Manager')
        models = [Store, StoreSection, Photo]
        perms = []
        for model in models:
            ct = ContentType.objects.get_for_model(model)
            perms.extend(Permission.objects.filter(content_type=ct))
        group.permissions.set(perms)
        self.stdout.write(self.style.SUCCESS("Manager group ensured with model permissions."))


