from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('home/', views.home, name='home'),

    # Subject Routes
    path('subjects/', views.subject_list_view, name='subjects'),
    path('subjects/add/', views.subject_create_view, name='subject_create'),
    path('subjects/<int:pk>/', views.subject_detail_view, name='subject_detail'),
    
    # Exam Routes
    path('subjects/<int:subject_id>/exams/add/', views.student_upload_view, name='exam_create'),
    
    # Submission & Evaluation Routes
    path('submissions/<int:pk>/', views.submission_detail_view, name='submission_detail'),
    path('subjects/<int:pk>/delete/', views.subject_delete_view, name='subject_delete'),
    path('submissions/<int:pk>/delete/', views.submission_delete_view, name='submission_delete'),
]