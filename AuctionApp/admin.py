from django.contrib import admin
from .models import Item, ItemBuyer, PaymentRequestData

from reportlab.pdfgen    import canvas
from reportlab.lib.utils import ImageReader
from datetime            import datetime

from django.http import HttpResponse


admin.site.site_header = "MR GIG ADMIN"
admin.site.site_title = "MR GIG ADMIN"
admin.site.index_title= "Welcome MR GIG ADMIN"


class ItemAdmin(admin.ModelAdmin):
    model: Item
    actions = ['generate_client_report']
    list_display = ("name", "description", "amount", "status")
    list_filter = ("name", "description", "amount", "status")
   
    def generate_client_report(self, request, queryset):
        print(queryset.values())
        #queryset.update(status='REMOVED')
        # Create the HttpResponse object 
        response = HttpResponse(content_type='application/pdf') 

        # This line force a download
        response['Content-Disposition'] = 'attachment; filename="1.pdf"' 
        p = canvas.Canvas(response)
        x = 10
        y = 10

        for q in queryset:
            p.drawString(x, y, f"Name: {q.name}")
            y+=10

        # Close the PDF object. 
        p.showPage() 
        p.save()

        return response
        
    generate_client_report.short_description = "Send Client Report "   


# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemBuyer)
admin.site.register(PaymentRequestData)