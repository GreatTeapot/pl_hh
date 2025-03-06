# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.utils.translation import gettext_lazy as _
#
# from .models.users import User
#
#
# # region -------------------------- MODEL ADMIN -------------------------------------
# @admin.register(User)
# class UserAdmin(UserAdmin):
#     """
#     User admin model.
#
#     Attributes:
#         * `change_user_password_template` (None): change user password template.
#         * `fieldsets` (tuple[tuple[...]]): field groups.
#         * `add_fieldsets` (tuple[tuple[...]]): add field groups.
#         * `list_display` (tuple[str]): list display.
#         * `list_filter` (tuple[str]): list filter.
#         * `search_fields` (tuple[str]): search fields.
#         * `filter_horizontal` (tuple[str]): horizontal filter.
#         * `readonly_fields` (tuple[str]): read-only fields.
#         * `inlines` (tuple[ProfileAdmin]): inlines.
#     """
#     # region -------------- ADMIN PANEL FOR ADMIN USER ---------------------
#     change_user_password_template = None
#     fieldsets = (
#         (None,
#          {'fields': ('phone_number', 'email', 'username')}),
#         (_('Personal information'),
#          {'fields': ('first_name', 'last_name',)}),
#         (_('Permissions'), {
#             'fields': ('is_active',  'is_superuser',
#                        'groups', 'user_permissions',)
#         }),
#         (_('Important dates'), {'fields': ('last_login',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'phone_number', 'password1', 'password2',),
#         }),
#     )
#     list_display = ('id', 'full_name', 'email', 'phone_number',)
#
#     list_display_links = ('id', 'full_name',)
#     list_filter = ('is_superuser', 'is_active', 'groups')
#     search_fields = ('first_name', 'last_name', 'id', 'email', 'phone_number',)
#     ordering = ('-id',)
#     filter_horizontal = ('groups', 'user_permissions',)
#     readonly_fields = ('last_login',)
#
#     # endregion ---------------------------------------------------------------------
# # endregion -------------------------------------------------------------------------
