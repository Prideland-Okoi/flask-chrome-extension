# views.py
import os
import subprocess
import random
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import ScreenRecording, SavedSharedVideo
from .serializers import ScreenRecordingSerializer, SavedSharedVideoSerializer

def generate_random_string(length=10):
    """Generates a random string of the specified length."""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(length))

def generate_random_integer(min_value=0, max_value=100):
    """Generates a random integer between the specified minimum and maximum values."""
    return random.randint(min_value, max_value)

class ScreenRecordingViewSet(viewsets.ModelViewSet):
    queryset = ScreenRecording.objects.all()
    serializer_class = ScreenRecordingSerializer

    def create(self, request, *args, **kwargs):
        # Handle the incoming screen recording file
        uploaded_file = request.FILES.get('content')

        if not uploaded_file:
            return Response({'message': 'No file was provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a random string.
        random_string = generate_random_string()

        # Concatenate the random string to the filename.
        filename = f"my_file_{random_string}"

        # Create a temporary file path for the compressed video
        temp_video_path = os.path.join('/tmp', filename)

        # You can compress and process the file here before saving it.
        # For example, you might use a library like PIL or ffmpeg to compress video content.
        # Compress the video using ffmpeg
        try:
            subprocess.run([
                'ffmpeg',
                '-i', uploaded_file.temporary_file_path(),  # Input video file path
                '-vf', 'scale=640:-1',  # Example: Resize video to width 640 pixels
                '-c:v', 'libx264',  # Example: Video codec
                '-crf', '23',  # Example: Constant Rate Factor for quality (adjust as needed)
                '-c:a', 'aac',  # Example: Audio codec
                '-strict', 'experimental',  # Required for aac codec
                temp_video_path  # Output video file path
            ], check=True)
        except subprocess.CalledProcessError as e:
            return Response({'message': 'Video compression failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save the processed file
        screen_recording = ScreenRecording(content=temp_video_path)
        screen_recording.save()

        return Response({'message': 'Screen recording uploaded successfully.'}, status=status.HTTP_201_CREATED)

def share_screen_recording_api(request, id):
    screen_recording = get_object_or_404(ScreenRecording, id=id)
    email = request.POST.get('email')

    # Validate the email address
    try:
        validate_email(email)
    except ValidationError as e:
        return Response({'message': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

    # Share the screen recording using the email address
    screen_recording.share(attributes={'url': screen_recording.get_absolute_url(), 'filename': screen_recording.filename, 'email': email})

    # Return a success response
    return Response({'message': 'Screen recording shared successfully!'}, status=status.HTTP_201_CREATED)

class SharedVideoViewSet(viewsets.ModelViewSet):
    queryset = SavedSharedVideo.objects.all()
    serializer_class = SavedSharedVideoSerializer

    def create(self, request, *args, **kwargs):
        # Extract data from the request
        email = request.data.get('email')
        filename = request.data.get('filename')
        video_url = request.data.get('video_url')

        # Create a new SharedVideo instance
        shared_video = SavedSharedVideo(email=email, filename=filename, video_url=video_url)
        shared_video.save()

        return Response({'message': 'Video shared successfully.'}, status=status.HTTP_201_CREATED)
