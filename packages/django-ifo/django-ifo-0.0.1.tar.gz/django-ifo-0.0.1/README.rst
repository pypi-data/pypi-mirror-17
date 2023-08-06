=========================
Inline and Fieldset Order
=========================


This app allows you to specify the ordering of inlines and fieldsets
in Django Admin.

Quick start
-----------

1. Add "django_ifo" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        'django_ifo', # must be before admin

        'django.contrib.admin',
        ...
    ]

2. Add fieldsets_and_inlines_order field in UserAdmin::

    # employee/admin.py

    class MyUserAdmin(UserAdmin):
        fieldsets_and_inlines_order = ('f', 'i') # 1 fieldset then 1 inline

        def add_view(self, *args, **kwargs):
            self.inlines = []
            return super(UserAdmin, self).add_view(*args, **kwargs)

        def change_view(self, *args, **kwargs):
            self.inlines = [EmployeeInline]
            return super(UserAdmin, self).change_view(*args, **kwargs)

    admin.site.unregister(User)
    admin.site.register(User, MyUserAdmin)
