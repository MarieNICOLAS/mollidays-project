from django.contrib import admin
from circuits.models.circuit import Circuit
from circuits.models.category import Category
from circuits.models.tag import Tag
from circuits.models.step import Step

@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ("title", "destination", "start_date", "end_date", "price", "available_seats", "status")
    list_filter = ("status", "start_date", "category")
    search_fields = ("title", "destination", "description")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("title", "circuit", "order", "duration_hours")
    list_filter = ("circuit",)
    search_fields = ("title", "description")
