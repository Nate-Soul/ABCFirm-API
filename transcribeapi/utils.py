import os
import moviepy.editor as mp
import speech_recognition as sr
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.response import Response
from rest_framework import status

def transcribe_resource(resource, transcription_language, enable_speaker_recognition):
    if resource_is_link(resource):
        return None
    
    # else:
    resource_type = check_resource_type(resource)
    if resource_type == "video":
        video      = mp.VideoFileClip(resource)
        audio_file = video.audio
    elif resource_type == "audio":
        audio_file = mp.AudioFileClip(resource)
    else:
        print("Unsupported file extension")
    
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
    else:
        return None    
    
    
def resource_is_link(resource):
    if isinstance(resource, InMemoryUploadedFile):
        return False
    url_prefixes = ["http://", "https://", "ftp://", "ftps://", "www."]
    for prefix in url_prefixes:
        if resource.startswith(prefix):
            return True
    return False


def check_resource_type(resource):
    file_extension = os.path.splitext(resource)[1].lower()    
    
    if file_extension in [".mp4", ".avi", ".mkv", ".webm"]:
        return "video"
    elif file_extension in [".mp3", ".wav", ".ogg", ".flac"]:
        return "audio"
    else:
        return None


def get_resource_info(resource):
    file_type = check_resource_type(resource)
    name, ext = os.path.splitext(os.path.basename(resource)), file_type, "120 mins"
    return {"name": name, "type": file_type, "duration": ext}