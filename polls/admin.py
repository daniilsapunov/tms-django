from django.contrib import admin

# Register your models here.
from .models import Question, Choice


admin.site.register(Choice)
admin.site.register(Question)


#@admin.register(Question)
#class QuestionAdmin(admin.ModelAdmin):
#   fields = ["question_text", "pub_date"]
#    readonly_fields = ["pub_date"]