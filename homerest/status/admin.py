from django.contrib import admin

from .models import Status
from .forms import StatusForm


# ensure that valid data is entered fro the admin's dashboard form
class StatusAdmin(admin.ModelAdmin):
    # actual model field to display
    list_display = ['user', 'context', 'image']
    form = StatusForm

admin.site.register(Status,StatusAdmin)

