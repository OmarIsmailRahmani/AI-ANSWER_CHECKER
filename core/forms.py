from django import forms
from .models import Subject, Submission

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'reference_book']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_book': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class StudentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['student_fname', 'student_lname', 'student_id_number', 'answer_sheet', 'tutor_solution_text']
        widgets = {
            'student_fname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_lname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'answer_sheet': forms.FileInput(attrs={'class': 'form-control-file'}),
            'tutor_solution_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional: Add specific model answer here.'}),
        }