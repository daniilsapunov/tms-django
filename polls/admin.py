
from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    readonly_fields = ['votes']
    model = Choice
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    actions = ["approve_all_selected_question", "reject_all_selected_question"]
    readonly_fields = ["was_published_recently"]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ['pub_date', 'status']
    search_fields = ['question_text']
    fieldsets = [
        (None, {'fields': ['question_text', 'status']}),
        ('Date information', {'fields': ['pub_date', 'was_published_recently']})
    ]
    inlines = [ChoiceInline]

    @admin.action(description="Approve all selected questions")
    def approve_all_selected_question(self, request, queryset):
        queryset.update(status=Question.Status.APPROVED)

    @admin.action(description="Reject all selected questions")
    def reject_all_selected_question(self, request, queryset):
        queryset.update(status=Question.Status.REJECTED)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "get_question_text", "votes"]
    readonly_fields = ["votes", "get_question_text"]
    search_fields = ["choice_text", "question__question_text"]
