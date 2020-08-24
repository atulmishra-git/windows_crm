from django.contrib import admin
from mainapp.models import User, Customer, PurchaseRecord, CallNotes, Tasks, AttachmentTemplate, Pdf

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(PurchaseRecord)
admin.site.register(CallNotes)
admin.site.register(Tasks)
admin.site.register(AttachmentTemplate)
admin.site.register(Pdf)
