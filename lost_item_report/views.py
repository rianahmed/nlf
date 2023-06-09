from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from lost_item_report.models import FoundItem, UserClaimItem, ClaimStatus


def found_item_claim_view(request, id):
    print("I am in found_item_claim_view")
    found_item_obj = FoundItem.objects.get(pk=id)
    context = {
        "found_item_obj": found_item_obj,
        "create_url": reverse("admin:lost_item_report_userclaimitem_add"),
        "back_url": reverse("admin:lost_item_report_founditem_changelist")
    }
    return render(request, 'admin/my_model_detail.html', context)


def update_claim_item_status_view(request, id):
    print("I am in update_claim_item_status_view")
    all_claim_status = ClaimStatus.choices
    claim_item_obj = UserClaimItem.objects.get(pk=id)
    context = {
        "all_claim_status": all_claim_status,
        "claim_item_obj": claim_item_obj,
        "submit_url": reverse("admin:lost_item_report_userclaimitem_add"),
        "back_url": reverse("admin:lost_item_report_founditem_changelist")
    }
    return render(request, 'admin/claim_item_details.html', context)

def hello(request):
    return httpresponse("hello world")