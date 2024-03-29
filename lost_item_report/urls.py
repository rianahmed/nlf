from django.urls import path

from lost_item_report.views import (
    found_item_claim_view,
    update_claim_item_status_view,
    approve_found_item_view,
    update_found_item_approve_item_view,
)

urlpatterns = [
    path('found-item-claim/<int:id>', found_item_claim_view, name='found-item-claim-url'),
    path('approve-found-item/<int:id>', approve_found_item_view, name='approve-found-item-url'),
    path('claim-item-status/<int:id>', update_claim_item_status_view, name='claim-item-status-url'),
    path('update-founditem-approve-status/<int:id>', update_found_item_approve_item_view, name='update-founditem-approve-url'),
]
