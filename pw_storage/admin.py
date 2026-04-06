from django.contrib import admin
from .models import Password
# Register your models here.
admin.site.register(Password)



from .models import Notification

admin.site.register(Notification)
