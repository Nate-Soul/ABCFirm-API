from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Transcription(models.Model):
    
    RESOURCE_TYPE_CHOICES = (
        ("audio", "Audio"),
        ("video", "Video"),
        ("link", "Link"),
        ("unknown", "Unknown")
    )
    
    resource_file = models.FileField(
        verbose_name=_("Resource"),
        upload_to="uploads/",
        null=True,
        blank=True
    )
    
    resource_name = models.TextField(
        verbose_name=_("Resource Name"),
        null=True,
        blank=True,
    )
    
    resource_link = models.TextField(
        verbose_name=_("Resource Link"),
        null=True,
        blank=True,
    )
    
    resource_type = models.CharField(
        verbose_name=_("Resource Type"),
        choices=RESOURCE_TYPE_CHOICES,
        max_length=20,
        default="unknown"
    )
    
    resource_duration = models.CharField(
        verbose_name=_("Resource Duration/Length"),
        max_length=50,
        null=True,
        blank=True     
    )
    
    transcribed_text = models.TextField(
        verbose_name=_("Transcribed Text"),
        null=True,
        blank=False
    )
    
    transcription_language = models.CharField(
        verbose_name=_("Transcription Language"),
        max_length=50,
    )
    
    enable_speaker_recognition = models.BooleanField(
        verbose_name=_("Enable Speaker Recognition?"),
        default=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Transcription")
        verbose_name_plural = _("Transcriptions")
        
    def __str__(self):
        return f"New Resource Transcribed @ {self.created_at}"