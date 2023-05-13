from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from lost_item_report.models import FoundItem


def found_item_claim_view(request, id):
    print("I am in found_item_claim_view")
    found_item_obj = FoundItem.objects.get(pk=id)
    context = {
        "found_item_obj": found_item_obj,
        "create_url": reverse("admin:lost_item_report_userclaimitem_add"),
        "back_url": reverse("admin:lost_item_report_founditem_changelist")
    }
    return render(request, 'admin/my_model_detail.html', context)
