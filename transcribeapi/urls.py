from django.urls import path
from .views import TranscriptionListAPIView

app_name = 'transcribeapi'

urlpatterns = [
    path('', TranscriptionListAPIView.as_view(), name='transcribe-list-or-create'),
]