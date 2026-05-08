from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Room, Allocation, WaitlistEntry,Fee

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_number', 'gender', 'course', 'year', 'contact']
    search_fields = ['name', 'roll_number']
    list_filter = ['gender', 'course']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'block', 'gender_type', 'capacity']
    search_fields = ['room_number', 'block']
    list_filter = ['block', 'gender_type']

@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ['student', 'room', 'allocated_date', 'status']
    search_fields = ['student__name', 'room__room_number']
    list_filter = ['status']

@admin.register(WaitlistEntry)
class WaitlistAdmin(admin.ModelAdmin):
    list_display = ['student', 'requested_date']
    search_fields = ['student__name']

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'description', 'amount', 'due_date', 'status']
    search_fields = ['student__name']
    list_filter = ['status']