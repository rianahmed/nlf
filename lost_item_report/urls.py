from django.urls import path

from lost_item_report.views import found_item_claim_view

urlpatterns = [
    path('found-item-claim/<int:id>', found_item_claim_view, name='found-item-claim-url'),
]
