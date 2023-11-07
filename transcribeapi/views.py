from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import TranscriptionSerializer
from .utils import transcribe_resource, resource_is_link, get_resource_info

# Create your views here.
class TranscriptionListAPIView(APIView):
    
    serializer_class = TranscriptionSerializer
    parser_classes   = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        
        resource = request.data.get("resource")
        transcription_language = request.data.get("transcription_language")
        enable_speaker_recognition = request.data.get("enable_speaker_recognition")
        
        get_transcribed_text = transcribe_resource(resource, transcription_language, enable_speaker_recognition)
        
        is_link = resource_is_link(resource)
        
        if is_link:
            resource_info = get_resource_info(resource)
        
        data = {
            "transcription_language": transcription_language,
            "resource": resource if request.FILES else None,
            "enable_speaker_recognition": enable_speaker_recognition,
            "transcribed_text": get_transcribed_text,
            "resource_name": resource_info["name"] if resource_info else None,
            "resource_type": resource_info["type"] if resource_info else "link",
            "resource_duration": resource_info["duration"] if resource_info else None,
            "resource_link": resource if is_link else None
        }
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "it works", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)