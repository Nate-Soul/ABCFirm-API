from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import TranscriptionSerializer
from .utils import (
    transcribe_resource,
    get_resource_duration,
    get_resource_type,
)

# Create your views here.
class TranscriptionListAPIView(APIView):
    
    serializer_class = TranscriptionSerializer
    parser_classes   = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        
        resource_link = request.data.get("resource_link", None)
        transcription_language = request.data.get("transcription_language")
        enable_speaker_recognition = request.data.get("enable_speaker_recognition", False)
        
        if request.FILES:
            resource_file         = request.FILES.get("resource_file")
            resource_duration     = get_resource_duration(resource_file)
            resource_type         = get_resource_type(resource_file)
            get_transcribed_text  = transcribe_resource(resource_file, transcription_language, enable_speaker_recognition)
        elif resource_link:
            pass
        
        data = {
            "transcription_language": transcription_language,
            "resource_file": resource_file if request.FILES else None,
            "enable_speaker_recognition": enable_speaker_recognition,
            "transcribed_text": get_transcribed_text,
            "resource_link": resource_link,
            "resource_duration": resource_duration,
            "resource_type": resource_type,
        }
        
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                "success": True,
                "detail": "File successfully transcribed",
                "data": serializer.data
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)