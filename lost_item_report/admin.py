from django.contrib import admin
from django.urls import reverse, path
from django.utils.html import format_html

from lost_item_report.models import (
    ItemCategory,
    FoundItem,
    ReportLostItem,
    UserClaimItem,
)
from django.contrib.auth.models import Permission

from lost_item_report.views import found_item_claim_view

admin.site.register(Permission)
admin.site.register(ItemCategory)
admin.site.register(ReportLostItem)
admin.site.register(UserClaimItem)


@admin.action(description='User Claim Request Tracker')
def insert_user_claim_item(modeladmin, request, queryset):
    print(modeladmin, request, queryset)
    user_claim_item_obj = UserClaimItem()
    user_claim_item_obj.found_item = 1  # TODO: Found Item ID Here
    user_claim_item_obj.claimed_by = 1  # TODO: User ID Here
    user_claim_item_obj.save()


class FoundItemAdmin(admin.ModelAdmin):
    def image_viewer_function(self, single_db_obj):
        return format_html(f'<img src="{single_db_obj.image}" width="auto" height="200px" />')

    image_viewer_function.short_description = 'Image'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('found-item-claim/<int:id>', found_item_claim_view, name='found-item-claim-url'),
        ]
        return custom_urls + urls

    def custom_claim_button_field(self, obj):
        return format_html(
            '<a class="button button-danger" href="{}">Claim</a>',
            reverse('found-item-claim-url', args=[obj.pk]),
        )

    custom_claim_button_field.short_description = "Claim Item"
    custom_claim_button_field.allow_tags = True

    list_display = ['name', 'description', 'image_viewer_function', 'location', 'founded_by',
                    'item_category', 'custom_claim_button_field']
    search_fields = ['name', 'description']

    actions = [insert_user_claim_item]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.list_display
        else:
            return [field for field in self.list_display if field != 'founded_by']

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return super().get_fieldsets(request, obj)
        if obj.post_anonymous:
            return (
                (None, {'fields': (
                    'name', 'description', 'image', 'location', 'time', 'item_category', 'claimed_by',
                    'found_by_name_or_anonymous', 'claimed_date',
                    'post_anonymous')}),
            )
        else:
            return (
                (None, {'fields': (
                    'name', 'description', 'image', 'location', 'time', 'item_category', 'founded_by',
                    'claimed_by', 'claimed_date', 'post_anonymous')}),
            )

    def found_by_name_or_anonymous(self, obj):
        if obj.post_anonymous:
            return "Anonymous User"
        else:
            return obj.founded_by.username

    found_by_name_or_anonymous.short_description = 'Found By'

admin.site.register(FoundItem, FoundItemAdmin)
