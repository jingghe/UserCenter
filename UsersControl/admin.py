from django.contrib import admin

# Register your models here.

from UsersControl.models import UserProfile,Department,Permission


admin.site.register(UserProfile)
admin.site.register(Department)
# admin.site.register(APPAdmin)
# admin.site.register(RoleList)
admin.site.register(Permission)