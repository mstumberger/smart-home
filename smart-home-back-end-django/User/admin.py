
from django.contrib.auth import admin as authadmin
from django.contrib.auth.models import Group
from User.models import User
from django.contrib import admin

# Register your models here.


class UserAdmin(authadmin.UserAdmin):
    list_display = ('id', 'username', 'role')
    list_filter = ()
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('username', 'password', 'name', 'surname', 'role')}),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
