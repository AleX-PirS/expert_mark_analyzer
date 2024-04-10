from django.urls import path

from .views import Login, Home, Logout, AccessDenied, HomeUpdate, AddUser,\
AddArticle, Articles, ArticleDetail, Experts, ExpertDetail

app_name = 'mark_analyzer'

urlpatterns = [
    path('access_denied/', AccessDenied.as_view(), name='access_denied'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('home/', Home.as_view(), name='own_page'),
    path('update/', HomeUpdate.as_view(), name='own_page_update'),

    path('articles/', Articles.as_view(), name='articles'),
    path('articles/add/', AddArticle.as_view(), name='add_article'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    # path('articles/<int:pk>/mark/', VIEW, name='article_mark'), # expert

    path('experts/', Experts.as_view(), name='experts'),
    path('experts/add/', AddUser.as_view(), name='add_expert'),
    path('experts/<str:username>/', ExpertDetail.as_view(), name='expert_detail'),

    # path('home/marks/', VIEW, name='marks'), # expert
    # path('home/articles', VIEW, name='marks'), # worker
]
