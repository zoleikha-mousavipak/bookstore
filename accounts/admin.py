from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class ShopUserAdmin(UserAdmin):
    add_form = ShopUserChangeForm
    form = ShopUserChangeForm
    model = ShopUser
    list_display = ['username', 'email', 'phone', 'city']


admin.site.register(ShopUser, ShopUserAdmin)
