from django.core.management.base import BaseCommand
from nid_validator.models import APIKey


# Should run at the start of each month to reset API key quotas
class Command(BaseCommand):
    help = "Reset API key quotas if a new month has started"

    def handle(self, *args, **options):
        for key in APIKey.objects.all():
            key.refresh_quota_if_needed()
        self.stdout.write(self.style.SUCCESS("Quotas refreshed"))
