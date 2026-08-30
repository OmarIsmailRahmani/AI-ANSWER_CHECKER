from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True, null=True)
    reference_book = models.FileField(upload_to='subject_books/')
    book_extracted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})" if self.code else self.name
'''class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=200)
    question_paper_file = models.FileField(upload_to='question_papers/', blank=True, null=True)
    question_text = models.TextField(blank=True, null=True, help_text="Optional: Type questions here if not on the answer sheet.")
    tutor_solution_file = models.FileField(upload_to='tutor_solutions/', blank=True, null=True)
    tutor_solution_text = models.TextField(blank=True, null=True)
    total_marks = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.subject.name}"    '''
    
class Submission(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='submissions')
    student_fname = models.CharField(max_length=100)
    student_lname = models.CharField(max_length=100)
    student_id_number = models.CharField(max_length=50, blank=True, null=True)
    answer_sheet = models.FileField(upload_to='student_answers/')
    tutor_solution_text = models.TextField(blank=True, null=True)
    extracted_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_fname} {self.student_lname} - {self.exam.title}"
    
    
    def __str__(self):
        return f"Submission by {self.student_fname,self.student_lname}"
    
    
class Evaluation(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    score = models.IntegerField()
    confidence = models.CharField(max_length=20, default='Medium')
    feedback = models.TextField(blank=True, null=True)
    rubric_data = models.JSONField(default=dict, blank=True)
    book_citations = models.TextField(blank=True, null=True)
    evaluated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Result: {self.submission} ({self.score}%)"
    
        