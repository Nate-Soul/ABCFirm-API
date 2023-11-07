from rest_framework import serializers
from .models import Transcription as TranscriptionModel

class TranscriptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TranscriptionModel
        fields = "__all__"