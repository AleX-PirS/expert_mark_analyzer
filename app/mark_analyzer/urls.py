from django.urls import path

from .views import Login, Home, Logout, AccessDenied

app_name = 'mark_analyzer'

urlpatterns = [
    path('access_denied/', AccessDenied.as_view(), name='access_denied'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('home/', Home.as_view(), name='own_page'),
    # path('update/', VIEW, name='own_page_update'),

    # path('articles/', VIEW, name='articles'), # all
    # path('articles/add/', VIEW, name='add_article'), # worker
    # path('articles/<int:pk>/', VIEW, name='article_detail'), # all
    # path('articles/<int:pk>/mark/', VIEW, name='article_mark'), # expert
    # path('articles/<int:pk>/update/', VIEW, name='article_update'), # worker. if no marks yet 

    # path('experts/', VIEW, name='experts'), # all
    # path('experts/add/', VIEW, name='add_expert'), # worker
    # path('experts/<int:pk>/', VIEW, name='expert_detail'), # all
    # path('experts/<int:pk>/update/', VIEW, name='expert_update'), # worker

    # path('marks/', VIEW, name='marks'), # expert
]
