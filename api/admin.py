from django.contrib import admin
from .models import University, Question

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country", "has_custom_questions"]
    search_fields = ["name"]
    list_filter = ["has_custom_questions", "country"]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "is_common", "university"]
    list_filter = ["is_common"]
    search_fields = ["text"]
