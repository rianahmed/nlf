from django.shortcuts import render
# Create your views here.
from django.urls import reverse

from lost_item_report.models import FoundItem, UserClaimItem, ClaimStatus
from django.contrib.auth.models import User, Permission


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


#checking for found item count
def add_post(request):
    count = FoundItem.objects.count()
    if count<=5:
      user = User.objects.get(username='rian')
      permission=Permission.objects.get(codename='lost_item_report | found item | Can add found item')
      user.user_permissions.remove(permission)
      return render(request, 'admin/text.html', {'permission': permission})
    else:
        user = User.objects.get(username='rian')

        return render(request, 'admin/text.html', {'permission': user})