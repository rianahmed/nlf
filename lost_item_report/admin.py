from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.urls import reverse, path
from django.utils.html import format_html

from lost_item_report.models import (
    ItemCategory,
    FoundItem,
    ReportLostItem,
    UserClaimItem,
)
from django.contrib.auth.models import Permission

from lost_item_report.views import (
    found_item_claim_view,
    update_claim_item_status_view,
    approve_found_item_view,
    update_found_item_approve_item_view,
)

admin.site.register(Permission)
admin.site.register(ItemCategory)

@admin.action(description='User Claim Request Tracker')
def insert_user_claim_item(modeladmin, request, queryset):
    print(modeladmin, request, queryset)
    user_claim_item_obj = UserClaimItem()
    user_claim_item_obj.found_item = 1  # TODO: Found Item ID Here
    user_claim_item_obj.claimed_by = request.user  # TODO: User ID Here
    user_claim_item_obj.save()


class ReportLostItemAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            form.add_error(None, e)
            messages.error(request, str(e))
            return

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}

        if request.method == 'POST':
            try:
                response = super().changeform_view(request, object_id, form_url, extra_context)
            except Exception as e:
                extra_context['validation_error'] = str(e)
        else:
            response = super().changeform_view(request, object_id, form_url, extra_context)

        if 'validation_error' in extra_context:
            extra_context['errors'] = [extra_context['validation_error']]

        return response


class FoundItemAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(is_admin_approved=True)
        return qs

    def image_viewer_function(self, single_db_obj):
        return format_html(f'<img src="{single_db_obj.image}" width="auto" height="200px" />')

    image_viewer_function.short_description = 'Image'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('found-item-claim/<int:id>', found_item_claim_view, name='found-item-claim-url'),
            path('approve-found-item/<int:id>', approve_found_item_view, name='approve-found-item-url'),
            path('update-founditem-approve-status/<int:id>', update_found_item_approve_item_view,
                 name='update-founditem-approve-url'),
        ]
        return custom_urls + urls

    def get_form(self, request, obj=None, **kwargs):
        self.request = request  # Store the request object
        return super().get_form(request, obj, **kwargs)

    def custom_claim_button_field(self, obj):
        if obj.is_admin_approved:
            return format_html(
                '<a class="btn btn-info" href="{}">Claim</a>',
                reverse('found-item-claim-url', args=[obj.pk]),
            )
        return format_html(
            '<button type="button" disabled>Not Approved</button>'
        )

    custom_claim_button_field.short_description = "Claim Item"
    custom_claim_button_field.allow_tags = True

    def custom_approve_button(self, obj):
        if not obj.is_admin_approved and self.request.user.is_superuser:
            return format_html(
                '<a class="btn btn-success" href="{}">Approve</a>',
                reverse('approve-found-item-url', args=[obj.pk]),
            )

    custom_approve_button.short_description = "Approve Found Item"
    custom_approve_button.allow_tags = True

    list_display = ['name', 'description', 'image_viewer_function', 'location', 'founded_by',
                    'item_category', 'custom_claim_button_field', 'custom_approve_button']
    search_fields = ['name', 'description']

    actions = [insert_user_claim_item]

    def get_list_display(self, request):
        self.request = request
        if request.user.is_superuser:
            return self.list_display
        else:
            user_excluded_list = ['founded_by', 'custom_approve_button']
            return [field for field in self.list_display if field not in user_excluded_list]

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return super().get_fieldsets(request, obj)
        if obj.post_anonymous:
            return (
                (None, {'fields': (
                    'name', 'description', 'image', 'location', 'time', 'item_category', 'claimed_by',
                    'found_by_name_anonymous', 'claimed_date',
                    'post_anonymous')}),
            )
        else:
            return (
                (None, {'fields': (
                    'name', 'description', 'image', 'location', 'time', 'item_category', 'founded_by',
                    'claimed_by', 'claimed_date', 'post_anonymous')}),
            )

    def found_by_name_anonymous(self, obj):
        if obj.post_anonymous:
            return "Anonymous User"
        else:
            return obj.founded_by.username

    found_by_name_anonymous.short_description = 'Found By'


class UserClaimItemAdmin(admin.ModelAdmin):
    list_display = ['found_item', 'description', 'status']
    search_fields = ['status', 'description']
    custom_approve_button_field_added = False

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if request.user.is_superuser and not self.custom_approve_button_field_added:
            list_display.append('custom_approve_button_field')
            self.custom_approve_button_field_added = True
        return list_display

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)
        if not request.user.is_superuser:
            fields = [field for field in fields if field != 'status']
        return fields

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('claim-item-status/<int:id>', update_claim_item_status_view, name='claim-item-status-url'),
        ]
        return custom_urls + urls

    def custom_approve_button_field(self, obj):
        return format_html(
            '<a class="btn btn-warning" href="{}">Update Status</a>',
            reverse('claim-item-status-url', args=[obj.pk]),
        )

    custom_approve_button_field.short_description = "Status"
    custom_approve_button_field.allow_tags = True

    def save_model(self, request, obj, form, change):
        self.request = request
        try:
            obj.full_clean()  # Run model validation
            obj.save()
        except ValidationError as e:
            form.add_error(None, e)
            messages.error(request, str(e))
            return


admin.site.register(UserClaimItem, UserClaimItemAdmin)
admin.site.register(FoundItem, FoundItemAdmin)
admin.site.register(ReportLostItem, ReportLostItemAdmin)
