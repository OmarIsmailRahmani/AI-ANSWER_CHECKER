from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subject, Submission, Evaluation
from .forms import SubjectForm, StudentSubmissionForm
from .utils import extract_text_from_file
from .services import evaluate_exam_submission
'''
the home page view , where any new user lands, from here the person can register or log in
'''
def landing_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')

'''
The dashboard per user (needs authentication)
'''
@login_required
def home(request):
    return render(request, 'home.html')

'''
already created subjects by the teacher (needs authentication)
'''
@login_required
def subject_list_view(request):
    subjects = Subject.objects.filter(teacher=request.user).order_by('-created_at')
    return render(request, 'subject_list.html', {'subjects': subjects})
'''
function to create new subject (needs authentication)
'''
@login_required
def subject_create_view(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.teacher = request.user
            subject.save()
            
            if subject.reference_book:
                extracted_text = extract_text_from_file(subject.reference_book.path)
                subject.book_extracted_text = extracted_text
                subject.save()
                
            messages.success(request, "Subject created and textbook processed.")
            return redirect('subjects')
    else:
        form = SubjectForm()
    return render(request, 'subject_form.html', {'form': form})
'''
function to view submissions within subject (needs authentication)
'''
@login_required
def subject_detail_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk, teacher=request.user)
    submissions = subject.submissions.all().order_by('-uploaded_at')
    form = StudentSubmissionForm()
    return render(request, 'subject_detail.html', {'subject': subject, 'submissions': submissions, 'form': form})

'''
function to upload answer sheets (needs authentication)
'''
@login_required
def student_upload_view(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id, teacher=request.user)
    
    if request.method == 'POST':
        form = StudentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.subject = subject
            submission.save()

            try: #using try except because the ai call can fail due to many reasons but it should not crash the whole application
                ai_result = evaluate_exam_submission(
                    student_image_path=submission.answer_sheet.path,
                    subject_book_context=subject.book_extracted_text or "No textbook text available.",
                    tutor_solution_text=submission.tutor_solution_text
                )
                
                submission.extracted_text = ai_result.get('transcription_summary', '')
                submission.save()

                Evaluation.objects.create(
                    submission=submission,
                    score=ai_result.get('total_score', 0),
                    confidence=ai_result.get('confidence', 'Low'),
                    feedback=ai_result.get('pedagogical_feedback', 'No feedback.'),
                    rubric_data=ai_result.get('questions', []),
                    book_citations=ai_result.get('book_citations', '')
                )
                
                messages.success(request, f"Graded! Score: {ai_result.get('total_score')}%")
                return redirect('submission_detail', pk=submission.id)

            except Exception as e:
                messages.error(request, f"Grading Failed: {str(e)}")
                return redirect('subject_detail', pk=subject.id)
    
    return redirect('subject_detail', pk=subject.id)
'''
function to see the ai evaluation (needs authentication)
this is the main view which is shown after the paper has been evaluated by the AI
'''
@login_required
def submission_detail_view(request, pk):
    submission = get_object_or_404(Submission, pk=pk, subject__teacher=request.user)
    evaluation = getattr(submission, 'evaluation', None)
    return render(request, 'submission_detail.html', {'submission': submission, 'evaluation': evaluation})

'''
function to delete subject (needs authentication)
good for data privacy
'''
@login_required
def subject_delete_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk, teacher=request.user)
    if request.method == 'POST':
        subject.name_to_delete = subject.name
        subject.delete()
        messages.success(request, f"Subject '{subject.name_to_delete}' and all its submissions were deleted.")
        return redirect('subjects')
    return redirect('subjects')
'''
function to delete submission(needs authentication)
good for data privacy
'''
@login_required
def submission_delete_view(request, pk):
    submission = get_object_or_404(Submission, pk=pk, subject__teacher=request.user)
    subject_id = submission.subject.id
    if request.method == 'POST':
        submission.delete()
        messages.success(request, "Student submission deleted successfully.")
        return redirect('subject_detail', pk=subject_id)
    return redirect('subject_detail', pk=subject_id)