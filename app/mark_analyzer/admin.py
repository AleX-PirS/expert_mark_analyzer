from django.contrib import admin
from .models import User, Theme, UserTheme, Criteria, MarkList, \
MarkListCriteria, Article, ArticleTheme, Score, ScoreCriteria

admin.site.register(User)
admin.site.register(Theme)
admin.site.register(UserTheme)
admin.site.register(Criteria)
admin.site.register(MarkList)
admin.site.register(MarkListCriteria)
admin.site.register(Article)
admin.site.register(ArticleTheme)
admin.site.register(Score)
admin.site.register(ScoreCriteria)
