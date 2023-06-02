from django.contrib import admin
from django.contrib import auth

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import mark_safe
from social.models import *


class UserAdmin(BaseUserAdmin):
    list_display = ('id','email', 'username',)
    search_fields = ('email', 'username',)

    # fieldsets = BaseUserAdmin.fieldsets
    # fieldsets[0][1]['fields'] = fieldsets[0][1]['fields'] + (
    #     'Money','Total_recharge_money','Total_amount_deducted','Avatar','OTP','Two_factor_authentication'
    # )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email','username', 'password1', 'password2','Avatar')}
    #     ),
    # )
admin.site.register(User,UserAdmin)
admin.site.unregister(auth.models.Group)

class Data_zip_exel_Admin(admin.ModelAdmin):
    list_display = ('id','zip_file','image_file')
    search_fields = ('zip_file','image_file',)

admin.site.register(Data_zip_exel,Data_zip_exel_Admin)