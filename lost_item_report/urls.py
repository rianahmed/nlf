from django.urls import path

from lost_item_report.views import found_item_claim_view, update_claim_item_status_view, add_post

urlpatterns = [
    path('found-item-claim/<int:id>', found_item_claim_view, name='found-item-claim-url'),
    path('claim-item-status/<int:id>', update_claim_item_status_view, name='claim-item-status-url'),

    #checking for found item count
    path('count/', add_post, name='count'),

]
