from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.http import HttpRequest
from django.utils.timezone import now
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone


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
        super(FoundItem, self).clean()
        # Get the current user
        user = self.founded_by

        if isinstance(user, AnonymousUser):
            raise ValidationError("No user found.")

        # Check the number of unclaimed items for the user
        max_unclaimed_items = 5  # Set your desired limit
        unclaimed_items_count = FoundItem.objects.filter(founded_by=user, claimed_by__isnull=True).count()

        if not self.pk and unclaimed_items_count >= max_unclaimed_items:
            raise ValueError("Maximum limit reached for unclaimed founditems.")

    def save(self, *args, **kwargs):
        # Only for newly created objects
        if not self.pk:
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
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT, related_name="reported_lost_item_user")
    image = models.ImageField(null=True, blank=True)
    item_category = models.ForeignKey(ItemCategory, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name

    def clean(self):
        super().clean()

        # validation for ReportLostItem user can post only 5 post.
        max_count = 6  # Maximum allowed posts
        time_period_days = 3  # Time period in days
        current_user = self.reported_by
        current_time = timezone.now()

        # Calculate the start time of the time period
        start_time = current_time - timezone.timedelta(days=time_period_days)

        # Count the number of items created by the user within the time period
        current_count = ReportLostItem.objects.filter(
            reported_by=current_user,
            created_at__gte=start_time,
            created_at__lte=current_time
        ).count()

        if not self.pk and current_count >= max_count:
            raise ValueError(f"You have reached the maximum number of posts ({max_count}) within {time_period_days} days.")

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for newly created objects
            self.clean()
            request = kwargs.pop('request', None)  # Retrieve the request object
            if request and isinstance(request, HttpRequest) and request.user.is_authenticated:
                self.reported_by = request.user  # Set the reported_by field to the authenticated user
        super().save(*args, **kwargs)


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

    def clean(self):
        super().clean()

        # validation for ReportLostItem user can post only 5 post.
        max_count = 6  # Maximum allowed posts
        time_period_days = 3  # Time period in days
        current_user = self.claimed_by
        current_time = timezone.now()

        # Calculate the start time of the time period
        start_time = current_time - timezone.timedelta(days=time_period_days)

        # Count the number of items created by the user within the time period
        current_count = UserClaimItem.objects.filter(
            reported_by=current_user,
            created_at__gte=start_time,
            created_at__lte=current_time
        ).count()

        if not self.pk and current_count >= max_count:
            raise ValueError(f"You have reached the maximum number of ({max_count}) claims within {time_period_days} days.")

    def save(self, *args, **kwargs):
        # Only for newly created objects
        if not self.pk:
            self.clean()
            request = kwargs.pop('request', None)  # Retrieve the request object
            if request and isinstance(request, HttpRequest) and request.user.is_authenticated:
                self.claimed_by = request.user  # Set the claimed_by field to the authenticated user
        super().save(*args, **kwargs)
