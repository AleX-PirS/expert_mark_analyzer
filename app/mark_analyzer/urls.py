from django.urls import path

from .views import Experts, Articles, MarkForm

app_name = 'mark_analyzer'

urlpatterns = [
    path('experts/', Experts.as_view(), name='experts'),
    path('articles/', Articles.as_view(), name='articles'),
    path('mark/', MarkForm.as_view(), name='create_mark'),
    # path('source/<int:pk>', SourceDetail.as_view(), name='detail_source'),
]
