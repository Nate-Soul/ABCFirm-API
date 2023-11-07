import os
import moviepy.editor as mp
import speech_recognition as sr
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

def transcribe_resource(resource, transcription_language, enable_speaker_recognition):
    
    if not resource:
        return None
    
    # content = resource.read()
    
    resource_type = check_file_type(resource)
    if resource_type == "video":
        video      = mp.VideoFileClip(resource, fps_source="tbr")
        audio_file = video.audio
    elif resource_type == "audio":
        audio_file = mp.AudioFileClip(resource)
    else:
        return Response(
            {"detail": "Unsupported File Extension"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    r = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        data = r.record(source)
        
    if enable_speaker_recognition:
        try:
            text = r.recognize_google(data, language=transcription_language)
            return text
        except sr.UnknownValueError:
            return Response(
                {"detail": "Speech Recognition could not understand audio"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except sr.RequestError as e:
            return Response(
                {"detail": "Could not request results from Google web speech API; {0}".format(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    
def resource_is_link(resource):
    if isinstance(resource, InMemoryUploadedFile):
        return False
    url_prefixes = ["http://", "https://", "ftp://", "ftps://", "www."]
    for prefix in url_prefixes:
        if resource.startswith(prefix):
            return True
    return False


def check_file_type(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension in [".mp4", ".avi", ".mkv", ".webm"]:
        return "video"
    elif file_extension in [".mp3", ".wav", ".ogg", ".flac"]:
        return "audio"
    else:
        return None


def get_resource_info(file_path):
    if os.path.exists(file_path):
        name, ext = os.path.splitext(os.path.basename(file_path)), check_file_type(file_path)
        return {"name": name, "type": ext, "duration": "120 mins"}
    else:
        return None
    
def save_temporary_file(uploaded_file):
    
    temporary_dir = settings.FILE_UPLOAD_TEMP_DIR
    
    with TemporaryUploadedFile(uploaded_file.name, uploaded_file.content_type, 0, None) as temp_file:
        with open(os.path.join(temporary_dir, uploaded_file.name), 'wb') as dest:
            for chunk in temp_file.chunks():
                dest.write(chunk)
                
    return os.path.join(temporary_dir, uploaded_file.name)