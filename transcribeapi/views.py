from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import TranscriptionSerializer
from .utils import (
    transcribe_resource, 
    resource_is_link, 
    get_resource_info, 
    save_temporary_file
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
            resource_file = request.FILES.get("resource_file")
            resource_file_content = resource_file.read()
            get_transcribed_text = transcribe_resource(resource_file_content, transcription_language, enable_speaker_recognition)
            uploaded_file_path = save_temporary_file(resource_file)
            resource_info = get_resource_info(uploaded_file_path)
        elif resource_is_link(resource_link):
            pass
        
        data = {
            "transcription_language": transcription_language,
            "resource_file": resource_file if request.FILES else None,
            "enable_speaker_recognition": enable_speaker_recognition,
            "transcribed_text": get_transcribed_text,
            "resource_link": resource_link,
            "resource_name": resource_info["name"],
            "resource_duration": resource_info["duration"],
            "resource_type": resource_info["type"],
        }
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "it works", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)