from django.shortcuts import render, redirect
from django.views import View

from .models import Article, Expert, Marks
from .forms import ArticleForm, ExpertMarksFormSet
from .analize import Analyzer

class Experts(View):
    def get(self, request, *args, **kwargs):
        ids = []
        article_id = request.GET.get("article_id", -1)
        id1 = request.GET.get("id1", -1)
        if id1 != -1:
            ids.append(id1)
        id2 = request.GET.get("id2", -1)
        if id2 != -1:
            ids.append(id2)
        id3 = request.GET.get("id3", -1)
        if id3 != -1:
            ids.append(id3)
        
        if len(ids) == 0: 
            return render(
                request, 
                'experts.html',
                {
                    "title": Expert._meta.verbose_name_plural,
                    "query": Expert.objects.all(),
                }
            )

        # experts_bad = Expert.objects.filter(uid__in=ids).all()
        # marks = Marks.objects.filter(article_id=article_id).all()
        # exp_ids = [mk.uid for mk in marks]
        # was_experts_good = Expert.objects.filter(uid__in=exp_ids).exclude(experts_bad).get()
        # experts_all = Expert.objects.all().exclude(experts_bad+was_experts_good)

        experts_bad = Expert.objects.filter(uid__in=ids)
        marks = Marks.objects.filter(article_id=article_id)
        exp_ids = [mk.expert_id_id for mk in marks]
        was_experts_good = Expert.objects.filter(uid__in=exp_ids).exclude(uid__in=experts_bad.values_list('uid', flat=True))
        experts_all = Expert.objects.exclude(uid__in=experts_bad.values_list('uid', flat=True)).exclude(uid__in=was_experts_good.values_list('uid', flat=True))


        experts_to_check = list(was_experts_good)+list(experts_all.all()[:3-len(was_experts_good)])

        print(experts_to_check)


        return render(
                request, 
                'experts.html',
                {
                    "title": Expert._meta.verbose_name_plural,
                    "query": experts_to_check,
                }
            )

    
class Articles(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 
            'articles.html',
            {
                "title": Article._meta.verbose_name_plural,
                "query": Article.objects.all(),
            }
        )

class MarkForm(View):
    def get(self, request, *args, **kwargs):
        article_form = ArticleForm(instance=None)
        formset = ExpertMarksFormSet(queryset=Marks.objects.none())

        return render(request, 'marks_form.html', {'article_form': article_form, 'formset': formset})


    def post(self, request, *args, **kwargs):
        article_form = ArticleForm(request.POST)
        formset = ExpertMarksFormSet(request.POST)

        if article_form.is_valid() and formset.is_valid():
            all_marks_filled = all(all(form.cleaned_data.get(field) for field in ['pni_1', 'pni_2', 'pni_3', 'pni_4', 'pni_5', 'pni_6', 'po_1', 'po_2', 'po_3', 'po_4', 'po_5']) for form in formset)
            marks_to_save = []
            
            if all_marks_filled:
                article = article_form.save()
                for form in formset:
                    marks = form.save(commit=False)
                    marks.article_id = article
                    marks.save()
                    marks_to_save.append(marks)
            else:
                return render(request, 'marks_form.html', {'article_form': article_form, 'formset': formset})
                
            Analyzer.calculate_total_mark(marks_to_save)
            consistency = Analyzer.compute_consistency([mark.to_array() for mark in marks_to_save])
            if len(consistency) == 0:
                article.status = 1
                article.save()
                return redirect('/articles/')
            
            article.status = -1
            article.save()

            url = f"/?article_id={article.uid}&"
            for idx, expert_index in enumerate(consistency):
                url += f"id{idx+1}={marks_to_save[expert_index].expert_id.uid}&"

            return redirect(f'/experts{url[:-1]}')          
        
        return render(request, 'marks_form.html', {'article_form': article_form, 'formset': formset})
