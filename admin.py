from django.contrib import admin
from accounts.models import *
from simple_history.admin import SimpleHistoryAdmin


class TaskAdmin(admin.ModelAdmin):
	list_display = ['title', 'content', 'deadline', 'status', 'public', 'created_to', 'update_to', 'history']

admin.site.register(Task , TaskAdmin)

