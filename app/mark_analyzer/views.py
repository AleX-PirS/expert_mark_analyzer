from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import HttpResponse

from .models import User, Article, Theme
from .forms import ArticleForm, ChangeUserInfoForm, NewUserForm
# from .analize import Analyzer

class AccessDenied(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'access_denied.html')

class Login(View):
    def get(self, request, *args, **kwargs):
        first_attempt = True
        first_attempt_query = request.GET.get('first_attempt')
        if first_attempt_query == 'false':
            first_attempt = False
        return render(request, 'login.html', {'first_attempt':first_attempt})
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
      
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/home/')
        
        return redirect(f'/login/?first_attempt=false')
    
class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/login/')
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('/login/')

class HomeUpdate(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        form = ChangeUserInfoForm(initial={
            'about': user.about,
            'first_name': user.first_name,
            'second_name': user.last_name,
            'birthday': user.birthday,
        })
        
        return render(request, 'update_home.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ChangeUserInfoForm(request.POST)

        first_name = form.data['first_name']
        second_name = form.data['second_name']
        password = form.data['password']
        birthday = form.data['birthday']
        about = form.data['about']

        if form.is_valid():    
            user = User.objects.get(username=request.user.username)

            user.about = about
            user.first_name = first_name
            user.last_name = second_name
            user.birthday = birthday
            if len(password)>1:
                user.set_password(password)
            user.save()
        else:
            form = ChangeUserInfoForm(initial={
                'about': about,
                'first_name': first_name,
                'second_name': second_name,
                'birthday': birthday,
                'password': password,
            })
            return render(request, 'create_article.html', {'form': form})

        return redirect('/home/')

class AddUser(View):
    def get(self, request, *args, **kwargs):
        form = NewUserForm()        
        return render(request, 'add_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = NewUserForm(request.POST)

        first_name = form.data['first_name']
        second_name = form.data['second_name']
        username = form.data['username']
        password = form.data['password']
        role = form.data['role']

        if form.is_valid():    
            user = User.objects.create()

            user.first_name = first_name
            user.last_name = second_name
            user.username = username
            user.role = role
            user.set_password(password)

            user.save()
        else:
            form = NewUserForm(initial={
                'first_name': first_name,
                'second_name': second_name,
                'username': username,
                'password': password,
                'role': role,
            })
            return render(request, 'add_user.html', {'form': form})

        return redirect('/home/')

class AddArticle(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()        
        return render(request, 'add_article.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)

        author = form.data['author']
        title = form.data['title']
        link = form.data['link']
        mark_list = form.data['mark_list']
        theme = form.data['theme']

        if form.is_valid():    
            user = User.objects.get(username=request.user.username)
            article = Article.objects.create()
            theme_obj = Theme.objects.get(title=theme)
            
            article.created_by = user
            article.author = author
            article.title = title
            article.link = link
            article.theme_id = theme_obj

            article.save()

            # Create event NEW_ARTICLE (theme, mark_list) -> create X score works to some experts
            # If all X scores are allocated to experts, then change ARTICLE status to ON_MARK

        else:
            form = ChangeUserInfoForm(initial={
                'author': author,
                'title': title,
                'link': link,
                'mark_list': mark_list,
                'theme': theme,
            })
            return render(request, 'add_article.html', {'form': form})

        return redirect('/home/')

class Articles(View):
    def get(self, request, *args, **kwargs):
        # Add page actions (../?page=1...n)
        articles = Article.objects.all()
        # Some function to prep article to THAT user
        return render(request, 'articles.html', {'articles':articles})

class ArticleDetail(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        # Some function to prep article to THAT user
        return render(request, 'article_detail.html', {'article':article})

class Experts(View):
    def get(self, request, *args, **kwargs):
        # Add page actions (../?page=1...n)
        experts = User.objects.filter(role=User.EXPERT).all()
        return render(request, 'experts.html', {'experts':experts})

class ExpertDetail(View):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        username_current=request.user.username

        if username == username_current:
            redirect('/home/')
        expert = get_object_or_404(User, username=username)
        return render(request, 'expert_detail.html', {'expert':expert})

class Home(View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)

        match user.role:
            case User.EXPERT:
                return render(request, 'page_expert.html', {'user':user})
            case User.WORKER:
                return render(request, 'page_worker.html', {'user':user})

# class Experts(View):
#     def get(self, request, *args, **kwargs):
#         ids = []
#         article_id = request.GET.get("article_id", -1)
#         id1 = request.GET.get("id1", -1)
#         if id1 != -1:
#             ids.append(id1)
#         id2 = request.GET.get("id2", -1)
#         if id2 != -1:
#             ids.append(id2)
#         id3 = request.GET.get("id3", -1)
#         if id3 != -1:
#             ids.append(id3)
        
#         if len(ids) == 0: 
#             return render(
#                 request, 
#                 'experts.html',
#                 {
#                     "title": Expert._meta.verbose_name_plural,
#                     "query": Expert.objects.all(),
#                 }
#             )

#         # experts_bad = Expert.objects.filter(uid__in=ids).all()
#         # marks = Marks.objects.filter(article_id=article_id).all()
#         # exp_ids = [mk.uid for mk in marks]
#         # was_experts_good = Expert.objects.filter(uid__in=exp_ids).exclude(experts_bad).get()
#         # experts_all = Expert.objects.all().exclude(experts_bad+was_experts_good)

#         experts_bad = Expert.objects.filter(uid__in=ids)
#         marks = Marks.objects.filter(article_id=article_id)
#         exp_ids = [mk.expert_id_id for mk in marks]
#         was_experts_good = Expert.objects.filter(uid__in=exp_ids).exclude(uid__in=experts_bad.values_list('uid', flat=True))
#         experts_all = Expert.objects.exclude(uid__in=experts_bad.values_list('uid', flat=True)).exclude(uid__in=was_experts_good.values_list('uid', flat=True))


#         experts_to_check = list(was_experts_good)+list(experts_all.all()[:3-len(was_experts_good)])

#         print(experts_to_check)


#         return render(
#                 request, 
#                 'experts.html',
#                 {
#                     "title": Expert._meta.verbose_name_plural,
#                     "query": experts_to_check,
#                 }
#             )

    
# class Articles(View):
#     def get(self, request, *args, **kwargs):
#         return render(
#             request, 
#             'articles.html',
#             {
#                 "title": Article._meta.verbose_name_plural,
#                 "query": Article.objects.all(),
#             }
#         )

# class MarkForm(View):
#     def get(self, request, *args, **kwargs):
#         article_form = ArticleForm(instance=None)
#         formset = ExpertMarksFormSet(queryset=Marks.objects.none())

#         return render(request, 'marks_form.html', {'article_form': article_form, 'formset': formset})


#     def post(self, request, *args, **kwargs):
#         article_form = ArticleForm(request.POST)
#         formset = ExpertMarksFormSet(request.POST)

#         if article_form.is_valid() and formset.is_valid():
#             all_marks_filled = all(all(form.cleaned_data.get(field) for field in ['pni_1', 'pni_2', 'pni_3', 'pni_4', 'pni_5', 'pni_6', 'po_1', 'po_2', 'po_3', 'po_4', 'po_5']) for form in formset)
#             marks_to_save = []
            
#             if all_marks_filled:
#                 article = article_form.save()
#                 for form in formset:
#                     marks = form.save(commit=False)
#                     marks.article_id = article
#                     marks.save()
#                     marks_to_save.append(marks)
#             else:
#                 return render(request, 'marks_form.html', {'article_form': article_form, 'formset': formset})
                
#             Analyzer.calculate_total_mark(marks_to_save)
#             consistency = Analyzer.compute_consistency([mark.to_array() for mark in marks_to_save])
#             if len(consistency) == 0:
#                 article.status = 1
#                 article.save()
#                 return redirect('/articles/')
            
#             article.status = -1
#             article.save()

#             url = f"/?article_id={article.uid}&"
#             for idx, expert_index in enumerate(consistency):
#                 url += f"id{idx+1}={marks_to_save[expert_index].expert_id.uid}&"

#             return redirect(f'/experts{url[:-1]}')          
        
#         return render(request, 'marks_form.html', {'article_form': article_form, 'formset': formset})
