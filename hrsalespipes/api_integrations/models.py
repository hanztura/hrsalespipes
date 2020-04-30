from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from django_extensions.db.models import TimeStampedModel


# Create your models here.
class LinkedinApi(TimeStampedModel):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    profile_url = models.URLField(blank=True)
    code = models.TextField(blank=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    state_is_used = models.BooleanField(default=False, blank=True)
    access_token = models.TextField(blank=True)
    expires_in = models.PositiveIntegerField(blank=True, null=True)
    error = models.TextField(blank=True)
    error_description = models.TextField(blank=True)

    def __str__(self):
        return self.user_id

    @property
    def expired(self):
        if not self.expires_in:
            return True

        now = timezone.localtime()
        seconds_passed = (now - self.created).seconds
        has_expired = self.expires_in <= seconds_passed
        return True if has_expired else False


class CreateLinkedinProfile(TimeStampedModel):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    target_url = models.URLField()
