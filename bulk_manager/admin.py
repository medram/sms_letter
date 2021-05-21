from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from background_task.models import Task, CompletedTask

from .models import Campaign

# unregister Background_task app
admin.site.unregister(Task)
admin.site.unregister(CompletedTask)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'run_at',
                           'repeat', 'repeat_until', 'contact_lists', 'messages')}),
        (_('Access Info'), {
         'fields': ('created_by_profile_large', 'created', 'updated')})
    )
    list_display = ('id', 'title', 'total_messages', 'total_contacts',
                    'created_by_profile', 'created')
    list_display_links = ('id', 'title')
    filter_horizontal = ('contact_lists', 'messages')
    readonly_fields = ('updated', 'created', 'updated_by',
                       'created_by', 'updated_by_profile', 'created_by_profile', 'created_by_profile_large')
    list_filter = ('created', 'created_by')
    search_fields = ('id', 'title')
    date_hierarchy = 'created'
    radio_fields = {'repeat': admin.VERTICAL}

    def total_messages(self, obj=None):
        return obj.messages.count()

    def total_contacts(self, obj=None):
        return sum([l.contacts.count() for l in obj.contact_lists.all()])
