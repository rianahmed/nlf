from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from django.http import HttpResponseBadRequest


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
    #added for Post Limit
    post_limit=models.IntegerField(default=1)

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
    class Meta:
        verbose_name='My Claim Item'

