from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from lifequotesbot.models import Questions, Answers, ChatRecord, NoRecordFoundResponse


# Register your models here.
class AdminQuestions(ImportExportModelAdmin):
    list_display = ('question_keyword',)
    search_fields = ('question_keyword',)


class AdminAnswers(ImportExportModelAdmin):
    list_display = ('question_keyword', 'answer')
    search_fields = ('question_keyword__question_keyword', 'answer')


class AdminNoRecordFoundResponse(ImportExportModelAdmin):
    list_display = ('responsetext', )
    search_fields = ('responsetext', )


class AdminChatRecord(ImportExportModelAdmin):
    list_display = ('fb_user', 'message', 'response', 'timestamp')
    search_fields = ('fb_user', 'message', 'response', 'timestamp')


admin.site.register(Questions, AdminQuestions)
admin.site.register(Answers, AdminAnswers)
admin.site.register(NoRecordFoundResponse, AdminNoRecordFoundResponse)
admin.site.register(ChatRecord, AdminChatRecord)