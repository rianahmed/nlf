from django.http import Http404
from django.shortcuts import render, redirect

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


def approve_found_item_view(request, id):
    found_item_obj = FoundItem.objects.get(pk=id)
    context = {
        "found_item_obj": found_item_obj,
        "approval_url": reverse("update-founditem-approve-url", args=[found_item_obj.pk]),
        "back_url": reverse("admin:lost_item_report_founditem_changelist")
    }
    return render(request, 'admin/approve_found_item_detail.html', context)


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


def update_found_item_approve_item_view(request, id):
    print("I am in update_found_item_approve_status_view")
    try:
        found_item_obj = FoundItem.objects.get(pk=id)
        found_item_obj.is_admin_approved = True
        found_item_obj.save()
        return redirect('/')
    except Exception as exception:
        raise Http404("FoundItem Not Found")


def hello(request):
    return httpresponse("hello world")
