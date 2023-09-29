# serializers.py
from rest_framework import serializers
from .models import ScreenRecording, SavedSharedVideo

class ScreenRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenRecording
        fields = '__all__'

class SavedSharedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedSharedVideo
        fields = '__all__'