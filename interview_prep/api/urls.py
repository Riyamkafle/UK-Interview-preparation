from django.urls import path
from .views import UniversityListView, QuestionListView, EvaluateView

urlpatterns = [
    path("universities/", UniversityListView.as_view(), name="universities"),
    path("questions/", QuestionListView.as_view(), name="questions"),
    path("evaluate/", EvaluateView.as_view(), name="evaluate"),
]
