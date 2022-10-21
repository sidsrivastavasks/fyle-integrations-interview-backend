from django.urls import path
from apps.teachers.views import TeacherAssignmentsView

urlpatterns = [
    path('assignments/', TeacherAssignmentsView.as_view(), name='teachers-assignments')
]
