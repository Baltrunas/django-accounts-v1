# -*- coding: utf-8 -*-
from accounts.models import User
from billboard.models import Ad

def vars(request):
    return {
        'user_count': User.objects.all().count(),
        'ad_count': Ad.objects.filter(public=True, deleted=False).count(),
    }