from django import forms

class TaskForm(forms.Form):
    task_title = forms.CharField(max_length=200)
    task_description = forms.CharField(max_length=1000, widget=forms.Textarea, required=False)