import os
import moviepy.editor as mp
import mimetypes
import speech_recognition as sr
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

def transcribe_resource(resource, transcription_language, enable_speaker_recognition):
    
    if not resource:
        return None
    
    resource_content = resource.read()
    resource_type = get_resource_type(resource)
    
    if resource_type == "video":
        try:
            video      = mp.VideoFileClip(resource_content)
            audio      = video.audio            
        except Exception as e:
            return None
                
    elif resource_type == "audio":
        try:
            audio = mp.AudioFileClip(resource.name)
        except Exception as e:
            return None
            
    #Transcribe the audio file
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio.write_audiofile("temp_audio.wav")) as source:
        audio_data = recognizer.record(source)
        
    language_code = transcription_language    
    if enable_speaker_recognition:
        language_code += "-speaker"
    
    try:
        transcribed_text = recognizer.recognize_google(audio_data, language=language_code)
        return transcribed_text
    except sr.UnknownValueError:
        return Response(
            {"detail": "Speech Recognition could not understand speech in audio file"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except sr.RequestError as e:
        return Response(
            {"detail": "Could not request results from Google web speech API; {0}".format(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    finally:
        video.close()
        audio.close()
        os.remove("temp_audio.wav")    
    
def resource_is_link(resource):
    if isinstance(resource, InMemoryUploadedFile):
        return False
    url_prefixes = ["http://", "https://", "ftp://", "ftps://", "www."]
    for prefix in url_prefixes:
        if resource.startswith(prefix):
            return True
    return False


def get_resource_type(resource):
    file_mimetype = resource.content_type
    if file_mimetype.startswith("video/"):
        return "video"
    elif file_mimetype.startswith("audio/"):
        return "audio"
    else:
        return None
        
    
def get_resource_duration(resource):
    resource_contents = resource.read()
    resource_type     = get_resource_type(resource)
    if resource_type == "video":
        try:
            video = mp.VideoFileClip(resource_contents)
            duration = video.duration
            video.close()
            return duration
        except Exception as e:
            return None
                  
    elif resource_type == "audio":
        try:
            audio = mp.AudioFileClip(resource_contents)
            duration = audio.duration
            audio.close()
            return duration
        except Exception as e:
            return None
    else:
        return None
    
def save_temporary_file(uploaded_file):
    
    temporary_dir = settings.FILE_UPLOAD_TEMP_DIR
    
    with TemporaryUploadedFile(uploaded_file.name, uploaded_file.content_type, 0, None) as temp_file:
        with open(os.path.join(temporary_dir, uploaded_file.name), 'wb') as dest:
            for chunk in temp_file.chunks():
                dest.write(chunk)
                
    return os.path.join(temporary_dir, uploaded_file.name)