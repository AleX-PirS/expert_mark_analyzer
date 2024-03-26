from django import forms


class ArticleForm(forms.ModelForm):
    class Meta:
        # model = Article
        fields = ['title', 'author_full_name']

# ExpertMarksFormSet = forms.modelformset_factory(Marks, fields = ['expert_id', 'pni_1', 'pni_2', 'pni_3', 'pni_4', 'pni_5', 'pni_6', 'po_1', 'po_2', 'po_3', 'po_4', 'po_5'], extra=3)

