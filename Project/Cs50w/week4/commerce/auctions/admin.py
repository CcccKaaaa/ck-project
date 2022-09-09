from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Bids)
admin.site.register(Auctions)
admin.site.register(Comments)
admin.site.register(WatchList)
