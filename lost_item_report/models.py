from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.middleware import get_user


# lost item names
class ItemCategory(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


# Lost item found by users
class FoundItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    location = models.CharField(max_length=255)
    time = models.DateTimeField()
    item_category = models.ForeignKey(ItemCategory, on_delete=models.RESTRICT)
    founded_by = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT, related_name="founded_item_user")
    claimed_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="claimed_user")
    claimed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    post_anonymous = models.BooleanField(default=False)
    is_admin_approved = models.BooleanField(default=False, help_text="Only This field value true Found Item will be shown on frontend list")

    def clean(self):
        # Get the current user
        user = get_user(self._state.db)

        if isinstance(user, AnonymousUser):
            raise ValidationError("No user found.")

        # Check the number of unclaimed items for the user
        max_unclaimed_items = 5  # Set your desired limit
        unclaimed_items_count = FoundItem.objects.filter(founded_by=user, claimed_by__isnull=True).count()

        if unclaimed_items_count >= max_unclaimed_items:
            raise ValidationError("Maximum limit reached for unclaimed items.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# A user giving ad for the item he has lost
class ReportLostItem(models.Model):
    item_name = models.CharField(max_length=100)
    model_version = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    date_lost = models.DateTimeField()
    reporter_name = models.CharField(max_length=255)
    reporter_phone = models.CharField(max_length=20)
    image = models.ImageField(null=True, blank=True)
    item_category = models.ForeignKey(ItemCategory, on_delete=models.RESTRICT)

    def __str__(self):
        return self.item_name


class ClaimStatus(models.TextChoices):
    PROCESSING = "processing", "Processing State"
    IN_REVIEW = "in_review", "Under Review"
    APPROVED = "approved", "Approved"


class UserClaimItem(models.Model):
    found_item = models.ForeignKey(FoundItem, on_delete=models.RESTRICT)
    claimed_by = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT, related_name="claimed_by_user")
    description = models.TextField()
    attachment = models.ImageField()
    status = models.CharField(max_length=20, choices=ClaimStatus.choices, default=ClaimStatus.PROCESSING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
