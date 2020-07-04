from django.contrib import admin

# Register your models here.
from .models import Name, MidName

admin.site.register(Name)


class MidNameAdmin(admin.ModelAdmin):
    list_display = ['__id__','__str__','__meaning__', '__gender__']
    class Meta:
        model = MidName

admin.site.register(MidName, MidNameAdmin)