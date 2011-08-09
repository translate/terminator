from terminator_comments_app.models import TerminatorComment
from terminator_comments_app.forms import TerminatorCommentForm

def get_model():
    return TerminatorComment

def get_form():
    return TerminatorCommentForm
