from django.contrib import admin
from .models import Department,Book,BorrowedBook,Student,Fine
from django.utils.html import format_html
from django.utils import timezone

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['DepartmentName','User']
    search_fields = ['DepartmentName']
    
    

admin.site.register(Department,DepartmentAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ['image_tag','Title','Author','ISBN','User','TotalCopies','AvailableCopies']
    search_fields = ['Title','Author']
    list_filter = ['Department']
    list_display_links = ['Title']
   
    def image_tag(self,obj):
        if obj.CoverImage:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.CoverImage.url)
        else:
            return 'Not Present'

    readonly_fields = ['image_tag']
     
admin.site.register(Book,BookAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ['User','StudentID','Department','Year']
    search_fields = ['Department','Year']
    list_filter =['Department','Year']

admin.site.register(Student,StudentAdmin)    

class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ['Student', 'Book', 'BorrowDate', 'ReturnDate', 'Actual_return_Date', 'Returned', 'FineAmount']
    list_filter = ['Returned']
    # exclude = ['Actual_return_Date']
    list_editable = ['Returned']


    def has_change_permission(self, request, obj = None):
        if obj is not None and obj.Returned:
            return False
        return super().has_change_permission(request, obj)
    def has_delete_permission(self, request, obj = None):
        if obj is not None and obj.Returned:
            return False
        return super().has_delete_permission(request, obj)
    
    def save_model(self, request, obj, form, change):
        if not change:  
            if obj.Book.AvailableCopies > 0: 
                obj.Book.AvailableCopies -= 1
                obj.Book.save()
            else:
                self.message_user(request, f"Book '{obj.Book.Title}' is not available.", level='ERROR')
                return  
        
        if obj.Returned == False: 
            obj.Book.AvailableCopies += 1
            if  obj.Actual_return_Date > obj.ReturnDate :
                DayDifference = obj.Actual_return_Date - obj.ReturnDate
                FineAmount = 5 * DayDifference.days
                obj.FineAmount = FineAmount 
                fineobj = Fine.objects.create(
                    BorrowedBook = obj,
                    Amount = FineAmount ,
                )
            obj.Book.save()
            self.message_user(request, f"Book '{obj.Book.Title}' marked as returned.")


        elif obj.Returned and obj.Actual_return_Date:
            self.message_user(request, f"Book '{obj.Book.Title}' was already returned.")
        elif not obj.Returned:
            obj.Actual_return_Date = None 
        
        
        
        super().save_model(request, obj, form, change)

admin.site.register(BorrowedBook, BorrowedBookAdmin)

class FineAdmin(admin.ModelAdmin):
    list_display = ['BorrowedBook','Amount','PaymentDate','Paid']
    list_filter = ['Paid']
    def has_change_permission(self, request, obj = None):
        if obj is not None and obj.Paid:
            return False
        return super().has_change_permission(request, obj)
    def has_delete_permission(self, request, obj = None):
        if obj is not None and obj.Paid:
            return False
        return super().has_delete_permission(request, obj)

admin.site.register(Fine,FineAdmin)