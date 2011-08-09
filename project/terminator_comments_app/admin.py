from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.admin import CommentsAdmin
from terminator_comments_app.models import TerminatorComment

class TerminatorCommentAdmin(CommentsAdmin):
    fieldsets = (
        (_('Content'),
           {'fields': ('user', 'mail_me', 'comment')}
        ),
        (_('Metadata'), {
            'classes': ('collapse',),
            'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')
            }
        ),
        (_('Other data'), {
            'classes': ('collapse',),
            'fields': ('content_type', 'object_pk', 'site')
            }
        ),
     )

    list_display = ('user', 'comment_thread', 'ip_address', 'submit_date', 'mail_me', 'is_public', 'is_removed')
    list_filter = ('submit_date', 'mail_me', 'site', 'is_public', 'is_removed')
    
    def get_actions(self, request):
        actions = super(TerminatorCommentAdmin, self).get_actions(request)
        actions.pop('flag_comments')
        actions.pop('approve_comments')
        actions.pop('remove_comments')
        return actions


admin.site.register(TerminatorComment, TerminatorCommentAdmin)



